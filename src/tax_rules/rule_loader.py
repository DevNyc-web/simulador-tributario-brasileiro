"""Carrega as regras tributárias de data/tax_rules/<ano>/rules.json.

Nenhuma regra fiscal vive em código: apenas dados por ano. Este módulo só
localiza, lê e valida a forma do arquivo — nunca calcula.
"""
import json
from pathlib import Path

from .exceptions import InvalidRuleFileError, UnsupportedTaxYearError

SUPPORTED_YEARS = range(2026, 2034)
SCHEMA_VERSION = 1
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "tax_rules"


def load_year_rules(year: int) -> dict:
    """Retorna as regras do ano informado.

    Levanta UnsupportedTaxYearError se o ano estiver fora de 2026-2033, e
    InvalidRuleFileError se o arquivo não existir, não for um JSON válido,
    ou não respeitar o schema esperado (schema_version, ano, regras).
    """
    if year not in SUPPORTED_YEARS:
        raise UnsupportedTaxYearError(
            f"Ano fora do período de transição (2026-2033): {year}"
        )

    path = DATA_DIR / str(year) / "rules.json"
    if not path.is_file():
        raise InvalidRuleFileError(f"Arquivo de regras não encontrado: {path}")

    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise InvalidRuleFileError(f"JSON inválido em {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise InvalidRuleFileError(f"Conteúdo de {path} deve ser um objeto JSON.")

    schema_version = data.get("schema_version")
    if schema_version != SCHEMA_VERSION:
        raise InvalidRuleFileError(
            f"schema_version inválido em {path}: esperado {SCHEMA_VERSION}, "
            f"encontrado {schema_version!r}"
        )

    file_year = data.get("ano")
    if file_year != year:
        raise InvalidRuleFileError(
            f"Campo 'ano' ({file_year!r}) diverge do diretório ({year}) em {path}"
        )

    if not isinstance(data.get("regras"), list):
        raise InvalidRuleFileError(f"Campo 'regras' deve ser uma lista em {path}")

    return data
