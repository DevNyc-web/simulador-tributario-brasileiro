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


class PlanoINSS(str, Enum):
    """Plano previdenciário do contribuinte individual (escolhido pelo usuário)."""

    NORMAL = "NORMAL"
    SIMPLIFICADO = "SIMPLIFICADO"


@dataclass(frozen=True)
class PFSimulationInput:
    """Entrada do cenário Pessoa Física / autônomo (TR-001 + TR-002)."""

    ano: int
    renda_mensal: Decimal
    plano_inss: PlanoINSS

    def __post_init__(self):
        if not isinstance(self.renda_mensal, Decimal) or not self.renda_mensal.is_finite():
            raise TypeError("renda_mensal deve ser um Decimal finito (nunca float).")
        if self.renda_mensal < 0:
            raise ValueError("renda_mensal não pode ser negativa.")
        if not isinstance(self.plano_inss, PlanoINSS):
            raise TypeError("plano_inss deve ser um PlanoINSS.")


class CategoriaMEI(str, Enum):
    """Categoria tributária do MEI comum (define as parcelas ICMS/ISS do DAS)."""

    COMERCIO_INDUSTRIA = "COMERCIO_INDUSTRIA"
    SERVICOS = "SERVICOS"
    COMERCIO_E_SERVICOS = "COMERCIO_E_SERVICOS"


class StatusLimiteMEI(str, Enum):
    """Situação da receita frente ao limite de receita bruta do MEI."""

    COMPATIVEL = "COMPATIVEL"
    EXCESSO_ATE_20 = "EXCESSO_ATE_20"
    EXCESSO_MAIS_20 = "EXCESSO_MAIS_20"


@dataclass(frozen=True)
class MEISimulationInput:
    """Entrada do cenário MEI comum (TR-003 + TR-004).

    meses_atividade_no_ano: 12 para MEI enquadrado desde janeiro; no ano de abertura,
    meses até 31/12 (fração de mês = mês inteiro).
    optante_simei: o cenário continua enquadrado/optante pelo SIMEI (não significa
    "teve receita no mês": receita zero não elimina o DAS). Baixa está fora do MVP.
    """

    ano: int
    receita_acumulada: Decimal
    categoria: CategoriaMEI
    meses_atividade_no_ano: int
    optante_simei: bool = True

    def __post_init__(self):
        if not isinstance(self.receita_acumulada, Decimal) or not self.receita_acumulada.is_finite():
            raise TypeError("receita_acumulada deve ser um Decimal finito (nunca float).")
        if self.receita_acumulada < 0:
            raise ValueError("receita_acumulada não pode ser negativa.")
        if not isinstance(self.categoria, CategoriaMEI):
            raise TypeError("categoria deve ser uma CategoriaMEI.")
        if isinstance(self.meses_atividade_no_ano, bool) or not isinstance(self.meses_atividade_no_ano, int):
            raise TypeError("meses_atividade_no_ano deve ser int.")
        if not 1 <= self.meses_atividade_no_ano <= 12:
            raise ValueError("meses_atividade_no_ano deve estar entre 1 e 12.")
        if not isinstance(self.optante_simei, bool):
            raise TypeError("optante_simei deve ser bool.")


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
