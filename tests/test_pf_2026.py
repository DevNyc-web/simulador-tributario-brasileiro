"""Testes do motor PF 2026 (TR-001 IRPF mensal, TR-002 INSS autônomo).

Valores esperados vêm de docs/research/pf-2026-research.md (F-01, F-02, F-11).
Comparações exatas em Decimal; nenhum arredondamento é aplicado (Q-02).
"""
from decimal import Decimal as D

import pytest

from src.models.tax import PFSimulationInput, PlanoINSS, SimulationStatus
from src.services import simulate_transition
from src.tax_engine import calculate
from src.tax_engine.pf_2026 import (
    calculate_inss_autonomo_2026,
    calculate_irpf_mensal_2026,
    calculate_pf_2026,
)
from src.tax_rules import load_year_rules

SIMPL = D("607.20")  # desconto simplificado (F-01)


def irpf(rendimento, contribuicao="0"):
    return calculate_irpf_mensal_2026(D(rendimento), D(contribuicao))


# --- TR-001: faixas (base = rendimento - 607,20 quando só há simplificado) ---

@pytest.mark.parametrize("base,aliq", [
    ("2428.80", "0"), ("2428.81", "0.075"),
    ("2826.65", "0.075"), ("2826.66", "0.15"),
    ("3751.05", "0.15"), ("3751.06", "0.225"),
    ("4664.68", "0.225"), ("4664.69", "0.275"),
])
def test_irpf_band_boundaries(base, aliq):
    r = irpf(D(base) + SIMPL)
    assert r.base_calculo == D(base)
    assert r.aliquota == D(aliq)


def test_irpf_zero_income():
    r = irpf("0")
    assert r.base_calculo == 0 and r.imposto_devido == 0 and r.reducao == 0


def test_irpf_below_first_band():
    r = irpf("1000")
    assert r.base_calculo == D("392.80") and r.imposto_devido == 0


@pytest.mark.parametrize("renda,formula", [
    ("5000.00", D("312.89")),
    ("5000.01", D("978.62") - D("0.133145") * D("5000.01")),
    ("7350.00", D("978.62") - D("0.133145") * D("7350.00")),
    ("7350.01", D("0")),
])
def test_reducao_uses_rendimento_thresholds(renda, formula):
    r = irpf(renda)
    assert r.reducao == min(formula, r.imposto_antes_reducao)


def test_reducao_capped_at_tax_and_tax_never_negative():
    for renda in ("1000", "3036.00", "4000.00", "5000.00", "5500", "6000", "7350", "9000", "50000"):
        r = irpf(renda)
        assert r.reducao <= r.imposto_antes_reducao
        assert r.imposto_devido >= 0 and r.reducao >= 0


def test_reducao_threshold_not_base():
    # rendimento 5.000 => redução máxima mesmo com base (4.392,80) < 5.000
    assert irpf("5000.00").imposto_devido == 0
    # rendimento > 7.350 sem redução, mesmo com contribuição alta derrubando a base
    r = irpf("7400.00", "2000.00")
    assert r.reducao == 0


def test_simplified_chosen_when_greater():
    r = irpf("4000", "500")
    assert r.usou_simplificado and r.deducao_utilizada == SIMPL


def test_contribution_chosen_when_greater_and_not_summed():
    r = irpf("6000", "649.60")
    assert not r.usou_simplificado
    assert r.deducao_utilizada == D("649.60")
    assert r.base_calculo == D("5350.40")


# --- Exemplos oficiais (F-02; TC-001..005) ---

def test_irpf_official_example_tc001_joao():
    r = irpf("3036.00")
    # A página oficial da Receita (F-02) publica literalmente "R$ 3.036,00 - R$ 607,20 = R$ 2.428,00",
    # o que é aritmeticamente inconsistente: o resultado correto é 2.428,80 (limite da faixa zero).
    # O motor usa o valor matematicamente correto; o imposto permanece 0,00 em ambos os casos.
    assert r.base_calculo == D("2428.80") and r.imposto_devido == 0


def test_irpf_official_example_tc002_jose():
    r = irpf("4000.00")
    assert r.base_calculo == D("3392.80")
    assert r.imposto_antes_reducao == D("114.76")
    assert r.reducao == D("114.76") and r.imposto_devido == 0


def test_irpf_official_example_tc003_maria():
    r = irpf("5000.00")
    assert r.base_calculo == D("4392.80")
    assert r.imposto_antes_reducao == D("312.89") and r.imposto_devido == 0


def test_irpf_official_example_tc004_rita():
    r = irpf("6000.00", "649.60")
    assert r.imposto_antes_reducao == D("562.63")
    assert r.reducao == D("179.75")
    assert r.imposto_devido == D("382.88")


def test_irpf_official_example_tc005_vera():
    r = irpf("7607.20")
    assert r.base_calculo == D("7000.00")
    assert r.imposto_devido == D("1016.27") and r.reducao == 0


# --- TR-002 ---

def inss(renda, plano=PlanoINSS.NORMAL):
    return calculate_inss_autonomo_2026(D(renda), plano)


def test_inss_normal_at_minimum_wage():
    assert inss("1621.00").contribuicao == D("324.20")


def test_inss_normal_above_minimum():
    r = inss("3000.00")
    assert r.contribuicao == D("600.00") and not r.abaixo_do_minimo


def test_inss_normal_exactly_at_ceiling():
    r = inss("8475.55")
    assert r.contribuicao == D("1695.11") and not r.limitado_ao_teto


def test_inss_normal_above_ceiling_capped():
    r = inss("50000")
    assert r.contribuicao == D("1695.11") and r.limitado_ao_teto


def test_inss_normal_below_minimum_adjusts_and_warns():
    r = inss("1000")
    assert r.abaixo_do_minimo and r.contribuicao == D("324.20")
    res = calculate_pf_2026(PFSimulationInput(2026, D("1000"), PlanoINSS.NORMAL))
    assert any("abaixo do salário mínimo" in w for w in res.warnings)


@pytest.mark.parametrize("renda", ["1000", "3000", "9000"])
def test_inss_simplified_fixed_independent_of_income(renda):
    assert inss(renda, PlanoINSS.SIMPLIFICADO).contribuicao == D("178.31")


def test_simplified_warns_about_limitation():
    res = calculate_pf_2026(PFSimulationInput(2026, D("3000"), PlanoINSS.SIMPLIFICADO))
    assert any("aposentadoria por tempo de contribuição" in w for w in res.warnings)


def test_no_float_anywhere():
    res = calculate_pf_2026(PFSimulationInput(2026, D("6000"), PlanoINSS.NORMAL))
    values = [res.total_tributos, res.liquido_estimado]
    for it in res.itens:
        values += [it.valor, it.aliquota, it.base_calculo]
    assert all(isinstance(v, D) for v in values)
    with pytest.raises(TypeError):
        PFSimulationInput(2026, 6000.0, PlanoINSS.NORMAL)
    with pytest.raises(TypeError):
        PFSimulationInput(2026, D("6000"), "NORMAL")


# --- Integração ---

@pytest.mark.parametrize("renda", ["0", "1000", "1621.00", "4000", "6000", "8475.55", "12000"])
@pytest.mark.parametrize("plano", list(PlanoINSS))
def test_integrated_invariants(renda, plano):
    res = calculate_pf_2026(PFSimulationInput(2026, D(renda), plano))
    assert res.status == SimulationStatus.OK
    codigos = {i.codigo: i for i in res.itens}
    assert set(codigos) == {"INSS", "IRPF"}
    assert res.total_tributos == codigos["INSS"].valor + codigos["IRPF"].valor
    assert res.liquido_estimado == D(renda) - res.total_tributos
    assert all(v is not None for i in res.itens for v in (i.valor, i.aliquota, i.base_calculo))
    assert {"TR-001", "TR-002"} <= {e.rule_id for e in res.explicacoes}


def test_integrated_flow_6000_normal():
    res = calculate_pf_2026(PFSimulationInput(2026, D("6000"), PlanoINSS.NORMAL))
    # INSS 20% x 6000 = 1200 (> simplificado) -> base 4800 -> 27,5% -> 411.27 - reducao 179.75
    inss_item, irpf_item = res.itens
    assert inss_item.valor == D("1200.00")
    assert irpf_item.base_calculo == D("4800.00")
    assert irpf_item.valor == D("4800.00") * D("0.275") - D("908.73") - (D("978.62") - D("0.133145") * 6000)


def test_calculator_dispatch_and_pending():
    entrada = PFSimulationInput(2026, D("4000"), PlanoINSS.NORMAL)
    scenario = {"tipo_simulacao": "pf", "entrada": entrada}
    res = simulate_transition(scenario)
    assert res[0].status == SimulationStatus.OK
    assert all(r.status == SimulationStatus.PENDENTE and r.total_tributos is None for r in res[1:])
    assert calculate(load_year_rules(2026), {}).status == SimulationStatus.PENDENTE
    with pytest.raises(ValueError):
        calculate_pf_2026(PFSimulationInput(2027, D("1"), PlanoINSS.NORMAL))


def test_inss_zero_income_is_zero_and_warns():
    for plano in PlanoINSS:
        r = inss("0", plano)
        assert r.contribuicao == 0 and r.sem_remuneracao and not r.abaixo_do_minimo
    res = calculate_pf_2026(PFSimulationInput(2026, D("0"), PlanoINSS.NORMAL))
    assert any("contribuição facultativa" in w for w in res.warnings)


def test_integrated_zero_income():
    for plano in PlanoINSS:
        res = calculate_pf_2026(PFSimulationInput(2026, D("0"), plano))
        assert [i.valor for i in res.itens] == [0, 0]
        assert res.total_tributos == 0 and res.liquido_estimado == 0


def test_positive_income_below_minimum_reaches_minimum_with_explicit_warning():
    res = calculate_pf_2026(PFSimulationInput(2026, D("500"), PlanoINSS.NORMAL))
    assert res.itens[0].valor == D("1621.00") * D("0.20") == D("324.20")
    w = next(w for w in res.warnings if "abaixo do salário mínimo" in w)
    assert "complementação, utilização ou agrupamento" in w and "não é uma contribuição obrigatória adicional" in w
