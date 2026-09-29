"""Núcleo de cálculo tributário (independente de Flask/interface).

Ainda sem cálculos reais: enquanto não houver regras validadas para o ano,
devolve resultado pendente.
"""
from src.tax_rules import PENDING


def calculate(rules: dict, scenario: dict) -> dict:
    """Calcula um cenário com as regras de um ano.

    Sem regras validadas, retorna resultado pendente (sem inventar valores).
    """
    if not rules.get("regras"):
        return {"ano": rules["ano"], "status": PENDING, "resultado": None}
    raise NotImplementedError("Cálculo real ainda não implementado.")
