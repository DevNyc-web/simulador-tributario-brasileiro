"""Testes do motor MEI 2026 (TR-003 limite, TR-004 DAS-MEI).

Valores esperados: docs/research/mei-2026-research.md (F-23, F-30, F-31).
"""
from decimal import Decimal as D

import pytest

from src.models.tax import CategoriaMEI, MEISimulationInput, SimulationStatus, StatusLimiteMEI
from src.services import simulate_transition
from src.tax_engine import calculate
from src.tax_engine.mei_2026 import calculate_das_mei_2026, calculate_mei_2026, calculate_mei_limit_2026
from src.tax_rules import get_rule, load_year_rules, parse_decimal

C, A, F = StatusLimiteMEI.COMPATIVEL, StatusLimiteMEI.EXCESSO_ATE_20, StatusLimiteMEI.EXCESSO_MAIS_20


def lim(receita, meses=12):
    return calculate_mei_limit_2026(D(receita), meses)


# --- TR-003: limite anual ---

@pytest.mark.parametrize("receita,status", [
    ("0", C), ("80999.99", C), ("81000.00", C),
    ("81000.01", A), ("97200.00", A),
    ("97200.01", F),
])
def test_annual_limit_classification(receita, status):
    assert lim(receita).status is status


def test_annual_limit_values_from_rules():
    r = lim("0")
    assert r.limite_aplicavel == D("81000.00") and r.limite_com_tolerancia == D("97200.00")


# --- TR-003: ano de abertura ---

@pytest.mark.parametrize("meses,esperado", [(12, "81000.00"), (6, "40500.00"), (1, "6750.00"), (7, "47250.00")])
def test_applicable_limit_by_months(meses, esperado):
    assert lim("0", meses).limite_aplicavel == D(esperado)


@pytest.mark.parametrize("meses", [1, 6, 11])
def test_proportional_boundaries(meses):
    limite = lim("0", meses).limite_aplicavel
    teto = limite * D("1.20")
    cent = D("0.01")
    assert lim(limite, meses).status is C
    assert lim(limite + cent, meses).status is A
    assert lim(teto, meses).status is A
    assert lim(teto + cent, meses).status is F


def test_limit_derived_from_rules_not_hardcoded():
    p = get_rule(2026, "TR-003").parametros
    assert lim("0", 6).limite_aplicavel == parse_decimal(p["limite_proporcional_mensal"]) * 6


# --- TR-004 ---

@pytest.mark.parametrize("cat,total", [
    (CategoriaMEI.COMERCIO_INDUSTRIA, "82.05"),
    (CategoriaMEI.SERVICOS, "86.05"),
    (CategoriaMEI.COMERCIO_E_SERVICOS, "87.05"),
])
def test_das_totals(cat, total):
    assert calculate_das_mei_2026(cat).total == D(total)


def test_das_components():
    d = calculate_das_mei_2026(CategoriaMEI.COMERCIO_E_SERVICOS)
    assert (d.previdencia, d.icms, d.iss) == (D("81.05"), D("1.00"), D("5.00"))
    assert calculate_das_mei_2026(CategoriaMEI.SERVICOS).icms == 0
    assert calculate_das_mei_2026(CategoriaMEI.COMERCIO_INDUSTRIA).iss == 0


@pytest.mark.parametrize("receita", ["0", "1000", "81000", "200000"])
def test_das_fixed_and_due_regardless_of_revenue(receita):
    res = calculate_mei_2026(MEISimulationInput(2026, D(receita), CategoriaMEI.SERVICOS, 12))
    assert res.status == SimulationStatus.OK
    assert res.total_tributos == D("86.05") and res.itens[0].valor == D("86.05")


# --- Resultado, warnings, entrada ---

def test_result_shape_and_explanations():
    res = calculate_mei_2026(MEISimulationInput(2026, D("50000"), CategoriaMEI.COMERCIO_INDUSTRIA, 12))
    item = res.itens[0]
    assert item.codigo == "DAS-MEI" and item.base_calculo is None and item.aliquota is None
    assert {e.rule_id for e in res.explicacoes} == {"TR-003", "TR-004"}
    assert res.liquido_estimado is None


def test_excess_warnings():
    a = calculate_mei_2026(MEISimulationInput(2026, D("90000"), CategoriaMEI.SERVICOS, 12))
    assert any("1º de janeiro do ano seguinte" in w for w in a.warnings)
    f = calculate_mei_2026(MEISimulationInput(2026, D("100000"), CategoriaMEI.SERVICOS, 12))
    assert any("1º de janeiro do ano do excesso" in w for w in f.warnings)
    g = calculate_mei_2026(MEISimulationInput(2026, D("100000"), CategoriaMEI.SERVICOS, 6))
    assert any("início da atividade" in w for w in g.warnings)
    ok = calculate_mei_2026(MEISimulationInput(2026, D("1000"), CategoriaMEI.SERVICOS, 12))
    assert not any("desenquadramento" in w or "retroativ" in w for w in ok.warnings)


def test_not_optante_simei_not_supported():
    res = calculate_mei_2026(MEISimulationInput(2026, D("0"), CategoriaMEI.SERVICOS, 12, optante_simei=False))
    assert res.status == SimulationStatus.NAO_SUPORTADO and res.total_tributos is None
    assert res.itens == () and any("enquadrado no SIMEI" in w for w in res.warnings)


def test_zero_revenue_is_not_lack_of_enquadramento():
    res = calculate_mei_2026(MEISimulationInput(2026, D("0"), CategoriaMEI.SERVICOS, 12, optante_simei=True))
    assert res.status == SimulationStatus.OK and res.total_tributos == D("86.05")
    assert MEISimulationInput(2026, D("0"), CategoriaMEI.SERVICOS, 12).optante_simei is True
    with pytest.raises(TypeError):
        MEISimulationInput(2026, D("0"), CategoriaMEI.SERVICOS, 12, optante_simei=0)


def test_input_validation_and_no_float():
    with pytest.raises(TypeError):
        MEISimulationInput(2026, 1000.0, CategoriaMEI.SERVICOS, 12)
    with pytest.raises(ValueError):
        MEISimulationInput(2026, D("-1"), CategoriaMEI.SERVICOS, 12)
    with pytest.raises(TypeError):
        MEISimulationInput(2026, D("1"), "SERVICOS", 12)
    for m in (0, 13):
        with pytest.raises(ValueError):
            MEISimulationInput(2026, D("1"), CategoriaMEI.SERVICOS, m)
    with pytest.raises(TypeError):
        MEISimulationInput(2026, D("1"), CategoriaMEI.SERVICOS, 6.0)
    res = calculate_mei_2026(MEISimulationInput(2026, D("1"), CategoriaMEI.SERVICOS, 12))
    assert isinstance(res.total_tributos, D) and isinstance(res.itens[0].valor, D)


def test_calculator_dispatch():
    entrada = MEISimulationInput(2026, D("10000"), CategoriaMEI.SERVICOS, 12)
    res = simulate_transition({"tipo_simulacao": "mei", "entrada": entrada})
    assert res[0].status == SimulationStatus.OK and res[0].tipo_simulacao == "mei"
    assert all(r.status == SimulationStatus.PENDENTE for r in res[1:])
    assert calculate(load_year_rules(2026), {"tipo_simulacao": "mei"}).status == SimulationStatus.PENDENTE
    with pytest.raises(ValueError):
        calculate_mei_2026(MEISimulationInput(2027, D("1"), CategoriaMEI.SERVICOS, 12))
