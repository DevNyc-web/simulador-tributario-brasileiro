"""Testes do motor Simples Nacional 2026 (TR-005 a TR-009).

Valores esperados: docs/research/simples-2026-research.md (F-23/F-34, F-32, F-36, F-38).
"""
from decimal import Decimal as D

import pytest

from src.models.tax import (
    AnexoSimples,
    AtividadeSimples,
    SimplesSimulationInput,
    SimulationStatus,
    StatusSimples,
)
from src.services import simulate_transition
from src.tax_engine import calculate
from src.tax_engine.simples_2026 import (
    FatorRIndefinidoError,
    calculate_effective_rate,
    calculate_fator_r_2026,
    calculate_rbt12_2026,
    calculate_rbt12p_2026,
    calculate_simples_2026,
    calculate_simples_limit_2026,
    select_tax_bracket,
)
from src.tax_rules import get_rule, load_year_rules

III = get_rule(2026, "TR-006").parametros["faixas"]
V = get_rule(2026, "TR-007").parametros["faixas"]
CENT = D("0.01")

# (RBT12, faixa esperada) — fronteiras inclusivas no limite superior
FRONTEIRAS = [
    ("0", 1), ("180000.00", 1), ("180000.01", 2), ("360000.00", 2), ("360000.01", 3),
    ("720000.00", 3), ("720000.01", 4), ("1800000.00", 4), ("1800000.01", 5),
    ("3600000.00", 5), ("3600000.01", 6), ("4800000.00", 6),
]


def ds(*vals):
    return tuple(D(v) for v in vals)


def entrada(**kw):
    base = dict(
        ano=2026, receita_pa=D("20000"), receitas_anteriores=ds(*["20000"] * 12),
        folha_pa=D("6000"), folhas_anteriores=ds(*["6000"] * 12),
        receita_acumulada_ano=D("100000"), meses_desde_abertura=24,
        meses_atividade_no_ano=12, atividade=AtividadeSimples.CONSULTORIA,
    )
    base.update(kw)
    return SimplesSimulationInput(**base)


# --- Tabelas (TR-006/TR-007) ---

@pytest.mark.parametrize("tabela", [III, V], ids=["III", "V"])
@pytest.mark.parametrize("rbt,faixa", FRONTEIRAS)
def test_bracket_boundaries(tabela, rbt, faixa):
    assert select_tax_bracket(D(rbt), tabela).numero == faixa


@pytest.mark.parametrize("tabela", [III, V], ids=["III", "V"])
def test_bracket_above_table_raises(tabela):
    with pytest.raises(ValueError):
        select_tax_bracket(D("4800000.01"), tabela)


def test_tables_match_research():
    f = select_tax_bracket(D("500000"), III)
    assert (f.aliquota_nominal, f.parcela_deduzir) == (D("0.135"), D("17640.00"))
    f = select_tax_bracket(D("500000"), V)
    assert (f.aliquota_nominal, f.parcela_deduzir) == (D("0.195"), D("9900.00"))
    f = select_tax_bracket(D("4000000"), III)
    assert (f.aliquota_nominal, f.parcela_deduzir) == (D("0.33"), D("648000.00"))


# --- RBT12 (empresa madura) ---

def test_rbt12_sum_of_twelve_previous_months():
    assert calculate_rbt12_2026(ds(*range(1, 13))) == 78


def test_rbt12_excludes_current_pa():
    e = entrada(receita_pa=D("999999"), receita_acumulada_ano=D("999999"))
    assert calculate_simples_2026(e).status == SimulationStatus.OK
    assert calculate_rbt12_2026(e.receitas_anteriores) == D("240000")


def test_rbt12_uses_only_last_twelve_of_longer_history():
    assert calculate_rbt12_2026(ds("1000000", *["1"] * 12)) == 12


def test_inconsistent_history_raises():
    with pytest.raises(ValueError):
        entrada(receitas_anteriores=ds(*["1"] * 11))  # 13+ meses exige 12
    with pytest.raises(ValueError):
        entrada(meses_desde_abertura=4, receitas_anteriores=ds("1", "1"), folhas_anteriores=ds("1", "1"))
    with pytest.raises(ValueError):
        entrada(folhas_anteriores=ds(*["1"] * 11))
    with pytest.raises(ValueError):
        entrada(meses_desde_abertura=3, meses_atividade_no_ano=2,
                receitas_anteriores=ds("1", "1"), folhas_anteriores=ds("1", "1"))
    with pytest.raises(ValueError):
        entrada(receita_acumulada_ano=D("1"))


def test_input_validation_types():
    with pytest.raises(TypeError):
        entrada(receita_pa=1000.0)
    with pytest.raises(TypeError):
        entrada(receitas_anteriores=[D("1")] * 12)
    with pytest.raises(ValueError):
        entrada(folha_pa=D("-1"))
    with pytest.raises(ValueError):
        entrada(meses_desde_abertura=0)
    with pytest.raises(ValueError):
        entrada(meses_atividade_no_ano=13)
    with pytest.raises(TypeError):
        entrada(atividade="CONSULTORIA")


# --- RBT12p ---

def test_rbt12p_first_month():
    assert calculate_rbt12p_2026(D("10000"), ()) == D("120000")


def test_rbt12p_second_month_uses_previous_month_only():
    assert calculate_rbt12p_2026(D("99999"), ds("10000")) == D("120000")


def test_rbt12p_fourth_month_average_of_three_previous():
    assert calculate_rbt12p_2026(D("99999"), ds("10000", "20000", "30000")) == D("240000")


def test_rbt12p_twelfth_month_average_of_eleven_previous():
    assert calculate_rbt12p_2026(D("99999"), ds(*range(1, 12))) == D("66") / 11 * 12


# --- Fator R ---

@pytest.mark.parametrize("folha,anexo", [("27", AnexoSimples.V), ("28", AnexoSimples.III), ("29", AnexoSimples.III)])
def test_fator_r_cut(folha, anexo):
    r = calculate_fator_r_2026(D(folha), D("100"), primeiro_mes=False)
    assert r.fator == D(folha) / 100 and r.anexo is anexo


def test_fator_r_two_decimals_truncated_not_rounded():
    r = calculate_fator_r_2026(D("2774"), D("10000"), primeiro_mes=False)
    assert r.fator == D("0.27") and r.anexo is AnexoSimples.V
    r = calculate_fator_r_2026(D("2799"), D("10000"), primeiro_mes=False)
    assert r.fator == D("0.27") and r.anexo is AnexoSimples.V
    assert calculate_fator_r_2026(D("2800"), D("10000"), primeiro_mes=False).fator == D("0.28")
    assert calculate_fator_r_2026(D("29999"), D("100000"), primeiro_mes=False).fator == D("0.29")


@pytest.mark.parametrize("primeiro_mes,folha,receita,fator", [
    (True, "100", "0", "0.28"),
    (True, "0", "100", "0.01"),
    (False, "100", "0", "0.28"),
    (False, "0", "100", "0.01"),
    (False, "0", "0", "0.01"),
])
def test_fator_r_zero_cases(primeiro_mes, folha, receita, fator):
    assert calculate_fator_r_2026(D(folha), D(receita), primeiro_mes=primeiro_mes).fator == D(fator)


def test_fator_r_first_month_both_zero_undefined():
    with pytest.raises(FatorRIndefinidoError):
        calculate_fator_r_2026(D(0), D(0), primeiro_mes=True)
    e = entrada(meses_desde_abertura=1, receitas_anteriores=(), folhas_anteriores=(),
                receita_pa=D(0), folha_pa=D(0), receita_acumulada_ano=D(0), meses_atividade_no_ano=12)
    assert calculate_simples_2026(e).status == SimulationStatus.NAO_SUPORTADO


def test_fator_r_first_month_uses_pa_values():
    e = entrada(meses_desde_abertura=1, receitas_anteriores=(), folhas_anteriores=(),
                receita_pa=D("10000"), folha_pa=D("3000"), receita_acumulada_ano=D("10000"))
    r = calculate_simples_2026(e)
    assert r.status == SimulationStatus.OK
    assert any("Anexo III" in x.descricao for x in r.explicacoes if x.titulo == "Fator R")


def test_fator_r_months_2_to_12_uses_accumulated_previous_not_pa_nor_rbt12p():
    # anteriores: receita 10000+20000=30000, folha 9000 -> 0.30 (III); PA (folha 0) ignorado
    e = entrada(meses_desde_abertura=3, receitas_anteriores=ds("10000", "20000"),
                folhas_anteriores=ds("3000", "6000"), receita_pa=D("50000"), folha_pa=D("0"),
                receita_acumulada_ano=D("80000"), meses_atividade_no_ano=10)
    r = calculate_simples_2026(e)
    fator = next(x for x in r.explicacoes if x.titulo == "Fator R")
    assert "Fator R = 0.30" in fator.descricao and "Anexo III" in fator.descricao
    # RBT12p = média(10000,20000) x 12 = 180000 (1ª faixa), diferente do denominador do fator
    assert "180000" in next(x for x in r.explicacoes if x.titulo == "Receita bruta de 12 meses").descricao


def test_fator_r_mature_uses_twelve_previous_months():
    e = entrada(receitas_anteriores=ds(*["10000"] * 12), folhas_anteriores=ds(*["2000"] * 12))
    r = calculate_simples_2026(e)
    assert "Fator R = 0.20" in next(x for x in r.explicacoes if x.titulo == "Fator R").descricao
    assert r.explicacoes[3].titulo == "Faixa do Anexo V"


@pytest.mark.parametrize("atividade", list(AtividadeSimples))
def test_all_nine_activities_use_fator_r(atividade):
    iii = calculate_simples_2026(entrada(atividade=atividade, folhas_anteriores=ds(*["6000"] * 12)))
    v = calculate_simples_2026(entrada(atividade=atividade, folhas_anteriores=ds(*["1000"] * 12)))
    assert iii.explicacoes[3].titulo == "Faixa do Anexo III"
    assert v.explicacoes[3].titulo == "Faixa do Anexo V"


def test_activity_enum_matches_rules_json():
    assert {a.value for a in AtividadeSimples} == set(get_rule(2026, "TR-009").parametros["atividades"])
    assert len(AtividadeSimples) == 9


# --- Alíquota efetiva ---

def test_effective_rate_anexo_iii_intermediate():
    rbt = D("500000")
    f = select_tax_bracket(rbt, III)
    assert calculate_effective_rate(rbt, f).aliquota == (rbt * D("0.135") - D("17640")) / rbt


def test_effective_rate_anexo_v_intermediate():
    rbt = D("500000")
    f = select_tax_bracket(rbt, V)
    assert calculate_effective_rate(rbt, f).aliquota == (rbt * D("0.195") - D("9900")) / rbt


def test_effective_rate_zero_rbt_uses_substitute():
    f = select_tax_bracket(D(0), III)
    r = calculate_effective_rate(D(0), f)
    assert r.base_rbt == 1 and r.aliquota == D("0.06")


@pytest.mark.parametrize("tabela", [III, V], ids=["III", "V"])
@pytest.mark.parametrize("rbt,_", FRONTEIRAS)
def test_effective_rate_non_negative_and_below_nominal(tabela, rbt, _):
    f = select_tax_bracket(D(rbt), tabela)
    a = calculate_effective_rate(D(rbt), f).aliquota
    assert 0 <= a <= f.aliquota_nominal


def test_das_equals_receita_times_effective_rate_unrounded():
    r = calculate_simples_2026(entrada(receita_pa=D("12345.67")))
    item = r.itens[0]
    assert item.codigo == "DAS_SIMPLIFICADO" and item.base_calculo == D("12345.67")
    assert item.valor == D("12345.67") * item.aliquota == r.total_tributos
    assert isinstance(item.valor, D) and isinstance(item.aliquota, D)


# --- Limite (TR-005) ---

@pytest.mark.parametrize("receita,status", [
    ("4800000.00", StatusSimples.COMPATIVEL), ("4800000.01", StatusSimples.FORA_LIMITE_SIMPLES),
])
def test_general_limit_existing_company(receita, status):
    assert calculate_simples_limit_2026(D(receita), 12, D("100000")).status is status


@pytest.mark.parametrize("meses", [1, 6, 11])
def test_proportional_limit_opening_year(meses):
    limite = D("400000") * meses
    assert calculate_simples_limit_2026(limite, meses, D(0)).limite_aplicavel == limite
    assert calculate_simples_limit_2026(limite, meses, D(0)).status is StatusSimples.COMPATIVEL
    assert calculate_simples_limit_2026(limite + CENT, meses, D(0)).status is StatusSimples.FORA_LIMITE_SIMPLES


def test_mvp_sublimite_boundary():
    assert calculate_simples_limit_2026(D(0), 12, D("3600000.00")).status is StatusSimples.COMPATIVEL
    assert calculate_simples_limit_2026(D(0), 12, D("3600000.01")).status is StatusSimples.ACIMA_SUBLIMITE_MVP
    assert calculate_simples_limit_2026(D(0), 12, D("4800000.01")).status is StatusSimples.FORA_LIMITE_SIMPLES


def test_limit_is_independent_of_bracket_rbt():
    # RBT12 baixa, mas receita do ano acima do limite geral -> fora
    assert calculate_simples_limit_2026(D("5000000"), 12, D("100000")).status is StatusSimples.FORA_LIMITE_SIMPLES


# --- Integrados ---

def test_integrated_anexo_iii():
    r = calculate_simples_2026(entrada(folhas_anteriores=ds(*["6000"] * 12)))  # 0.30
    rbt = D("240000")
    aliq = (rbt * D("0.112") - D("9360")) / rbt
    assert r.status == SimulationStatus.OK and r.itens[0].aliquota == aliq
    assert r.itens[0].valor == D("20000") * aliq


def test_integrated_anexo_v():
    r = calculate_simples_2026(entrada(folhas_anteriores=ds(*["1000"] * 12)))  # 0.05
    rbt = D("240000")
    aliq = (rbt * D("0.18") - D("4500")) / rbt
    assert r.itens[0].aliquota == aliq and r.total_tributos == D("20000") * aliq
    assert {e.rule_id for e in r.explicacoes} >= {"TR-005", "TR-007", "TR-008", "TR-009"}


def test_integrated_new_company_rbt12p_fator_anexo_aliquota_das():
    e = entrada(meses_desde_abertura=4, receitas_anteriores=ds("10000", "20000", "30000"),
                folhas_anteriores=ds("3000", "6000", "9000"), receita_pa=D("25000"), folha_pa=D("1"),
                receita_acumulada_ano=D("85000"), meses_atividade_no_ano=9)
    r = calculate_simples_2026(e)
    rbt12p = D("240000")  # (10000+20000+30000)/3 x 12
    aliq = (rbt12p * D("0.112") - D("9360")) / rbt12p  # fator 18000/60000 = 0.30 -> III
    assert r.status == SimulationStatus.OK
    assert r.itens[0].aliquota == aliq and r.itens[0].valor == D("25000") * aliq
    assert "RBT12p" in r.explicacoes[1].descricao


def test_integrated_above_sublimite_not_supported_but_table_selects_band_6():
    e = entrada(receitas_anteriores=ds(*["300001"] * 12), receita_acumulada_ano=D("300001"))
    assert sum(e.receitas_anteriores) > D("3600000")
    assert select_tax_bracket(sum(e.receitas_anteriores), III).numero == 6
    r = calculate_simples_2026(e)
    assert r.status == SimulationStatus.NAO_SUPORTADO and r.total_tributos is None and not r.itens
    assert "ISS" in r.warnings[0] and "permanecer no Simples" in r.warnings[0]


def test_integrated_limit_exceeded_incompatible():
    over_year = calculate_simples_2026(entrada(receita_acumulada_ano=D("4800000.01")))
    assert over_year.status == SimulationStatus.INCOMPATIVEL and over_year.total_tributos is None
    over_rbt = calculate_simples_2026(entrada(receitas_anteriores=ds(*["400001"] * 12)))
    assert over_rbt.status == SimulationStatus.INCOMPATIVEL


def test_not_optante_not_supported():
    assert calculate_simples_2026(entrada(optante_simples=False)).status == SimulationStatus.NAO_SUPORTADO


def test_calculator_dispatch():
    scenario = {"tipo_simulacao": "simples", "entrada": entrada()}
    res = simulate_transition(scenario)
    assert res[0].status == SimulationStatus.OK and res[0].tipo_simulacao == "simples"
    assert all(r.status == SimulationStatus.PENDENTE for r in res[1:])
    assert calculate(load_year_rules(2026), {"tipo_simulacao": "simples"}).status == SimulationStatus.PENDENTE
    with pytest.raises(ValueError):
        calculate_simples_2026(entrada(ano=2027))


# --- Contrato do JSON ---

def test_json_tables_valid_and_ordered():
    geral = D(get_rule(2026, "TR-005").parametros["limite_geral"])
    for tabela in (III, V):
        limites = [D(f["limite_superior"]) for f in tabela]
        assert limites == sorted(limites) and len(set(limites)) == 6
        assert limites[-1] == geral
        aliquotas = [D(f["aliquota_nominal"]) for f in tabela]
        assert aliquotas == sorted(aliquotas) and all(isinstance(f["parcela_deduzir"], str) for f in tabela)
    assert III[0]["parcela_deduzir"] == "0" and V[0]["parcela_deduzir"] == "0"


def test_rules_005_to_009_contract():
    for i in range(5, 10):
        rule = get_rule(2026, f"TR-00{i}")
        assert rule.metadata.fontes and rule.metadata.status.value == "TESTADA"
