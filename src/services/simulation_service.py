"""Orquestra regras (por ano) e motores de cálculo para a camada de interface.

Não contém fórmula nem valor fiscal: só chama os motores e devolve seus resultados.
"""
from dataclasses import dataclass
from typing import Any

from src.models.tax import (
    ComparatorSimulationInput,
    MEISimulationInput,
    SimplesSimulationInput,
    SimulationResult,
)
from src.tax_engine import calculate
from src.tax_engine.comparator_2026 import compare_pf_pj_2026
from src.tax_engine.mei_2026 import calculate_das_mei_2026, calculate_mei_limit_2026
from src.tax_engine.simples_2026 import run_simples_2026
from src.tax_rules import SUPPORTED_YEARS, load_year_rules


@dataclass(frozen=True)
class SimulationOutcome:
    """Resultado do motor + estruturas detalhadas (vindas dos motores) para exibição."""

    tipo: str
    entrada: Any
    result: SimulationResult
    detail: Any = None  # MEI: (LimiteMEIResult, DASMEIResult); Simples: SimplesComputation|SimulationResult; comparar: ComparatorResult


def simulate_transition(scenario: dict) -> list[SimulationResult]:
    """Executa o cenário em cada ano da transição (2026–2033)."""
    return [calculate(load_year_rules(y), scenario) for y in SUPPORTED_YEARS]


def simulate(scenario: dict) -> SimulationOutcome:
    """Executa um cenário real (um ano) e reúne os dados detalhados dos motores."""
    entrada = scenario["entrada"]
    tipo = scenario["tipo_simulacao"]
    result = calculate(load_year_rules(entrada.ano), scenario)
    detail = None
    if isinstance(entrada, MEISimulationInput) and entrada.optante_simei:
        detail = (
            calculate_mei_limit_2026(entrada.receita_acumulada, entrada.meses_atividade_no_ano),
            calculate_das_mei_2026(entrada.categoria),
        )
    elif isinstance(entrada, SimplesSimulationInput):
        detail = run_simples_2026(entrada)
    elif isinstance(entrada, ComparatorSimulationInput):
        detail = compare_pf_pj_2026(entrada)
    return SimulationOutcome(tipo, entrada, result, detail)
