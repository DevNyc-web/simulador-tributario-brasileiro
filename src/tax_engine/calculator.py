"""Núcleo de cálculo tributário (independente de Flask/interface).

Calcula apenas o cenário PF 2026 (TR-001/TR-002); qualquer outro cenário
devolve um SimulationResult pendente (sem inventar valores).
"""
from src.models.tax import PFSimulationInput, SimulationResult, SimulationStatus

from .pf_2026 import ANO as PF_ANO
from .pf_2026 import calculate_pf_2026


def calculate(rules: dict, scenario: dict) -> SimulationResult:
    """Calcula um cenário com as regras de um ano.

    Cenário PF: scenario = {"tipo_simulacao": "pf", "entrada": PFSimulationInput}.
    Qualquer outro caso retorna status PENDENTE (total_tributos e
    liquido_estimado permanecem None, nunca zero).
    """
    entrada = scenario.get("entrada")
    if (
        scenario.get("tipo_simulacao") == "pf"
        and isinstance(entrada, PFSimulationInput)
        and entrada.ano == rules["ano"] == PF_ANO
    ):
        return calculate_pf_2026(entrada)
    return SimulationResult(
        status=SimulationStatus.PENDENTE,
        ano=rules["ano"],
        tipo_simulacao=scenario.get("tipo_simulacao"),
        total_tributos=None,
        liquido_estimado=None,
        warnings=("Nenhuma regra apta a produzir resultado fiscal para o ano/cenário informado.",),
    )
