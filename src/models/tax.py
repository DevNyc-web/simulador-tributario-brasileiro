"""Modelos comuns do motor tributário.

Modelos imutáveis (dataclasses frozen) e enums fechados, para impedir que
strings livres representem status de simulação ou de regra. Nenhum modelo
aqui contém regra, alíquota ou fórmula fiscal — apenas estrutura.

Valores fiscais pendentes são sempre None, nunca zero: zero é um valor real.
"""
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class SimulationStatus(str, Enum):
    """Status possível do resultado de uma simulação."""

    OK = "OK"
    PENDENTE = "PENDENTE"
    NAO_SUPORTADO = "NAO_SUPORTADO"
    INCOMPATIVEL = "INCOMPATIVEL"


class RuleStatus(str, Enum):
    """Estágio do ciclo de vida de uma regra tributária (tax-rule-catalog.md)."""

    PENDENTE = "PENDENTE"
    PESQUISADA = "PESQUISADA"
    VALIDADA = "VALIDADA"
    IMPLEMENTADA = "IMPLEMENTADA"
    TESTADA = "TESTADA"

    @property
    def esta_validada_normativamente(self) -> bool:
        """VALIDADA significa que a regra foi confirmada jurídica/normativamente
        contra fonte oficial — não que exista código capaz de calculá-la."""
        return self in (RuleStatus.VALIDADA, RuleStatus.IMPLEMENTADA, RuleStatus.TESTADA)

    @property
    def pode_produzir_resultado_fiscal(self) -> bool:
        """Só regra com código pronto (IMPLEMENTADA ou TESTADA) pode alimentar
        um cálculo real. VALIDADA sozinha NÃO autoriza cálculo."""
        return self in (RuleStatus.IMPLEMENTADA, RuleStatus.TESTADA)


@dataclass(frozen=True)
class TaxRuleMetadata:
    """Metadados de uma regra tributária (TR-XXX) — não os parâmetros fiscais em si."""

    id: str
    nome: str
    ano: int
    status: RuleStatus
    vigencia_inicio: str | None
    vigencia_fim: str | None
    fontes: tuple[str, ...] = ()


@dataclass(frozen=True)
class SimulationInput:
    """Entrada genérica de uma simulação; campos específicos virão por cenário."""

    ano: int
    tipo_simulacao: str | None = None


@dataclass(frozen=True)
class TaxItem:
    """Um tributo/contribuição individual dentro de um resultado de simulação."""

    codigo: str
    descricao: str
    valor: Decimal | None
    aliquota: Decimal | None
    base_calculo: Decimal | None


@dataclass(frozen=True)
class ExplanationItem:
    """Texto explicativo associado (opcionalmente) a uma regra."""

    titulo: str
    descricao: str
    rule_id: str | None = None


@dataclass(frozen=True)
class SimulationResult:
    """Resultado de uma simulação para um ano/cenário.

    Valores pendentes são None, nunca zero.
    """

    status: SimulationStatus
    ano: int
    tipo_simulacao: str | None
    total_tributos: Decimal | None
    liquido_estimado: Decimal | None
    itens: tuple[TaxItem, ...] = ()
    explicacoes: tuple[ExplanationItem, ...] = ()
    warnings: tuple[str, ...] = ()
