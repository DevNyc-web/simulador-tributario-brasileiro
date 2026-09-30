"""Testes do comparador PF x PJ 2026 (composição dos motores; sem recomendação)."""
from dataclasses import fields
from decimal import Decimal as D

import pytest

from src.models.tax import (
    AtividadeSimples,
    ComparatorSimulationInput,
    DividendosInput,
    ModoApuracaoLucro,
    PFSimulationInput,
    PlanoINSS,
    SimplesSimulationInput,
    SimulationStatus,
)
from src.services import simulate_transition
from src.tax_engine import calculate
from src.tax_engine.comparator_2026 import calculate_comparator_2026, compare_pf_pj_2026
from src.tax_engine.pf_2026 import calculate_pf_2026
from src.tax_engine.prolabore_2026 import calculate_prolabore_2026
from src.tax_engine.simples_2026 import calculate_simples_2026
from src.models.tax import ProLaboreInput
from src.tax_rules import load_year_rules

SEM, COM = ModoApuracaoLucro.SEM_ESCRITURACAO, ModoApuracaoLucro.COM_ESCRITURACAO
FORBIDDEN = ("melhor", "pior", "recomend", "vencedor", "compensa", "economia ideal", "vale a pena")


def ds(v, n=12):
    return tuple(D(v) for _ in range(n))


def build(receita="20000", prolabore="6000", folhas="6000", dividendos="3000", modo=COM, lucro="10000",
          renda_anual=None, atividade=AtividadeSimples.CONSULTORIA, anteriores=None, acumulada=None):
    rec = D(receita)
    simples = SimplesSimulationInput(
        ano=2026, receita_pa=rec, receitas_anteriores=anteriores or ds(receita),
        folha_pa=D(prolabore), folhas_anteriores=ds(folhas), receita_acumulada_ano=acumulada or rec,
        meses_desde_abertura=24, meses_atividade_no_ano=12, atividade=atividade,
    )
    div = DividendosInput(2026, D(dividendos), modo, D(lucro) if modo is COM else None, renda_anual)
    return ComparatorSimulationInput(PFSimulationInput(2026, rec, PlanoINSS.NORMAL), simples, D(prolabore), div)


def test_a_pf_vs_pj_anexo_iii_reuses_engines():
    e = build()  # fator 0.30 -> Anexo III, 2ª faixa: DAS 1460
    r = compare_pf_pj_2026(e)
    assert r.status == SimulationStatus.OK
    pf = calculate_pf_2026(e.pf_input)
    assert r.pf.total_tributos == pf.total_tributos and r.pf.liquido_pessoal == pf.liquido_estimado
    assert r.pf.inss == pf.itens[0].valor and r.pf.irpf == pf.itens[1].valor
    assert r.pj.das == calculate_simples_2026(e.simples_input).total_tributos == D("20000") * D("0.073")
    pl = calculate_prolabore_2026(ProLaboreInput(2026, D("6000")))
    assert (r.pj.inss_prolabore, r.pj.irpf_prolabore, r.pj.prolabore_liquido) == (pl.inss, pl.irpf, pl.liquido)


def test_b_pf_vs_pj_anexo_v():
    r = compare_pf_pj_2026(build(prolabore="1000", folhas="1000", dividendos="3000"))  # fator 0.05 -> V
    assert r.status == SimulationStatus.OK
    assert r.pj.das == D("20000") * ((D("240000") * D("0.18") - D("4500")) / D("240000"))


def test_c_dividends_up_to_50k_no_irrf():
    r = compare_pf_pj_2026(build(dividendos="50000", lucro="50000"))
    assert r.pj.irrf_dividendos == 0 and r.pj.dividendos_liquidos == D("50000")


def test_d_dividends_above_50k_irrf_on_total():
    r = compare_pf_pj_2026(build(dividendos="60000", lucro="60000"))
    assert r.pj.irrf_dividendos == D("6000.00") and r.pj.dividendos_liquidos == D("54000.00")


def test_totals_and_differences_are_arithmetic():
    r = compare_pf_pj_2026(build())
    pj = r.pj
    assert pj.total_tributos == pj.das + pj.inss_prolabore + pj.irpf_prolabore + pj.irrf_dividendos
    assert pj.recebido_pela_pf == pj.prolabore_liquido + pj.dividendos_liquidos
    assert r.diferenca_tributos == pj.total_tributos - r.pf.total_tributos
    assert r.diferenca_recebimento_pessoal == pj.recebido_pela_pf - r.pf.liquido_pessoal
    # sem CPP patronal de 20%: INSS do PJ só o do segurado (11%)
    assert pj.inss_prolabore == D("6000") * D("0.11")


def test_differences_can_be_negative_zero_or_positive_without_verdict():
    r = compare_pf_pj_2026(build())
    assert isinstance(r.diferenca_tributos, D)
    assert not hasattr(r, "melhor") and "recomend" not in " ".join(r.warnings).replace("não recomenda", "")


def test_e_different_revenues_error():
    e = build()
    with pytest.raises(ValueError):
        ComparatorSimulationInput(PFSimulationInput(2026, D("19999"), PlanoINSS.NORMAL),
                                  e.simples_input, e.prolabore, e.dividendos)


def test_f_folha_pa_must_equal_prolabore():
    e = build()
    with pytest.raises(ValueError):
        ComparatorSimulationInput(e.pf_input, e.simples_input, D("5000"), e.dividendos)


def test_input_type_and_year_validation():
    e = build()
    with pytest.raises(TypeError):
        ComparatorSimulationInput(e.pf_input, e.simples_input, 6000.0, e.dividendos)
    with pytest.raises(TypeError):
        ComparatorSimulationInput("x", e.simples_input, e.prolabore, e.dividendos)
    with pytest.raises(ValueError):
        ComparatorSimulationInput(e.pf_input, e.simples_input, e.prolabore, DividendosInput(2027, D("1"), COM, D("1")))


def test_g_simples_not_supported_no_invented_result():
    e = build(receita="300001", prolabore="6000", anteriores=ds("300001"), dividendos="0")
    r = compare_pf_pj_2026(e)
    assert r.status == SimulationStatus.NAO_SUPORTADO
    assert r.pf is None and r.pj is None and r.diferenca_tributos is None
    sr = calculate_comparator_2026(e)
    assert sr.status == SimulationStatus.NAO_SUPORTADO and not sr.itens and sr.total_tributos is None


def test_simples_incompatible_propagates():
    e = build(acumulada=D("4800000.01"))
    assert compare_pf_pj_2026(e).status == SimulationStatus.INCOMPATIVEL


def test_dividends_not_supported_blocks_comparison():
    e = build(modo=SEM, dividendos="6341.61")  # 1 centavo acima do limite sem escrituração
    r = compare_pf_pj_2026(e)
    assert r.status == SimulationStatus.NAO_SUPORTADO and r.pj is None
    ok = compare_pf_pj_2026(build(modo=SEM, dividendos="6341.60"))
    assert ok.status == SimulationStatus.OK


def test_dividends_above_available_profit_incompatible():
    assert compare_pf_pj_2026(build(dividendos="10001", lucro="10000")).status == SimulationStatus.INCOMPATIVEL


def test_h_no_verdict_or_recommendation_anywhere():
    res = calculate_comparator_2026(build())
    text = " ".join(
        [*res.warnings, *(e.titulo + " " + e.descricao for e in res.explicacoes), *(i.descricao for i in res.itens)]
    ).lower().replace("não recomenda estrutura alguma", "")
    assert not any(w in text for w in FORBIDDEN)
    names = {f.name for cls in (type(compare_pf_pj_2026(build())),) for f in fields(cls)}
    assert not names & {"melhor", "vencedor", "recomendado", "economia"}


def test_received_by_pf_is_not_called_economic_net():
    res = calculate_comparator_2026(build())
    assert any("não é lucro líquido nem líquido econômico" in w for w in res.warnings)
    assert any(e.titulo == "Valor recebido pela pessoa física" for e in res.explicacoes)


def test_health_activity_warning_and_spend_over_revenue_warning():
    r = compare_pf_pj_2026(build(atividade=AtividadeSimples.MEDICINA, dividendos="14000", lucro="14000"))
    assert any("atendimento profissional comum" in w for w in r.warnings)
    assert any("somam mais que o faturamento" in w for w in r.warnings)


def test_high_income_warning_flows_through():
    r = compare_pf_pj_2026(build(renda_anual=D("600000.01")))
    assert any("tributação mínima anual" in w for w in r.warnings)


def test_calculator_dispatch_comparar():
    e = build()
    res = simulate_transition({"tipo_simulacao": "comparar", "entrada": e})
    assert res[0].status == SimulationStatus.OK and res[0].tipo_simulacao == "comparar"
    assert {i.codigo for i in res[0].itens} >= {"PF_TOTAL_TRIBUTOS", "PJ_TOTAL_TRIBUTOS", "PJ_DAS"}
    assert all(r.status == SimulationStatus.PENDENTE for r in res[1:])
    assert calculate(load_year_rules(2026), {"tipo_simulacao": "comparar"}).status == SimulationStatus.PENDENTE


def test_no_float_in_comparison():
    r = compare_pf_pj_2026(build())
    for part in (r.pf, r.pj):
        assert all(isinstance(getattr(part, f.name), D) for f in fields(part))
