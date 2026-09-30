"""Exceções específicas do carregamento de regras tributárias."""


class TaxRuleError(Exception):
    """Erro base para problemas de regras tributárias."""


class UnsupportedTaxYearError(TaxRuleError):
    """Ano fora do período suportado (2026-2033)."""


class InvalidRuleFileError(TaxRuleError):
    """Arquivo de regras ausente, malformado, ou fora do schema esperado."""


class InvalidDecimalValueError(TaxRuleError):
    """Valor decimal fiscal inválido (não é uma string decimal válida)."""
