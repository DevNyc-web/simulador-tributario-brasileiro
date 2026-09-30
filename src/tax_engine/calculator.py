"""Núcleo de cálculo tributário (independente de Flask/interface).

Calcula apenas os cenários PF, MEI, Simples e comparador 2026 (TR-001 a TR-011); qualquer outro cenário
devolve um SimulationResult pendente (sem inventar valores).
"""
from src.models.tax import (
    ComparatorSimulationInput,
    MEISimulationInput,
    PFSimulationInput,
    SimplesSimulationInput,
    SimulationResult,
    SimulationStatus,
)

from .comparator_2026 import calculate_comparator_2026
from .mei_2026 import ANO as MEI_ANO
from .mei_2026 import calculate_mei_2026
from .pf_2026 import ANO as PF_ANO
from .pf_2026 import calculate_pf_2026
from .simples_2026 import ANO as SIMPLES_ANO
from .simples_2026 import calculate_simples_2026


def calculate(rules: dict, scenario: dict) -> SimulationResult:
    """Calcula um cenário com as regras de um ano.

    Cenários: {"tipo_simulacao": "pf"|"mei"|"simples"|"comparar", "entrada": <modelo do cenário>}.
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
    if (
        scenario.get("tipo_simulacao") == "simples"
        and isinstance(entrada, SimplesSimulationInput)
        and entrada.ano == rules["ano"] == SIMPLES_ANO
    ):
        return calculate_simples_2026(entrada)
    if (
        scenario.get("tipo_simulacao") == "comparar"
        and isinstance(entrada, ComparatorSimulationInput)
        and entrada.ano == rules["ano"] == SIMPLES_ANO
    ):
        return calculate_comparator_2026(entrada)
    return SimulationResult(
        status=SimulationStatus.PENDENTE,
        ano=rules["ano"],
        tipo_simulacao=scenario.get("tipo_simulacao"),
        total_tributos=None,
        liquido_estimado=None,
        warnings=("Nenhuma regra apta a produzir resultado fiscal para o ano/cenário informado.",),
    )
