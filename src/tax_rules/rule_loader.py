"""Carrega as regras tributárias de data/tax_rules/<ano>/rules.json.

Nenhuma regra fiscal vive em código: apenas dados por ano.
"""
import json
from pathlib import Path

PENDING = "[REGRA PENDENTE DE VALIDAÇÃO]"
SUPPORTED_YEARS = range(2026, 2034)
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "tax_rules"


def load_year_rules(year: int) -> dict:
    """Retorna as regras do ano informado; ValueError se fora de 2026–2033."""
    if year not in SUPPORTED_YEARS:
        raise ValueError(f"Ano fora do período de transição (2026–2033): {year}")
    with (DATA_DIR / str(year) / "rules.json").open(encoding="utf-8") as f:
        return json.load(f)
