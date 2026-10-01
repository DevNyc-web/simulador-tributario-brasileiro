"""Simulação guiada, limpeza de avisos, opções avançadas e página /reforma (Fase 5C)."""
import re
from decimal import Decimal as D
from pathlib import Path

import pytest

from app import create_app
from src.models.tax import AtividadeSimples, CategoriaMEI
from src.services.guided_simulation import (
    EnquadramentoGuiado,
    GuidedInput,
    StatusCenario,
    simulate_guided,
)
from src.services.simulation_input_adapter import SimulationInputError, build_guided_input
from src.tax_engine.prolabore_2026 import calculate_prolabore_2026
from src.models.tax import ProLaboreInput
from src.tax_rules import get_rule, parse_decimal

ROOT = Path(__file__).resolve().parents[1]
OLD_ROUTES = ["/", "/simulacao", "/simulacao/pf", "/simulacao/mei", "/simulacao/simples",
              "/simulacao/comparar", "/resultado", "/reforma", "/sobre", "/mapa-mental"]
VERDICT = ("melhor", "pior", "vantagem", "recomendado", "economiza", "ideal", "vencedor")
SM = parse_decimal(get_rule(2026, "TR-002").parametros["salario_minimo"])


@pytest.fixture
def client():
    return create_app().test_client()


def plain(markup: str) -> str:
    body = re.search(r"<main.*?</main>", markup, re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body.group(0) if body else markup))


def simples_form(**kw):
    return {"enquadramento": "SIMPLES", "atividade": "CONSULTORIA", "ticket_medio": "200,00",
            "clientes_mes": "100", **kw}


def mei_form(**kw):
    return {"enquadramento": "MEI", "categoria_mei": "SERVICOS", "ticket_medio": "100",
            "clientes_mes": "50", **kw}


def guided(client, form):
    return client.post("/simulacao-guiada", data=form)


# --- rotas e navegação ---

@pytest.mark.parametrize("path", OLD_ROUTES + ["/simulacao-guiada"])
def test_routes_return_200(client, path):
    assert client.get(path).status_code == 200


def test_both_modes_are_offered(client):
    page = client.get("/simulacao").get_data(as_text=True)
    assert 'href="/simulacao-guiada"' in page and "Simulação detalhada" in page
    assert 'action="/resultado"' not in page  # o seletor antigo continua (JS), sem perder o modo detalhado
    assert 'href="/simulacao/pf"' in page or "/simulacao/pf" in page
    home = client.get("/").get_data(as_text=True)
    assert 'href="/simulacao-guiada"' in home and 'href="/simulacao"' in home
    assert 'href="/simulacao-guiada"' in page  # também no menu


def test_nav_highlights_only_the_current_mode(client):
    nav = client.get("/simulacao-guiada").get_data(as_text=True)
    assert nav.count('aria-current="page"') == 1


def test_detailed_mode_still_works(client):
    r = client.post("/resultado", data={"tipo_simulacao": "pf", "renda_mensal": "8000", "plano_inss": "NORMAL"})
    assert r.status_code == 200 and "INSS" in plain(r.get_data(as_text=True))


def test_guided_form_fields(client):
    html = client.get("/simulacao-guiada").get_data(as_text=True)
    for needle in ('name="enquadramento"', 'name="ticket_medio"', 'name="clientes_mes"', 'name="categoria_mei"',
                   'name="atividade"', "Mostrar opções avançadas", 'name="prolabore"', 'name="optante_simei"'):
        assert needle in html, needle
    assert "Desenvolvimento de software" in html and "Comércio / Indústria" in html
    assert ">DESENVOLVIMENTO_SOFTWARE<" not in html
    for ident in re.findall(r'<(?:input|select)[^>]*\sid="([^"]+)"', html):
        assert f'for="{ident}"' in html, ident


# --- faturamento derivado e quadros ---

def test_revenue_is_ticket_times_clients(client):
    t = plain(guided(client, simples_form()).get_data(as_text=True))
    assert "R$ 20.000,00" in t
    assert simulate_guided(build_guided_input(simples_form())).faturamento_mensal == D("20000")
    assert simulate_guided(build_guided_input(mei_form(ticket_medio="99,90", clientes_mes="3"))).faturamento_mensal == D("299.70")


def test_presentation_has_seven_scenes_and_a_summary(client):
    html = guided(client, simples_form()).get_data(as_text=True)
    assert html.count("data-scene") == 7
    for needle in ("Seu cenário", "Faturamento bruto estimado", "Tributos considerados", "Sobra operacional estimada",
                   "Projeção em 12 meses", "Projeção operacional em 60 meses", "E se a equipe crescer?", "Resumo da simulação",
                   "Pular animação", "Comparação entre cenários"):
        assert needle in html, needle
    assert 'class="tick"' in html and "data-count=" in html and "data-final=" in html


def test_summary_has_charts_table_and_four_team_scenarios(client):
    html = guided(client, simples_form()).get_data(as_text=True)
    t = plain(html)
    for label in ("Sem funcionário", "+1 funcionário", "+2 funcionários", "+2 funcionários + gerente"):
        assert label in t
    assert html.count('class="g-chart"') == 3 and html.count("<tr>") == 5  # cabeçalho + 4 cenários
    assert 'class="g-stack"' in html and "Sobra operacional em 12 meses" in t and "Sobra operacional em 60 meses" in t


def test_projection_premises_are_explicit(client):
    t = plain(guided(client, simples_form()).get_data(as_text=True))
    for needle in ("Premissas e detalhes do cálculo", "Cálculo do motor", "Projeção", "Premissa operacional",
                   "aritméticas", "Mantêm constantes", "Não inclui cálculo trabalhista"):
        assert needle in t, needle


def test_at_most_one_notice_in_main_view(client):
    ok = guided(client, simples_form()).get_data(as_text=True)
    assert ok.count('class="g-notice"') == 0
    mei = guided(client, mei_form()).get_data(as_text=True)  # equipe não cabe no MEI
    assert mei.count('class="g-notice"') == 1


# --- serviço: cenários com equipe ---

def svc(form):
    return simulate_guided(build_guided_input(form))


def test_team_salaries_use_minimum_wage_from_rules():
    g = svc(simples_form())
    assert [c.salarios_mensais for c in g.cenarios] == [0, SM, SM * 2, SM * 4]
    assert g.salario_minimo == SM


def test_profit_identity_and_projections():
    g = svc(simples_form())
    for c in g.cenarios:
        assert c.ok
        assert c.sobra_mensal == c.faturamento - c.tributos_totais - c.custo_pessoal
        assert c.sobra_12m == c.sobra_mensal * 12 and c.sobra_60m == c.sobra_mensal * 60
    assert g.faturamento_12m == g.faturamento_mensal * 12 and g.faturamento_60m == g.faturamento_mensal * 60


def test_tax_values_come_from_the_engines():
    g = svc(simples_form(prolabore="3.000,00"))
    base = g.base
    pl = calculate_prolabore_2026(ProLaboreInput(2026, D("3000")))
    assert base.tributos_socio == pl.inss + pl.irpf
    assert g.prolabore_usado == D("3000")
    assert base.itens[0].rotulo == "DAS do Simples Nacional" and base.itens[0].valor == base.tributos_empresa


def test_default_prolabore_is_one_minimum_wage():
    assert svc(simples_form()).prolabore_usado == SM


def test_simples_team_changes_fator_r_annex():
    g = svc(simples_form())  # receita 20.000: a folha maior leva ao Anexo III no último cenário
    assert g.base.anexo == "Anexo V" and g.cenarios[3].anexo == "Anexo III"
    assert g.cenarios[3].aliquota_efetiva < g.base.aliquota_efetiva


def test_mei_one_employee_fits_more_do_not():
    g = svc(mei_form())
    assert [c.status for c in g.cenarios] == [StatusCenario.OK, StatusCenario.OK,
                                               StatusCenario.INCOMPATIVEL_MEI, StatusCenario.INCOMPATIVEL_MEI]
    assert "no máximo 1 empregado" in g.cenarios[2].motivo and "Simples Nacional" in g.cenarios[2].motivo
    assert g.cenarios[2].sobra_mensal is None and g.cenarios[2].sobra_12m is None
    assert g.aviso_principal and "MEI" in g.aviso_principal
    assert g.base.itens[0].rotulo == "DAS-MEI" and g.base.tributos_socio == 0


def test_mei_limit_parameters_come_from_rules_json():
    p = get_rule(2026, "TR-003").parametros
    assert p["maximo_empregados"] == "1"
    assert p["regra_remuneracao_empregado"] == "salario_minimo_ou_piso_da_categoria"
    assert "empregado_salario_maximo_em_salarios_minimos" not in p  # não transforma o texto legal em teto numérico


def test_mei_over_revenue_limit_is_not_pretended_to_fit(client):
    g = svc(mei_form(ticket_medio="300"))  # 15.000 por mês = 180.000 por ano
    assert all(c.status is StatusCenario.INCOMPATIVEL_MEI for c in g.cenarios)
    assert "acima do limite do MEI" in g.base.motivo
    t = plain(guided(client, mei_form(ticket_medio="300")).get_data(as_text=True))
    assert "Este cenário não pôde ser calculado" in t and "Simples Nacional" in t


def test_mei_not_optante_is_not_supported():
    g = svc(mei_form(optante_simei="nao"))
    assert all(c.status is StatusCenario.NAO_SUPORTADO for c in g.cenarios)


def test_simples_above_mvp_support_is_not_supported():
    g = svc(simples_form(ticket_medio="40000", clientes_mes="10"))  # 400.000 por mês: RBT12 acima do suporte
    assert all(not c.ok for c in g.cenarios) and g.aviso_principal


def test_months_of_activity_handled_and_zero_revenue_ok():
    assert svc(simples_form(meses_atividade_no_ano="6")).base.ok
    g = svc(simples_form(ticket_medio="0", clientes_mes="0", meses_atividade_no_ano="1"))
    assert g.faturamento_mensal == 0 and g.cenarios[0].status in (StatusCenario.OK, StatusCenario.NAO_SUPORTADO)
    assert svc(mei_form(ticket_medio="0")).base.tributos_empresa > 0  # DAS do MEI segue devido


def test_no_float_in_guided_result():
    g = svc(simples_form())
    for c in g.cenarios:
        for v in (c.faturamento, c.tributos_empresa, c.tributos_socio, c.custo_pessoal, c.sobra_mensal):
            assert isinstance(v, D)
    assert all(isinstance(b.pct, D) for b in g.barras_sobra_mensal)


# --- validação ---

@pytest.mark.parametrize("patch", [
    {"ticket_medio": "abc"}, {"ticket_medio": "-5"}, {"ticket_medio": ""}, {"clientes_mes": "-1"},
    {"clientes_mes": "1,5"}, {"clientes_mes": ""}, {"enquadramento": "OUTRO"}, {"enquadramento": ""},
    {"atividade": "NADA"}, {"meses_atividade_no_ano": "13"}, {"meses_atividade_no_ano": "0"}, {"prolabore": "x"},
])
def test_invalid_guided_inputs_are_controlled(client, patch):
    r = guided(client, simples_form(**patch))
    assert r.status_code == 422 and "Traceback" not in r.get_data(as_text=True)


def test_guided_requires_the_relevant_ramo(client):
    form = mei_form()
    form.pop("categoria_mei")
    assert guided(client, form).status_code == 422
    with pytest.raises(SimulationInputError):
        build_guided_input({"enquadramento": "SIMPLES", "ticket_medio": "1", "clientes_mes": "1"})


def test_guided_form_keeps_values_on_error(client):
    html = guided(client, simples_form(ticket_medio="abc")).get_data(as_text=True)
    assert 'value="abc"' in html and "Informe um valor válido" in html and 'aria-invalid="true"' in html


def test_guided_hostile_inputs_never_500():
    app = create_app()
    app.config["PROPAGATE_EXCEPTIONS"] = True
    c = app.test_client()
    hostile = ["", "  ", "--1", "1e10", "NaN", "Infinity", "9" * 40, "<script>", "OUTRO", "99999999999"]
    for base in (simples_form(), mei_form()):
        for field in base:
            for v in hostile:
                assert c.post("/simulacao-guiada", data={**base, field: v}).status_code in (200, 422)
            assert c.post("/simulacao-guiada", data={k: x for k, x in base.items() if k != field}).status_code in (200, 422)


def test_guided_output_is_escaped(client):
    html = guided(client, simples_form(ticket_medio="<script>alert(1)</script>")).get_data(as_text=True)
    assert "<script>alert(1)" not in html


# --- avisos recolhidos no modo detalhado ---

def detailed(client, **form):
    return client.post("/resultado", data=form).get_data(as_text=True)


def test_detailed_result_keeps_warnings_inside_accordion(client):
    html = detailed(client, tipo_simulacao="pf", renda_mensal="8000", plano_inss="NORMAL")
    assert "Premissas e detalhes do cálculo" in html and 'class="accordion"' in html
    assert html.count("key-notice") == 0  # nada de alerta solto em cenário normal
    assert html.index('class="accordion"') < html.index("Ferramenta educacional: não substitui")


def test_detailed_result_shows_single_key_notice_when_unsupported(client):
    html = detailed(client, tipo_simulacao="mei", receita_acumulada="1000", categoria="SERVICOS",
                    meses_atividade_no_ano="12", optante_simei="nao")
    assert html.count("key-notice") == 1
    assert "enquadrado no SIMEI" in html
    over = detailed(client, tipo_simulacao="mei", receita_acumulada="90000", categoria="SERVICOS",
                    meses_atividade_no_ano="12", optante_simei="sim")
    assert over.count("key-notice") == 1 and "DAS mensal" in plain(over)


# --- opções avançadas / modo estável no formulário detalhado ---

def test_advanced_options_are_collapsed(client):
    for path in ("/simulacao/simples", "/simulacao/comparar"):
        html = client.get(path).get_data(as_text=True)
        assert "Mostrar opções avançadas" in html and "data-advanced" in html and 'id="hist_modo"' in html
        assert re.search(r'id="hist_modo"[^>]*checked', html)


def test_stable_mode_fills_history_and_defaults(client):
    form = {"tipo_simulacao": "simples", "receita_pa": "20000", "folha_pa": "6000",
            "atividade": "CONSULTORIA", "hist_modo": "estavel"}
    t = plain(client.post("/resultado", data=form).get_data(as_text=True))
    assert "Anexo III" in t and "R$ 1.460,00" in t  # mesmo resultado do cenário com histórico explícito
    comp = {"tipo_simulacao": "comparar", "receita_mensal": "20000", "plano_inss": "NORMAL", "prolabore": "6000",
            "atividade": "CONSULTORIA", "dividendos": "3000", "modo_apuracao": "SEM_ESCRITURACAO",
            "hist_modo": "estavel"}
    assert "Diferenças numéricas" in plain(client.post("/resultado", data=comp).get_data(as_text=True))


def test_without_stable_mode_everything_is_still_required(client):
    form = {"tipo_simulacao": "simples", "receita_pa": "20000", "folha_pa": "6000", "atividade": "CONSULTORIA"}
    assert client.post("/resultado", data=form).status_code == 422


def test_stable_mode_explicit_values_take_precedence(client):
    form = {"tipo_simulacao": "simples", "receita_pa": "20000", "folha_pa": "1000",
            "atividade": "CONSULTORIA", "hist_modo": "estavel", "meses_atividade_no_ano": "2",
            "hist_receita_1": "20000", "hist_folha_1": "9000"}
    t = plain(client.post("/resultado", data=form).get_data(as_text=True))
    assert "Fator R 0,45" in t and "Anexo III" in t  # folha do mês anterior (9.000) informada manualmente


# --- /reforma ---

def test_reform_page_explains_the_strategy(client):
    html = client.get("/reforma").get_data(as_text=True)
    t = plain(html)
    for needle in ("Cálculo real implementado", "Conteúdo educacional / motor futuro", "versionadas por exercício",
                   "sem reescrever toda a aplicação", "Motor separado da interface", "Rastreabilidade",
                   "Evolução incremental", "Como o simulador acompanha mudanças?", "Linha do tempo da transição"):
        assert needle in t, needle
    assert "PENDENTE DE VALIDAÇÃO" not in html


def test_reform_versioning_flow_is_explained(client):
    t = plain(client.get("/reforma").get_data(as_text=True))
    order = ["Lei ou regra muda", "Pesquisa e validação", "rules.json do exercício", "Motor daquele ano", "Testes", "Interface"]
    positions = [t.index(x) for x in order]
    assert positions == sorted(positions)
    assert "separadas da interface e versionadas por exercício" in t


def test_reform_timeline_has_all_stages_with_official_schedule(client):
    html = client.get("/reforma").get_data(as_text=True)
    t = plain(html)
    for slug in ("2026", "2027-2028", "2029", "2030", "2031", "2032", "2033"):
        assert f'data-year="{slug}"' in html and f'data-panel="{slug}"' in html, slug
    assert html.count("data-panel=") == 7
    for needle in ("CBS de 0,9% e IBS de 0,1%", "PIS e Cofins", "Imposto Seletivo", "Proporção da transição: IBS 10% | ICMS/ISS 90%",
                   "Proporção da transição: IBS 20% | ICMS/ISS 80%", "Proporção da transição: IBS 30% | ICMS/ISS 70%",
                   "Proporção da transição: IBS 40% | ICMS/ISS 60%", "redução de 0,1 ponto percentual (não é uma alíquota de 0,1%)",
                   "ICMS e ISS extintos", "Resoluções CGSN nº 190 e nº 191/2026", "1º/1/2027"):
        assert needle in t, needle
    assert "Receita Federal" in t and "consultada em 30/09/2026" in t


def test_reform_transition_percentages_are_proportions_not_nominal_rates(client):
    html = client.get("/reforma").get_data(as_text=True)
    note = "não uma alíquota nominal definitiva do IBS"
    for slug in ("2029", "2030", "2031", "2032"):
        panel = html.split(f'data-panel="{slug}"')[1].split("</article>")[0]
        assert "Proporção da transição" in panel and note in plain(panel), slug
    assert "alíquota do IBS = " not in html and "IBS = 10%" not in html


def test_reform_badges_separate_implemented_from_educational(client):
    html = client.get("/reforma").get_data(as_text=True)
    assert html.count("Cálculo implementado no MVP") == 1
    panel_2026 = html.split('data-panel="2026"')[1].split("</article>")[0]
    assert "Cálculo implementado no MVP" in panel_2026
    for slug in ("2027-2028", "2029", "2030", "2031", "2032", "2033"):
        panel = html.split(f'data-panel="{slug}"')[1].split("</article>")[0]
        assert "Conteúdo educacional / motor futuro" in panel and "Cálculo implementado no MVP" not in panel, slug
        assert "Ainda não" in panel and "o sistema não calcula este exercício" in panel, slug


def test_reform_page_uses_real_rule_counts(client):
    t = plain(client.get("/reforma").get_data(as_text=True))
    assert re.search(r"2026 Cálculo implementado no MVP.{0,1200}Regras no arquivo do exercício 11 .{0,60}testadas 11", t)
    assert t.count("Cálculo disponível no simulador Ainda não") == 6 and t.count("Cálculo disponível no simulador Sim") == 1
    assert "Regras no arquivo do exercício 0 " in t


def test_reform_does_not_present_future_years_as_calculated(client):
    t = plain(client.get("/reforma").get_data(as_text=True))
    assert "não calcula CBS nem IBS" in t and "só calcula tributos de 2026" in t


# --- Fase 5C.1: semântica da sobra, projeções e regra do empregado MEI ---

def test_guided_does_not_call_the_operational_remainder_net_profit(client):
    for form in (simples_form(), mei_form(), mei_form(ticket_medio="300")):
        t = plain(guided(client, form).get_data(as_text=True)).lower()
        for forbidden in ("lucro líquido", "líquido do empresário", "sobra para o empresário", "lucro em 1 ano", "lucro em 5 anos"):
            assert forbidden not in t, forbidden
    t = plain(guided(client, simples_form()).get_data(as_text=True))
    assert "Sobra operacional estimada" in t and "Valor potencialmente disponível antes da distribuição" in t


def test_sixty_month_projection_states_constant_premises_and_links_to_reform(client):
    html = guided(client, simples_form()).get_data(as_text=True)
    ressalva = "Projeção operacional com premissas constantes. As regras tributárias futuras podem mudar durante o período."
    assert html.count(ressalva) >= 2
    assert html.count("Veja a transição tributária 2026–2033") >= 2 and 'href="/reforma"' in html
    scene6 = html.split('id="gs6"')[1].split("</section>")[0]
    assert "premissas constantes" in scene6 and "/reforma" in scene6
    assert "não representam cálculo tributário definitivo" in plain(html).lower()


def test_salaries_are_an_operational_premise_not_a_legal_rule(client):
    g = svc(simples_form())
    texts = " ".join(t for _, t in g.premissas)
    assert "Premissa operacional da simulação (não é regra legal de remuneração)" in texts
    assert "funcionário = 1 salário" in texts and "gerente = 2 salários mínimos" in texts
    assert [c.salarios_mensais for c in g.cenarios] == [0, SM, SM * 2, SM * 4]  # a demonstração continua usando 1 SM
    page = plain(guided(client, simples_form()).get_data(as_text=True))
    assert "não é regra legal de remuneração" in page and "cálculo trabalhista completo" in page


def test_mei_rule_is_quantity_limit_with_min_wage_or_category_floor():
    g = svc(mei_form())
    motivo = g.cenarios[2].motivo
    assert "no máximo 1 empregado" in motivo and "salário" not in motivo  # sem teto salarial universal inventado
    texts = " ".join(t for _, t in g.premissas)
    assert "um salário mínimo ou o piso salarial da categoria" in texts
    assert "adota 1 salário mínimo como hipótese do cenário" in texts
    assert "salário de até" not in texts.lower()


def test_mei_one_employee_with_minimum_wage_still_fits():
    g = svc(mei_form())
    assert g.cenarios[1].ok and g.cenarios[1].salarios_mensais == SM


# --- camadas ---

GJS = [ROOT / "static/js/guided-simulation.js", ROOT / "static/js/guided-form.js", ROOT / "static/js/reform.js"]


@pytest.mark.parametrize("path", GJS, ids=lambda p: p.name)
def test_new_js_has_no_tax_logic_or_network(path):
    code = re.sub(r"//.*", "", path.read_text(encoding="utf-8")).lower()
    for word in ("aliquota", "alíquota", "irpf", "inss", "rbt12", "fator", "anexo", "imposto", "dividend", "simples", "mei"):
        assert not re.search(r"\b" + word + r"\b", code), word
    assert "fetch(" not in code and "xmlhttprequest" not in code and "import " not in code
    assert not re.search(r"(?<![\d.,])(50000|81000|4800000|3600000|2428|1621|8475|0[.,]28|0[.,]11|0[.,]10)(?![\d])", code)


def test_guided_js_respects_reduced_motion_and_offers_skip():
    js = GJS[0].read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in js and "data-skip" in js and "requestAnimationFrame" in js
    css = (ROOT / "static/css/guided-simulation.css").read_text(encoding="utf-8")
    assert "prefers-reduced-motion: reduce" in css and "http" not in css


def test_guided_pages_have_no_verdict_words(client):
    pages = [guided(client, simples_form()).get_data(as_text=True), guided(client, mei_form()).get_data(as_text=True),
             client.get("/simulacao-guiada").get_data(as_text=True), client.get("/reforma").get_data(as_text=True)]
    for html in pages:
        assert not set(re.findall(r"[a-zà-ú]+", plain(html).lower())) & set(VERDICT)


def test_guided_service_layers_do_not_hardcode_fiscal_numbers():
    src = (ROOT / "src/services/guided_simulation.py").read_text(encoding="utf-8")
    assert not re.search(r"(?<![\d.,])(50000|81000|4800000|3600000|2428|1621|8475|0[.,]28|0[.,]11|0[.,]10)(?![\d])", src)
