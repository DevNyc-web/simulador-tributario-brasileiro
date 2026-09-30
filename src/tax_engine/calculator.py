"""Núcleo de cálculo tributário (independente de Flask/interface).

Calcula apenas os cenários PF e MEI 2026 (TR-001 a TR-004); qualquer outro cenário
devolve um SimulationResult pendente (sem inventar valores).
"""
from src.models.tax import MEISimulationInput, PFSimulationInput, SimulationResult, SimulationStatus

from .mei_2026 import ANO as MEI_ANO
from .mei_2026 import calculate_mei_2026
from .pf_2026 import ANO as PF_ANO
from .pf_2026 import calculate_pf_2026


def calculate(rules: dict, scenario: dict) -> SimulationResult:
    """Calcula um cenário com as regras de um ano.

    Cenários: {"tipo_simulacao": "pf"|"mei", "entrada": PFSimulationInput|MEISimulationInput}.
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
    if (
        scenario.get("tipo_simulacao") == "mei"
        and isinstance(entrada, MEISimulationInput)
        and entrada.ano == rules["ano"] == MEI_ANO
    ):
        return calculate_mei_2026(entrada)
    return SimulationResult(
        status=SimulationStatus.PENDENTE,
        ano=rules["ano"],
        tipo_simulacao=scenario.get("tipo_simulacao"),
        total_tributos=None,
        liquido_estimado=None,
        warnings=("Nenhuma regra apta a produzir resultado fiscal para o ano/cenário informado.",),
    )
