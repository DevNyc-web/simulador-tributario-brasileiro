"""Integração motor x frontend: POST /resultado, adaptador de formulário, apresentação."""
import re
from decimal import Decimal as D
from pathlib import Path

import pytest

from app import create_app
from src.services.presentation import brl, decimal_br, humanize, pct
from src.services.simulation_input_adapter import (
    SimulationInputError,
    build_scenario,
    parse_brl_input,
)

ROOT = Path(__file__).resolve().parents[1]
VERDICT = ("melhor", "pior", "vantagem", "recomendado", "economiza", "ideal", "vencedor")


@pytest.fixture
def client():
    return create_app().test_client()


def text(response) -> str:
    html = response.get_data(as_text=True)
    main = re.search(r"<main.*?</main>", html, re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", main.group(0) if main else html))


def hist(n, receita="20000", folha="6000"):
    out = {}
    for i in range(1, n + 1):
        out[f"hist_receita_{i}"] = receita
        out[f"hist_folha_{i}"] = folha
    return out


def pf(**kw):
    return {"tipo_simulacao": "pf", "renda_mensal": "8000,50", "plano_inss": "NORMAL", **kw}


def mei(**kw):
    return {"tipo_simulacao": "mei", "receita_acumulada": "50000", "categoria": "SERVICOS",
            "meses_atividade_no_ano": "12", "optante_simei": "sim", **kw}


def simples(meses="4", folha="6000", **kw):
    base = {"tipo_simulacao": "simples", "receita_pa": "20000", "folha_pa": "6000",
            "receita_acumulada_ano": "100000", "atividade": "CONSULTORIA", "meses_desde_abertura": meses,
            "meses_atividade_no_ano": "12", "optante_simples": "sim"}
    n = min(int(meses) - 1, 12)
    return {**base, **hist(n, folha=folha), **kw}


def comparar(**kw):
    base = {"tipo_simulacao": "comparar", "receita_mensal": "20000", "plano_inss": "NORMAL",
            "prolabore": "6000", "receita_acumulada_ano": "100000", "atividade": "CONSULTORIA",
            "meses_desde_abertura": "13", "meses_atividade_no_ano": "12", "optante_simples": "sim",
            "dividendos": "3000", "modo_apuracao": "COM_ESCRITURACAO", "lucro_contabil_disponivel": "10000",
            **hist(12)}
    return {**base, **kw}


# --- parser de moeda ---

@pytest.mark.parametrize("raw,expected", [
    ("8000", "8000"), ("8000.50", "8000.50"), ("8000,50", "8000.50"), ("8.000,50", "8000.50"),
    ("R$ 1.234.567,89", "1234567.89"), ("8.000", "8000"), ("0", "0"), ("0,5", "0.5"), ("  12,30 ", "12.30"),
])
def test_parse_brl_input_valid(raw, expected):
    v = parse_brl_input(raw)
    assert isinstance(v, D) and v == D(expected)


@pytest.mark.parametrize("raw", ["", "abc", "-5", "NaN", "Infinity", "1e3", "1,234,56", "8.00.0,50", "12,345", "1..2", "9" * 20])
def test_parse_brl_input_rejects(raw):
    with pytest.raises(ValueError):
        parse_brl_input(raw)


def test_parse_brl_input_negative_only_when_allowed_and_tax_rules_parser_untouched():
    assert parse_brl_input("-5,5", allow_negative=True) == D("-5.5")
    from src.tax_rules import parse_decimal
    from src.tax_rules.exceptions import InvalidDecimalValueError
    with pytest.raises(InvalidDecimalValueError):
        parse_decimal("8000,50")  # o parser do JSON continua estrito


# --- PF ---

def test_pf_valid_post(client):
    r = client.post("/resultado", data=pf())
    assert r.status_code == 200
    t = text(r)
    assert "INSS" in t and "IRPF" in t and "R$ 8.000,50" in t and "Líquido estimado" in t
    assert "TR-001" in t and "TR-002" in t
    assert "Simulação educacional baseada nas premissas informadas" in t


@pytest.mark.parametrize("renda", ["8000,50", "8.000,50"])
def test_pf_accepts_brazilian_formats(client, renda):
    r = client.post("/resultado", data=pf(renda_mensal=renda))
    assert r.status_code == 200 and "R$ 8.000,50" in text(r)


def test_pf_invalid_income_shows_error_and_keeps_values(client):
    r = client.post("/resultado", data=pf(renda_mensal="abc"))
    assert r.status_code == 422
    html = r.get_data(as_text=True)
    assert "Informe um valor válido" in html and 'value="abc"' in html and "Traceback" not in html
    assert 'aria-invalid="true"' in html and 'role="alert"' in html


def test_pf_invalid_plan_controlled_error(client):
    r = client.post("/resultado", data=pf(plano_inss="INEXISTENTE"))
    assert r.status_code == 422 and "Selecione uma opção válida" in text(r)


def test_negative_income_rejected(client):
    assert client.post("/resultado", data=pf(renda_mensal="-100")).status_code == 422


def test_unknown_type_is_400_not_500(client):
    assert client.post("/resultado", data={"tipo_simulacao": "x"}).status_code == 400
    assert client.post("/resultado", data={}).status_code == 400


def test_get_result_still_empty_state(client):
    assert "Nenhuma simulação disponível." in text(client.get("/resultado"))


# --- MEI ---

def test_mei_valid(client):
    t = text(client.post("/resultado", data=mei()))
    assert "R$ 86,05" in t and "Dentro do limite" in t and "R$ 81.000,00" in t and "TR-004" in t
    assert "SERVICOS" not in t and "COMPATIVEL" not in t


def test_mei_zero_revenue_das_still_shown(client):
    assert "R$ 86,05" in text(client.post("/resultado", data=mei(receita_acumulada="0")))


def test_mei_excess_situation_labels(client):
    assert "sem superar 20%" in text(client.post("/resultado", data=mei(receita_acumulada="90.000,00")))
    assert "em mais de 20%" in text(client.post("/resultado", data=mei(receita_acumulada="100000")))


def test_mei_invalid_category_and_months(client):
    assert client.post("/resultado", data=mei(categoria="OUTRA")).status_code == 422
    assert client.post("/resultado", data=mei(meses_atividade_no_ano="13")).status_code == 422
    assert client.post("/resultado", data=mei(meses_atividade_no_ano="")).status_code == 422


def test_mei_not_optante_not_supported_no_fictitious_values(client):
    r = client.post("/resultado", data=mei(optante_simei="nao"))
    t = text(r)
    assert r.status_code == 200 and "Cenário não suportado pelo MVP" in t and "R$ 86,05" not in t
    assert "enquadrado no SIMEI" in t


# --- Simples ---

def test_simples_anexo_iii(client):
    t = text(client.post("/resultado", data=simples()))
    assert "Anexo III" in t and "Fator R 0,30" in t and "2ª" in t and "R$ 1.460,00" in t
    assert "RBT12p" in t and "TR-006" in t


def test_simples_anexo_v(client):
    t = text(client.post("/resultado", data=simples(folha="1000")))
    assert "Anexo V" in t and "TR-007" in t


def test_simples_insufficient_history_controlled_error(client):
    data = simples(meses="4")
    data.pop("hist_receita_3")
    r = client.post("/resultado", data=data)
    assert r.status_code == 422 and "hist_receita_3" in r.get_data(as_text=True) and "Campo obrigatório" in text(r)


def test_simples_history_quantity_by_months(client):
    assert client.post("/resultado", data=simples(meses="1")).status_code == 200  # nenhum mês anterior
    assert client.post("/resultado", data=simples(meses="2")).status_code == 200  # 1 mês anterior
    assert client.post("/resultado", data={**simples(meses="13"), **hist(12)}).status_code == 200
    data = simples(meses="13")
    data.pop("hist_receita_12")  # 13+ exige 12 meses anteriores
    assert client.post("/resultado", data=data).status_code == 422


def test_simples_extra_history_rows_are_ignored(client):
    assert client.post("/resultado", data={**simples(meses="2"), **hist(12)}).status_code == 200


def test_simples_inconsistent_model_validation_is_controlled(client):
    r = client.post("/resultado", data=simples(receita_acumulada_ano="1"))
    assert r.status_code == 422 and "deve incluir a receita do PA" in text(r)


def test_simples_above_mvp_support_shows_not_supported(client):
    data = simples(meses="13", receita_pa="300001", folha_pa="6000", receita_acumulada_ano="300001")
    data.update(hist(12, receita="300001"))
    r = client.post("/resultado", data=data)
    t = text(r)
    assert r.status_code == 200 and "Cenário não suportado pelo MVP" in t and "ISS" in t
    assert "DAS estimado" not in t and "Alíquota efetiva" not in t


def test_simples_over_legal_limit_incompatible(client):
    t = text(client.post("/resultado", data=simples(receita_acumulada_ano="4.800.000,01")))
    assert "Cenário incompatível com o regime" in t and "DAS estimado" not in t


def test_simples_first_month_zero_zero_not_supported(client):
    data = simples(meses="1", receita_pa="0", folha_pa="0", receita_acumulada_ano="0")
    t = text(client.post("/resultado", data=data))
    assert "Cenário não suportado pelo MVP" in t and "não atribui 0,01 nem 0,28" in t


# --- Comparador ---

def test_comparator_valid_side_by_side(client):
    t = text(client.post("/resultado", data=comparar()))
    for label in ("Pessoa Física", "Pessoa Jurídica", "Diferenças numéricas", "IRRF sobre dividendos",
                  "Valor recebido pela pessoa física no cenário PJ", "Diferença de tributos"):
        assert label in t


def test_comparator_single_revenue_field_feeds_pf_and_pj(client):
    t = text(client.post("/resultado", data=comparar(receita_mensal="20000")))
    assert t.count("R$ 20.000,00") >= 2  # receita PF e faturamento PJ
    scenario = build_scenario(comparar(receita_mensal="20000"))["entrada"]
    assert scenario.pf_input.renda_mensal == scenario.simples_input.receita_pa == D("20000")


def test_comparator_folha_pa_derived_from_prolabore():
    e = build_scenario(comparar(prolabore="4.321,09"))["entrada"]
    assert e.simples_input.folha_pa == e.prolabore == D("4321.09")


def test_comparator_without_bookkeeping(client):
    data = comparar(modo_apuracao="SEM_ESCRITURACAO", dividendos="3000")
    data.pop("lucro_contabil_disponivel")
    t = text(client.post("/resultado", data=data))
    assert "Diferenças numéricas" in t and "Limite sem escrituração" in t


def test_comparator_without_bookkeeping_above_limit_not_supported(client):
    data = comparar(modo_apuracao="SEM_ESCRITURACAO", dividendos="20000")
    t = text(client.post("/resultado", data=data))
    assert "Cenário não suportado pelo MVP" in t and "excede o limite de isenção" in t
    assert "Diferença de tributos" not in t


def test_comparator_with_bookkeeping(client):
    t = text(client.post("/resultado", data=comparar()))
    assert "escrituração contábil regular" in t


def test_comparator_missing_profit_when_required(client):
    data = comparar()
    data.pop("lucro_contabil_disponivel")
    r = client.post("/resultado", data=data)
    assert r.status_code == 422 and "lucro_contabil_disponivel" in r.get_data(as_text=True)


def test_comparator_dividends_above_limit_show_irrf(client):
    t = text(client.post("/resultado", data=comparar(dividendos="60000", lucro_contabil_disponivel="70000")))
    assert "IRRF sobre dividendos R$ 6.000,00" in t


def test_comparator_optional_high_income_field(client):
    t = text(client.post("/resultado", data=comparar(renda_anual_relevante="600.000,01")))
    assert "tributação mínima anual" in t
    assert "não foi avaliada" in text(client.post("/resultado", data=comparar()))


def test_comparator_page_has_no_verdict_words(client):
    pages = [text(client.post("/resultado", data=comparar())), text(client.get("/simulacao/comparar"))]
    for t in pages:
        words = set(re.findall(r"[a-zà-ú]+", t.lower()))
        assert not words & set(VERDICT)


def test_comparator_no_good_bad_color_classes(client):
    html = client.post("/resultado", data=comparar()).get_data(as_text=True).lower()
    assert "positive" not in html and "negative" not in html and "good" not in html


# --- formulários GET ---

@pytest.mark.parametrize("path,needle", [
    ("/simulacao/pf", 'name="tipo_simulacao" value="pf"'),
    ("/simulacao/mei", 'name="tipo_simulacao" value="mei"'),
    ("/simulacao/simples", 'name="tipo_simulacao" value="simples"'),
    ("/simulacao/comparar", 'name="tipo_simulacao" value="comparar"'),
])
def test_forms_post_to_resultado(client, path, needle):
    html = client.get(path).get_data(as_text=True)
    assert 'method="post"' in html and 'action="/resultado"' in html and needle in html


def test_form_labels_are_friendly_not_enum_names(client):
    html = client.get("/simulacao/simples").get_data(as_text=True)
    assert "Desenvolvimento de software" in html and ">DESENVOLVIMENTO_SOFTWARE<" not in html
    html = client.get("/simulacao/mei").get_data(as_text=True)
    assert "Comércio / Indústria" in html and ">COMERCIO_INDUSTRIA<" not in html
    assert html.count("<label") >= 4


def test_every_form_input_has_a_label(client):
    for path in ("/simulacao/pf", "/simulacao/mei", "/simulacao/simples", "/simulacao/comparar"):
        html = client.get(path).get_data(as_text=True)
        for ident in re.findall(r'<(?:input|select)[^>]*\sid="([^"]+)"', html):
            assert f'for="{ident}"' in html, (path, ident)


# --- apresentação ---

def test_formatting_helpers_are_visual_only():
    v = D("1234.5")
    assert brl(v) == "R$ 1.234,50" and v == D("1234.5")
    assert brl(D("0.005")) == "R$ 0,01" and brl(None) == "—" and brl(D("-1234.567")) == "-R$ 1.234,57"
    assert pct(D("0.28")) == "28,00%" and pct(D("0.073"), 4) == "7,3000%"
    assert decimal_br(D("0.3")) == "0,30"
    assert humanize("Plano NORMAL: 1600.1000 e COMPATIVEL; Lei 15.270/2025") == "Plano normal: 1.600,10 e Dentro do limite; Lei 15.270/2025"


def test_adapter_errors_are_structured():
    with pytest.raises(SimulationInputError) as exc:
        build_scenario(pf(renda_mensal="x", plano_inss=""))
    assert set(exc.value.errors) == {"renda_mensal", "plano_inss"}


# --- camadas: nenhum parâmetro fiscal no frontend ---

FISCAL = re.compile(r"(?<![\d.,])(50000|81000|4800000|3600000|2428|1621|8475|0[.,]28|0[.,]11|0[.,]10)(?![\d])")


def _sources():
    files = [ROOT / "app.py", ROOT / "src/services/simulation_input_adapter.py", ROOT / "src/services/presentation.py"]
    files += sorted((ROOT / "templates").glob("*.html")) + sorted((ROOT / "static/js").glob("*.js"))
    return files


@pytest.mark.parametrize("path", _sources(), ids=lambda p: p.name)
def test_no_fiscal_parameters_in_presentation_layers(path):
    found = FISCAL.findall(path.read_text(encoding="utf-8"))
    assert not found, (path.name, found)


def test_js_has_no_tax_logic():
    code = re.sub(r"//.*", "", (ROOT / "static/js/app.js").read_text(encoding="utf-8")).lower()
    for word in ("aliquota", "alíquota", "irpf", "inss", "rbt12", "fator", "anexo", "das", "dividend", "limite"):
        assert not re.search(r"" + word + r"", code), word
    assert "* 12" not in code and "* 0." not in code


# --- Fase 4G: hardening ---

HOSTILE = ["", "   ", "--1", "1e10", "NaN", "-Infinity", "1,2,3", "-5", "9" * 40, "<script>", "OUTRO", "13", "0", "99999999999"]


def _bases():
    return {
        "pf": pf(),
        "mei": mei(),
        "simples": simples(meses="2"),
        "comparar": comparar(meses_desde_abertura="2", modo_apuracao="SEM_ESCRITURACAO", dividendos="0",
                             **{k: v for k, v in hist(1).items()}),
    }


def test_hostile_inputs_never_cause_500_or_traceback():
    app = create_app()
    app.config["PROPAGATE_EXCEPTIONS"] = True  # qualquer exceção não tratada falharia aqui
    client = app.test_client()
    failures = []
    for tipo, base in _bases().items():
        for field in (f for f in base if f != "tipo_simulacao"):
            for value in HOSTILE:
                r = client.post("/resultado", data={**base, field: value})
                body = r.get_data(as_text=True)
                if r.status_code not in (200, 400, 422) or "Traceback" in body:
                    failures.append((tipo, field, value, r.status_code))
            missing = {k: v for k, v in base.items() if k != field}
            r = client.post("/resultado", data=missing)
            if r.status_code not in (200, 400, 422):
                failures.append((tipo, field, "<ausente>", r.status_code))
    assert not failures, failures[:10]


def test_user_input_is_escaped_in_output(client):
    r = client.post("/resultado", data=pf(renda_mensal="<script>alert(1)</script>"))
    html = r.get_data(as_text=True)
    assert r.status_code == 422 and "<script>alert(1)" not in html and "&lt;script&gt;alert(1)" in html


def test_templates_never_mark_content_safe():
    for path in (ROOT / "templates").glob("*.html"):
        src = path.read_text(encoding="utf-8")
        assert "|safe" not in src.replace(" ", "") and "autoescape false" not in src, path.name


def test_zero_values_end_to_end(client):
    t = text(client.post("/resultado", data=pf(renda_mensal="0")))
    assert "Total de tributos" in t and "R$ 0,00" in t
    assert "R$ 86,05" in text(client.post("/resultado", data=mei(receita_acumulada="0", optante_simei="sim")))
    for meses in ("1", "2", "13"):
        r = client.post("/resultado", data=simples(meses=meses, receita_pa="0", receita_acumulada_ano="0"))
        assert r.status_code == 200
    mature = client.post("/resultado", data={**simples(meses="13", receita_pa="0", folha_pa="0", receita_acumulada_ano="0"),
                                              **hist(12, receita="0", folha="0")})
    assert mature.status_code == 200 and "DAS estimado R$ 0,00" in text(mature)
    t = text(client.post("/resultado", data=comparar(prolabore="0", dividendos="0", lucro_contabil_disponivel="0")))
    assert "INSS do pró-labore R$ 0,00" in t and "IRRF sobre dividendos R$ 0,00" in t


def test_warning_severity_comes_from_status_not_from_text(client):
    ok = client.post("/resultado", data=pf()).get_data(as_text=True)
    assert "alert-attention" in ok and "alert-unsupported" not in ok and "alert-info" not in ok
    bad = client.post("/resultado", data=mei(optante_simei="nao")).get_data(as_text=True)
    assert "alert-unsupported" in bad and "alert-attention" not in bad


def test_error_summary_links_point_to_existing_elements(client):
    cases = [pf(renda_mensal="x", plano_inss=""), mei(optante_simei="talvez", categoria=""),
             {**simples(meses="4"), "hist_receita_2": ""}, comparar(modo_apuracao="")]
    for data in cases:
        html = client.post("/resultado", data=data).get_data(as_text=True)
        summary = html.split("data-error-summary")[1].split("</div>")[0]
        targets = re.findall(r'href="#([^"]+)"', summary)
        assert targets
        for target in targets:
            assert f'id="{target}"' in html, target


def test_technical_field_names_do_not_leak_in_error_messages(client):
    data = simples(meses="4", meses_atividade_no_ano="2")  # meses_desde_abertura > meses de atividade no ano
    t = text(client.post("/resultado", data=data))
    assert "Meses de atividade no ano" in t
    for leaked in ("meses_atividade_no_ano", "meses_desde_abertura", "receita_acumulada_ano", "simples_input"):
        assert leaked not in t.split("Não foi possível simular")[1].split("Mês de apuração")[0]


def test_no_stale_pending_text_in_simulation_pages(client):
    for path in ("/", "/sobre", "/simulacao", "/simulacao/pf", "/simulacao/mei", "/simulacao/simples", "/simulacao/comparar"):
        t = text(client.get(path))
        assert "Pendente de validação" not in t and "aguardam validação" not in t, path
    assert "Pendente de validação" not in text(client.post("/resultado", data=comparar()))


def test_no_technical_enum_or_dataclass_repr_in_results(client):
    pages = [client.post("/resultado", data=d) for d in (pf(), mei(), simples(), comparar(), mei(optante_simei="nao"))]
    for r in pages:
        t = text(r)
        for token in ("COMPATIVEL", "EXCESSO_", "SERVICOS", "NORMAL", "CONSULTORIA", "Result(", "Decimal(", "SimulationStatus", "None"):
            assert token not in t, token
