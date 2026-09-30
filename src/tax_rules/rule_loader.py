"""Carrega as regras tributárias de data/tax_rules/<ano>/rules.json.

Nenhuma regra fiscal vive em código: apenas dados por ano. Este módulo só
localiza, lê e valida a forma do arquivo — nunca calcula.
"""
import json
from dataclasses import dataclass
from pathlib import Path

from src.models.tax import RuleStatus, TaxRuleMetadata

from .exceptions import (
    InvalidRuleFileError,
    RuleNotCalculableError,
    RuleNotFoundError,
    UnsupportedTaxYearError,
)

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


@dataclass(frozen=True)
class TaxRule:
    """Regra carregada: metadados validados + parâmetros crus (decimais ainda
    como string; quem usa converte com parse_decimal)."""

    metadata: TaxRuleMetadata
    parametros: dict


def get_rule(year: int, rule_id: str, *, require_calculable: bool = True) -> TaxRule:
    """Obtém uma regra por ID, validando metadados.

    Levanta RuleNotFoundError se o ID não existir, InvalidRuleFileError se os
    metadados forem inválidos e RuleNotCalculableError se o status não
    autorizar resultado fiscal (a menos que require_calculable=False).
    """
    matches = [r for r in load_year_rules(year)["regras"] if isinstance(r, dict) and r.get("id") == rule_id]
    if not matches:
        raise RuleNotFoundError(f"Regra {rule_id} não encontrada para {year}.")
    if len(matches) > 1:
        raise InvalidRuleFileError(f"Regra {rule_id} duplicada em {year}.")
    raw = matches[0]

    try:
        status = RuleStatus(raw["status"])
        fontes = raw["fontes"]
        parametros = raw["parametros"]
        if raw["ano"] != year or not raw["nome"] or not raw["vigencia_inicio"]:
            raise ValueError
        if not (isinstance(fontes, list) and fontes and isinstance(parametros, dict)):
            raise ValueError
        meta = TaxRuleMetadata(
            id=rule_id,
            nome=raw["nome"],
            ano=year,
            status=status,
            vigencia_inicio=raw["vigencia_inicio"],
            vigencia_fim=raw["vigencia_fim"],
            fontes=tuple(fontes),
        )
    except (KeyError, ValueError) as exc:
        raise InvalidRuleFileError(f"Metadados inválidos na regra {rule_id} ({year}).") from exc

    if require_calculable and not status.pode_produzir_resultado_fiscal:
        raise RuleNotCalculableError(f"Regra {rule_id} com status {status.value} não produz resultado fiscal.")
    return TaxRule(metadata=meta, parametros=parametros)
