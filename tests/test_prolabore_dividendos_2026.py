"""Testes de TR-010 (pró-labore) e TR-011 (dividendos).

Valores esperados: docs/research/pj-comparator-2026-research.md (F-39, F-40, F-41, F-43, F-48).
"""
from decimal import Decimal as D

import pytest

from src.models.tax import (
    AnexoSimples,
    DividendosInput,
    ModoApuracaoLucro,
    ProLaboreInput,
    SimulationStatus,
)
from src.tax_engine.dividendos_2026 import (
    calculate_dividendos_2026,
    calculate_irpj_no_das_2026,
    calculate_irrf_dividendos_2026,
)
from src.tax_engine.pf_2026 import calculate_irpf_mensal_2026
from src.tax_engine.prolabore_2026 import calculate_prolabore_2026
from src.models.tax import AtividadeSimples, SimplesSimulationInput
from src.tax_engine.simples_2026 import run_simples_2026
from src.tax_rules import get_rule, parse_decimal

SEM, COM = ModoApuracaoLucro.SEM_ESCRITURACAO, ModoApuracaoLucro.COM_ESCRITURACAO
TETO_INSS = D("8475.55") * D("0.11")


def prolabore(valor):
    return calculate_prolabore_2026(ProLaboreInput(2026, D(valor)))


# --- TR-010 ---

def test_prolabore_zero_no_contribution_and_warning():
    r = prolabore("0")
    assert (r.inss, r.irpf, r.liquido, r.base_inss) == (0, 0, 0, 0)
    assert any("ausência de remuneração" in w for w in r.warnings)


def test_prolabore_positive_below_minimum_uses_informed_value():
    r = prolabore("1000")
    assert r.base_inss == D("1000") and r.inss == D("110.00")  # não vira salário mínimo
    assert any("complementação, utilização ou agrupamento" in w for w in r.warnings)
    assert r.liquido == D("890.00")


def test_prolabore_at_minimum_wage():
    r = prolabore("1621.00")
    assert r.inss == D("178.31") and not r.warnings


def test_prolabore_below_ceiling():
    r = prolabore("5000")
    assert r.base_inss == D("5000") and r.inss == D("550.00")


def test_prolabore_exactly_at_ceiling():
    r = prolabore("8475.55")
    assert r.base_inss == D("8475.55") and r.inss == TETO_INSS and not r.warnings


def test_prolabore_above_ceiling_capped():
    r = prolabore("15000")
    assert r.base_inss == D("8475.55") and r.inss == TETO_INSS
    assert any("teto" in w for w in r.warnings)


@pytest.mark.parametrize("valor", ["0", "1000", "2500", "5000", "6000", "8475.55", "15000"])
def test_prolabore_irpf_reuses_tr001_and_liquido_invariant(valor):
    r = prolabore(valor)
    assert r.irpf == calculate_irpf_mensal_2026(D(valor), r.inss).imposto_devido
    assert r.liquido == r.bruto - r.inss - r.irpf


def test_prolabore_previdenciary_deduction_and_2026_reduction():
    r = prolabore("6000")
    ref = calculate_irpf_mensal_2026(D("6000"), D("660.00"))
    assert not ref.usou_simplificado and ref.deducao_utilizada == D("660.00")  # INSS > simplificado
    assert ref.reducao == D("978.62") - D("0.133145") * 6000 > 0
    assert r.irpf == ref.imposto_antes_reducao - ref.reducao


def test_prolabore_no_employer_cpp_added():
    # só a retenção do segurado: nunca acima de teto x 11%
    assert prolabore("50000").inss == TETO_INSS
    assert not hasattr(prolabore("5000"), "cpp")


def test_prolabore_rule_params_consistent_with_tr002():
    a = get_rule(2026, "TR-010").parametros
    b = get_rule(2026, "TR-002").parametros
    assert a["teto_previdenciario"] == b["teto_previdenciario"] and a["salario_minimo"] == b["salario_minimo"]


def test_prolabore_input_validation():
    with pytest.raises(TypeError):
        ProLaboreInput(2026, 1000.0)
    with pytest.raises(ValueError):
        ProLaboreInput(2026, D("-1"))
    with pytest.raises(ValueError):
        calculate_prolabore_2026(ProLaboreInput(2027, D("1")))


# --- TR-011: IRRF art. 6º-A ---

@pytest.mark.parametrize("total,irrf", [
    ("0", "0"), ("49999.99", "0"), ("50000.00", "0"),
    ("50000.01", "5000.001"), ("60000.00", "6000.00"),
])
def test_irrf_dividends_boundaries(total, irrf):
    assert calculate_irrf_dividendos_2026(D(total)) == D(irrf)


def test_irrf_is_on_total_not_on_excess():
    assert calculate_irrf_dividendos_2026(D("60000")) == D("6000") != D("1000")


def test_dividends_liquid_never_negative_and_equals_gross_minus_irrf():
    for v in ("0", "49999.99", "50000.00", "50000.01", "60000.00"):
        r = calculate_dividendos_2026(DividendosInput(2026, D(v), COM, D("100000")))
        assert r.status == SimulationStatus.OK and r.liquido == r.bruto - r.irrf >= 0


# --- TR-011: sem escrituração ---

def irpj(anexo, faixa, aliq, receita="20000"):
    return calculate_irpj_no_das_2026(anexo, faixa, D(aliq), D(receita))


def test_irpj_in_das_anexo_iii_low_band():
    assert irpj(AnexoSimples.III, 1, "0.06") == D("20000") * D("0.06") * D("0.04")


def test_irpj_in_das_anexo_v_bands_follow_official_repartition():
    for faixa, pct in enumerate(["0.25", "0.23", "0.24", "0.21", "0.23"], start=1):
        assert irpj(AnexoSimples.V, faixa, "0.10") == D("20000") * D("0.10") * D(pct)


def test_irpj_in_das_anexo_iii_fifth_band_split():
    # alíquota efetiva abaixo do limite: partilha normal (4%)
    assert irpj(AnexoSimples.III, 5, "0.14") == D("20000") * D("0.14") * D("0.04")
    # acima de 14,92537%: ISS fixo em 5%; IRPJ = (efetiva - 5%) x 6,02%
    assert irpj(AnexoSimples.III, 5, "0.17") == D("20000") * (D("0.17") - D("0.05")) * D("0.0602")


def test_irpj_repartition_params_shape():
    p = get_rule(2026, "TR-011").parametros["reparticao_irpj"]
    assert set(p) == {"III", "V"} and all(len(v) == 6 for v in p.values())


def sem(valor):
    # receita 20000, Anexo III, faixa 2: alíquota efetiva 0.073 -> DAS 1460 -> IRPJ 58.40
    irpj_das = irpj(AnexoSimples.III, 2, "0.073")
    return calculate_dividendos_2026(DividendosInput(2026, D(valor), SEM), receita_pa=D("20000"), irpj_no_das=irpj_das)


def test_sem_escrituracao_limit_derived_from_official_repartition():
    r = sem("0")
    assert r.irpj_no_das == D("58.4000") and r.limite_isento_sem_escrituracao == D("6400") - D("58.4")


def test_sem_escrituracao_exactly_at_limit_ok():
    r = sem("6341.6")
    assert r.status == SimulationStatus.OK and r.irrf == 0 and r.liquido == D("6341.6")


def test_sem_escrituracao_one_cent_above_limit_not_supported():
    r = sem("6341.61")
    assert r.status == SimulationStatus.NAO_SUPORTADO and r.liquido is None and r.irrf is None
    assert "tributação do excedente não é modelada" in r.warnings[0]


def test_sem_escrituracao_anexo_v_intermediate():
    i = irpj(AnexoSimples.V, 2, "0.16125")  # 3225 x 23%
    r = calculate_dividendos_2026(DividendosInput(2026, D("5658.25"), SEM), receita_pa=D("20000"), irpj_no_das=i)
    assert i == D("741.75") and r.status == SimulationStatus.OK
    assert r.limite_isento_sem_escrituracao == D("5658.25")


def test_sem_escrituracao_limit_never_negative():
    r = calculate_dividendos_2026(DividendosInput(2026, D("0"), SEM), receita_pa=D("100"), irpj_no_das=D("999"))
    assert r.limite_isento_sem_escrituracao == 0 and r.status == SimulationStatus.OK


def test_sem_escrituracao_requires_context():
    with pytest.raises(ValueError):
        calculate_dividendos_2026(DividendosInput(2026, D("1"), SEM))


def test_sem_escrituracao_high_dividends_irrf_not_reachable_without_excess():
    # limite de 32% x 200000 - IRPJ permite > 50.000: aplica 10% sobre o total
    r = calculate_dividendos_2026(DividendosInput(2026, D("60000"), SEM), receita_pa=D("200000"), irpj_no_das=D("100"))
    assert r.status == SimulationStatus.OK and r.irrf == D("6000.00")


# --- TR-011: com escrituração ---

def test_com_escrituracao_sufficient_profit():
    r = calculate_dividendos_2026(DividendosInput(2026, D("3000"), COM, D("10000")))
    assert r.status == SimulationStatus.OK and r.limite_isento_sem_escrituracao is None
    assert any("escrituração contábil regular" in w for w in r.warnings)


def test_com_escrituracao_equal_to_available_profit():
    assert calculate_dividendos_2026(DividendosInput(2026, D("10000"), COM, D("10000"))).status == SimulationStatus.OK


def test_com_escrituracao_above_available_profit_incompatible():
    r = calculate_dividendos_2026(DividendosInput(2026, D("10000.01"), COM, D("10000")))
    assert r.status == SimulationStatus.INCOMPATIVEL and r.liquido is None


def test_com_escrituracao_requires_profit():
    with pytest.raises(ValueError):
        DividendosInput(2026, D("1"), COM, None)
    with pytest.raises(ValueError):
        DividendosInput(2026, D("1"), SEM, D("1"))


def test_com_escrituracao_zero_value():
    r = calculate_dividendos_2026(DividendosInput(2026, D("0"), COM, D("0")))
    assert r.status == SimulationStatus.OK and r.irrf == 0 and r.liquido == 0


def test_dividends_input_validation():
    with pytest.raises(TypeError):
        DividendosInput(2026, 10.0, COM, D("1"))
    with pytest.raises(ValueError):
        DividendosInput(2026, D("-1"), COM, D("1"))
    with pytest.raises(TypeError):
        DividendosInput(2026, D("1"), "COM_ESCRITURACAO", D("1"))
    with pytest.raises(ValueError):
        DividendosInput(2026, D("1"), COM, D("1"), D("-5"))


# --- TR-011: altas rendas (somente avisos) ---

def altas(renda):
    r = calculate_dividendos_2026(DividendosInput(2026, D("1000"), COM, D("5000"), renda))
    return r


def test_high_income_none_warns_not_evaluated():
    assert any("não foi avaliada" in w for w in altas(None).warnings)


@pytest.mark.parametrize("renda", ["600000.00"])
def test_high_income_at_limit_no_extra_warning(renda):
    w = " ".join(altas(D(renda)).warnings)
    assert "altas rendas" not in w


@pytest.mark.parametrize("renda", ["600000.01", "1200000.00"])
def test_high_income_above_limit_warns_without_computing_tax(renda):
    r = altas(D(renda))
    assert any("pode estar sujeito à tributação mínima anual" in w for w in r.warnings)
    assert r.irrf == 0  # nenhum imposto anual calculado


def test_previous_years_profit_warning():
    assert any("2025 ou anteriores" in w for w in altas(None).warnings)


def test_dividend_limit_without_bookkeeping_subtracts_only_irpj_component():
    # Q-PJ-07: limite = presunção x receita - IRPJ contido no DAS (não o DAS total)
    receita = D("20000")
    simples = run_simples_2026(SimplesSimulationInput(
        ano=2026, receita_pa=receita, receitas_anteriores=(receita,) * 12, folha_pa=D("6000"),
        folhas_anteriores=(D("6000"),) * 12, receita_acumulada_ano=receita, meses_desde_abertura=24,
        meses_atividade_no_ano=12, atividade=AtividadeSimples.CONSULTORIA,
    ))
    das_total = simples.das
    irpj_no_das = calculate_irpj_no_das_2026(simples.fator.anexo, simples.faixa.numero, simples.eficaz.aliquota, receita)
    presuncao = parse_decimal(get_rule(2026, "TR-011").parametros["percentual_presuncao_servicos"])
    assert irpj_no_das != das_total and 0 < irpj_no_das < das_total

    r = calculate_dividendos_2026(DividendosInput(2026, D("0"), SEM), receita_pa=receita, irpj_no_das=irpj_no_das)
    assert r.limite_isento_sem_escrituracao == receita * presuncao - irpj_no_das
    assert r.limite_isento_sem_escrituracao != receita * presuncao - das_total
    assert r.irpj_no_das == irpj_no_das
