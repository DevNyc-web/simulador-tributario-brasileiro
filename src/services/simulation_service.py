"""Orquestra regras (por ano) e motor de cálculo para a camada de interface."""
from src.models.tax import SimulationResult
from src.tax_engine import calculate
from src.tax_rules import SUPPORTED_YEARS, load_year_rules


def simulate_transition(scenario: dict) -> list[SimulationResult]:
    """Executa o cenário em cada ano da transição (2026–2033)."""
    return [calculate(load_year_rules(y), scenario) for y in SUPPORTED_YEARS]
