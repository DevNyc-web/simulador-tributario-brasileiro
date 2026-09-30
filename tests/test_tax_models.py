"""Testes dos modelos comuns do motor tributário (contrato estrutural).

Nenhum destes testes verifica fórmula fiscal: apenas a imutabilidade dos
modelos e a política de None-vs-zero para valores pendentes.
"""
import dataclasses
import json
from decimal import Decimal
from pathlib import Path

import pytest

from src.models.tax import (
    ExplanationItem,
    RuleStatus,
    SimulationInput,
    SimulationResult,
    SimulationStatus,
    TaxItem,
    TaxRuleMetadata,
)
from src.tax_rules import parse_decimal

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def test_simulation_result_pending_uses_none_not_zero():
    result = SimulationResult(
        status=SimulationStatus.PENDENTE,
        ano=2026,
        tipo_simulacao=None,
        total_tributos=None,
        liquido_estimado=None,
    )
    assert result.total_tributos is None
    assert result.liquido_estimado is None
    assert result.itens == ()
    assert result.explicacoes == ()


def test_simulation_result_is_frozen():
    result = SimulationResult(
        status=SimulationStatus.PENDENTE,
        ano=2026,
        tipo_simulacao=None,
        total_tributos=None,
        liquido_estimado=None,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.total_tributos = Decimal("1")


def test_tax_rule_metadata_is_frozen():
    metadata = TaxRuleMetadata(
        id="TR-000",
        nome="Regra fictícia para teste de infraestrutura",
        ano=2026,
        status=RuleStatus.PENDENTE,
        vigencia_inicio=None,
        vigencia_fim=None,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        metadata.status = RuleStatus.VALIDADA


def test_tax_item_accepts_decimal_or_none():
    pendente = TaxItem(
        codigo="X", descricao="Item pendente", valor=None, aliquota=None, base_calculo=None
    )
    calculado = TaxItem(
        codigo="X",
        descricao="Item",
        valor=Decimal("10.00"),
        aliquota=Decimal("0.11"),
        base_calculo=Decimal("100.00"),
    )
    assert pendente.valor is None
    assert calculado.valor == Decimal("10.00")


@pytest.mark.parametrize(
    "status,esperado_validada,esperado_pode_calcular",
    [
        (RuleStatus.PENDENTE, False, False),
        (RuleStatus.PESQUISADA, False, False),
        (RuleStatus.VALIDADA, True, False),
        (RuleStatus.IMPLEMENTADA, True, True),
        (RuleStatus.TESTADA, True, True),
    ],
)
def test_rule_status_semantics_for_all_five_states(
    status, esperado_validada, esperado_pode_calcular
):
    """VALIDADA significa apenas validação normativa/jurídica — não que haja
    código pronto. Só IMPLEMENTADA/TESTADA autorizam produzir resultado
    fiscal (ver docs/project/tax-engine-architecture.md, "Segurança normativa")."""
    assert status.esta_validada_normativamente is esperado_validada
    assert status.pode_produzir_resultado_fiscal is esperado_pode_calcular


def test_simulation_input_generic_fields():
    sim_input = SimulationInput(ano=2026, tipo_simulacao="pf")
    assert sim_input.ano == 2026
    assert sim_input.tipo_simulacao == "pf"


def test_explanation_item_optional_rule_id():
    item = ExplanationItem(titulo="Aviso", descricao="Texto explicativo.")
    assert item.rule_id is None


def test_fictitious_rule_fixture_matches_metadata_contract():
    """Confirma que o contrato futuro de regra (seção 4) é construível a
    partir de um JSON no formato esperado — usando um fixture fictício,
    nunca um dado de data/tax_rules/."""
    payload = json.loads(
        (FIXTURES_DIR / "fictitious_rule_example.json").read_text(encoding="utf-8")
    )
    metadata = TaxRuleMetadata(
        id=payload["id"],
        nome=payload["nome"],
        ano=payload["ano"],
        status=RuleStatus(payload["status"]),
        vigencia_inicio=payload["vigencia_inicio"],
        vigencia_fim=payload["vigencia_fim"],
        fontes=tuple(payload["fontes"]),
    )
    # A fixture usa status "VALIDADA": validada normativamente, mas ainda
    # sem código pronto — não autoriza produzir resultado fiscal.
    assert metadata.status.esta_validada_normativamente
    assert not metadata.status.pode_produzir_resultado_fiscal
    assert parse_decimal(payload["parametros"]["aliquota_exemplo"]) == Decimal("0.1100")


# --- imutabilidade real das coleções ------------------------------------


def test_simulation_result_collections_cannot_be_mutated():
    result = SimulationResult(
        status=SimulationStatus.PENDENTE,
        ano=2026,
        tipo_simulacao=None,
        total_tributos=None,
        liquido_estimado=None,
        itens=(TaxItem(codigo="X", descricao="Item", valor=None, aliquota=None, base_calculo=None),),
        warnings=("aviso",),
    )
    with pytest.raises(AttributeError):
        result.itens.append("qualquer coisa")
    with pytest.raises(TypeError):
        result.itens[0] = None
    with pytest.raises(AttributeError):
        result.warnings.append("outro aviso")


def test_tax_rule_metadata_fontes_cannot_be_mutated():
    metadata = TaxRuleMetadata(
        id="TR-000",
        nome="Regra fictícia para teste de infraestrutura",
        ano=2026,
        status=RuleStatus.PENDENTE,
        vigencia_inicio=None,
        vigencia_fim=None,
        fontes=("F-00",),
    )
    with pytest.raises(AttributeError):
        metadata.fontes.append("F-01")
