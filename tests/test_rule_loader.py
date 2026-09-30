"""Testes da infraestrutura de carregamento de regras tributárias.

Nenhum destes testes verifica fórmula fiscal: apenas o contrato do loader
(schema, validação de ano, tratamento de erros, independência do cwd) e o
parser estrito de decimais.
"""
import json
from decimal import Decimal

import pytest

from src.tax_rules import SUPPORTED_YEARS, load_year_rules, parse_decimal
from src.tax_rules.exceptions import (
    InvalidDecimalValueError,
    InvalidRuleFileError,
    UnsupportedTaxYearError,
)
from src.tax_rules.rule_loader import SCHEMA_VERSION


@pytest.mark.parametrize("year", SUPPORTED_YEARS)
def test_all_supported_years_load_valid_files(year):
    rules = load_year_rules(year)
    assert rules["ano"] == year
    assert rules["schema_version"] == SCHEMA_VERSION


@pytest.mark.parametrize("year", SUPPORTED_YEARS)
def test_all_supported_years_have_no_rules_yet(year):
    rules = load_year_rules(year)
    assert rules["regras"] == []


@pytest.mark.parametrize("year", SUPPORTED_YEARS)
def test_rules_files_have_no_legacy_status_field(year):
    """O campo top-level "status" (legado, redundante com RuleStatus por
    regra) foi retirado do schema; nenhum arquivo deve mais tê-lo."""
    rules = load_year_rules(year)
    assert "status" not in rules


@pytest.mark.parametrize("year", [2025, 2034, 1999, 3000])
def test_unsupported_year_raises_explicit_error(year):
    with pytest.raises(UnsupportedTaxYearError):
        load_year_rules(year)


def test_missing_file_raises_explicit_error(tmp_path, monkeypatch):
    monkeypatch.setattr("src.tax_rules.rule_loader.DATA_DIR", tmp_path)
    with pytest.raises(InvalidRuleFileError):
        load_year_rules(2026)


def test_invalid_json_raises_explicit_error(tmp_path, monkeypatch):
    monkeypatch.setattr("src.tax_rules.rule_loader.DATA_DIR", tmp_path)
    year_dir = tmp_path / "2026"
    year_dir.mkdir()
    (year_dir / "rules.json").write_text("{not valid json", encoding="utf-8")
    with pytest.raises(InvalidRuleFileError):
        load_year_rules(2026)


def test_invalid_schema_version_raises_explicit_error(tmp_path, monkeypatch):
    monkeypatch.setattr("src.tax_rules.rule_loader.DATA_DIR", tmp_path)
    year_dir = tmp_path / "2026"
    year_dir.mkdir()
    payload = {"schema_version": 999, "ano": 2026, "regras": []}
    (year_dir / "rules.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(InvalidRuleFileError):
        load_year_rules(2026)


def test_ano_mismatch_raises_explicit_error(tmp_path, monkeypatch):
    monkeypatch.setattr("src.tax_rules.rule_loader.DATA_DIR", tmp_path)
    year_dir = tmp_path / "2026"
    year_dir.mkdir()
    payload = {"schema_version": SCHEMA_VERSION, "ano": 2027, "regras": []}
    (year_dir / "rules.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(InvalidRuleFileError):
        load_year_rules(2026)


def test_regras_not_a_list_raises_explicit_error(tmp_path, monkeypatch):
    monkeypatch.setattr("src.tax_rules.rule_loader.DATA_DIR", tmp_path)
    year_dir = tmp_path / "2026"
    year_dir.mkdir()
    payload = {"schema_version": SCHEMA_VERSION, "ano": 2026, "regras": "não é lista"}
    (year_dir / "rules.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(InvalidRuleFileError):
        load_year_rules(2026)


def test_loader_is_independent_of_cwd(tmp_path, monkeypatch):
    """load_year_rules não pode depender do diretório de trabalho atual —
    o caminho é resolvido a partir de __file__, não de os.getcwd()."""
    monkeypatch.chdir(tmp_path)
    rules = load_year_rules(2026)
    assert rules["ano"] == 2026
    assert rules["regras"] == []


# --- parse_decimal -----------------------------------------------------


def test_parse_decimal_from_string():
    assert parse_decimal("10.00") == Decimal("10.00")
    assert parse_decimal("0.28") == Decimal("0.28")
    assert parse_decimal("1621.00") == Decimal("1621.00")


@pytest.mark.parametrize("value", [10, 10.0, True, False, [], {}])
def test_parse_decimal_rejects_non_string_types(value):
    with pytest.raises(InvalidDecimalValueError):
        parse_decimal(value)


@pytest.mark.parametrize("value", ["", "abc", "1,50"])
def test_parse_decimal_rejects_malformed_strings(value):
    with pytest.raises(InvalidDecimalValueError):
        parse_decimal(value)


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-Infinity"])
def test_parse_decimal_rejects_non_finite_strings(value):
    with pytest.raises(InvalidDecimalValueError):
        parse_decimal(value)


def test_parse_decimal_none_requires_explicit_allow_none():
    with pytest.raises(InvalidDecimalValueError):
        parse_decimal(None)


def test_parse_decimal_none_with_allow_none_true():
    assert parse_decimal(None, allow_none=True) is None
