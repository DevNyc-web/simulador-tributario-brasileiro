"""Núcleo de cálculo tributário (independente de Flask/interface).

Ainda sem cálculos reais: enquanto não houver regra com
RuleStatus.pode_produzir_resultado_fiscal (isto é, IMPLEMENTADA ou TESTADA),
devolve um SimulationResult pendente (sem inventar valores). Uma regra
apenas VALIDADA (normativamente) não é suficiente para autorizar cálculo —
só quando também estiver IMPLEMENTADA no ciclo técnico.
"""
from src.models.tax import SimulationResult, SimulationStatus


def calculate(rules: dict, scenario: dict) -> SimulationResult:
    """Calcula um cenário com as regras de um ano.

    Sem regras aptas a produzir resultado fiscal (ver
    RuleStatus.pode_produzir_resultado_fiscal), retorna um SimulationResult
    com status PENDENTE (nenhum valor numérico é produzido —
    total_tributos e liquido_estimado permanecem None, nunca zero).
    """
    if not rules.get("regras"):
        return SimulationResult(
            status=SimulationStatus.PENDENTE,
            ano=rules["ano"],
            tipo_simulacao=scenario.get("tipo_simulacao"),
            total_tributos=None,
            liquido_estimado=None,
            warnings=("Nenhuma regra apta a produzir resultado fiscal para o ano informado.",),
        )
    raise NotImplementedError("Cálculo real ainda não implementado.")
