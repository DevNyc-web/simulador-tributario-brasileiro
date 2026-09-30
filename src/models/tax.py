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


class AnexoSimples(str, Enum):
    """Anexo do Simples Nacional suportado (serviços sujeitos ao Fator R)."""

    III = "III"
    V = "V"


class AtividadeSimples(str, Enum):
    """As 9 atividades do MVP, todas sujeitas ao Fator R (simples-2026-research.md)."""

    DESENVOLVIMENTO_SOFTWARE = "DESENVOLVIMENTO_SOFTWARE"
    CONSULTORIA = "CONSULTORIA"
    ENGENHARIA = "ENGENHARIA"
    ARQUITETURA = "ARQUITETURA"
    MEDICINA = "MEDICINA"
    ODONTOLOGIA = "ODONTOLOGIA"
    PSICOLOGIA = "PSICOLOGIA"
    FISIOTERAPIA = "FISIOTERAPIA"
    ACADEMIAS = "ACADEMIAS"


class StatusSimples(str, Enum):
    """Situação frente aos limites do Simples Nacional (distinta de SimulationStatus)."""

    COMPATIVEL = "COMPATIVEL"
    ACIMA_SUBLIMITE_MVP = "ACIMA_SUBLIMITE_MVP"
    FORA_LIMITE_SIMPLES = "FORA_LIMITE_SIMPLES"


def _money_tuple(name, values):
    if not isinstance(values, tuple):
        raise TypeError(f"{name} deve ser uma tupla de Decimal.")
    for v in values:
        _money(name, v)


def _money(name, value):
    if not isinstance(value, Decimal) or not value.is_finite():
        raise TypeError(f"{name} deve ser Decimal finito (nunca float).")
    if value < 0:
        raise ValueError(f"{name} não pode ser negativo.")


@dataclass(frozen=True)
class SimplesSimulationInput:
    """Entrada do cenário Simples Nacional (TR-005 a TR-009), mês de apuração (PA).

    receitas_anteriores / folhas_anteriores: meses anteriores ao PA, em ordem
    cronológica. Empresa com menos de 13 meses: exatamente meses_desde_abertura - 1
    valores; com 13+ meses: pelo menos 12 (só os 12 mais recentes são usados).
    meses_desde_abertura: 1 = mês de abertura (o próprio PA).
    meses_atividade_no_ano: meses de atividade no ano-calendário até 31/12 (fração
    = mês inteiro); 12 para empresa já existente. Abaixo de 12 indica que a empresa
    abriu no próprio ano e o limite de permanência é proporcional.
    receita_acumulada_ano: receita bruta do ano-calendário, inclusive o PA.
    """

    ano: int
    receita_pa: Decimal
    receitas_anteriores: tuple[Decimal, ...]
    folha_pa: Decimal
    folhas_anteriores: tuple[Decimal, ...]
    receita_acumulada_ano: Decimal
    meses_desde_abertura: int
    meses_atividade_no_ano: int
    atividade: AtividadeSimples
    optante_simples: bool = True

    def __post_init__(self):
        _money("receita_pa", self.receita_pa)
        _money("folha_pa", self.folha_pa)
        _money("receita_acumulada_ano", self.receita_acumulada_ano)
        _money_tuple("receitas_anteriores", self.receitas_anteriores)
        _money_tuple("folhas_anteriores", self.folhas_anteriores)
        for name in ("meses_desde_abertura", "meses_atividade_no_ano"):
            v = getattr(self, name)
            if isinstance(v, bool) or not isinstance(v, int):
                raise TypeError(f"{name} deve ser int.")
        if self.meses_desde_abertura < 1:
            raise ValueError("meses_desde_abertura deve ser >= 1.")
        if not 1 <= self.meses_atividade_no_ano <= 12:
            raise ValueError("meses_atividade_no_ano deve estar entre 1 e 12.")
        if not isinstance(self.atividade, AtividadeSimples):
            raise TypeError("atividade deve ser uma AtividadeSimples.")
        if not isinstance(self.optante_simples, bool):
            raise TypeError("optante_simples deve ser bool.")

        n = len(self.receitas_anteriores)
        if len(self.folhas_anteriores) != n:
            raise ValueError("receitas_anteriores e folhas_anteriores devem ter o mesmo tamanho.")
        if self.meses_desde_abertura < 13:
            if n != self.meses_desde_abertura - 1:
                raise ValueError("Histórico incompatível: esperado meses_desde_abertura - 1 meses anteriores.")
        elif n < 12:
            raise ValueError("Histórico incompatível: empresa com 13+ meses exige ao menos 12 meses anteriores.")
        if self.meses_atividade_no_ano < 12 and self.meses_desde_abertura > self.meses_atividade_no_ano:
            raise ValueError("meses_atividade_no_ano inconsistente com meses_desde_abertura.")
        if self.receita_acumulada_ano < self.receita_pa:
            raise ValueError("receita_acumulada_ano deve incluir a receita do PA.")


class ModoApuracaoLucro(str, Enum):
    """Como a PJ sustenta a distribuição de lucros isenta (LC 123/2006, art. 14)."""

    SEM_ESCRITURACAO = "SEM_ESCRITURACAO"
    COM_ESCRITURACAO = "COM_ESCRITURACAO"


def _opt_money(name, value):
    if value is not None:
        _money(name, value)


@dataclass(frozen=True)
class ProLaboreInput:
    """Pró-labore mensal do sócio único (TR-010)."""

    ano: int
    valor: Decimal

    def __post_init__(self):
        _money("valor", self.valor)


@dataclass(frozen=True)
class DividendosInput:
    """Distribuição de lucros do mês (TR-011), referente a resultados de 2026.

    valor_distribuido: TOTAL do mês pago pela mesma PJ à mesma PF (soma dos pagamentos).
    lucro_contabil_disponivel: informado pelo usuário; obrigatório com escrituração e
    proibido sem escrituração (o simulador não calcula lucro contábil).
    renda_anual_relevante_informada: opcional; só dispara aviso de altas rendas.
    """

    ano: int
    valor_distribuido: Decimal
    modo_apuracao: ModoApuracaoLucro
    lucro_contabil_disponivel: Decimal | None = None
    renda_anual_relevante_informada: Decimal | None = None

    def __post_init__(self):
        _money("valor_distribuido", self.valor_distribuido)
        _opt_money("lucro_contabil_disponivel", self.lucro_contabil_disponivel)
        _opt_money("renda_anual_relevante_informada", self.renda_anual_relevante_informada)
        if not isinstance(self.modo_apuracao, ModoApuracaoLucro):
            raise TypeError("modo_apuracao deve ser um ModoApuracaoLucro.")
        com = self.modo_apuracao is ModoApuracaoLucro.COM_ESCRITURACAO
        if com and self.lucro_contabil_disponivel is None:
            raise ValueError("COM_ESCRITURACAO exige lucro_contabil_disponivel.")
        if not com and self.lucro_contabil_disponivel is not None:
            raise ValueError("lucro_contabil_disponivel só se aplica a COM_ESCRITURACAO.")


@dataclass(frozen=True)
class ComparatorSimulationInput:
    """Mesma receita mensal sob duas estruturas: PF autônomo x PJ (Simples, sócio único, sem empregados)."""

    pf_input: PFSimulationInput
    simples_input: SimplesSimulationInput
    prolabore: Decimal
    dividendos: DividendosInput

    def __post_init__(self):
        for name, cls in (("pf_input", PFSimulationInput), ("simples_input", SimplesSimulationInput),
                          ("dividendos", DividendosInput)):
            if not isinstance(getattr(self, name), cls):
                raise TypeError(f"{name} deve ser {cls.__name__}.")
        _money("prolabore", self.prolabore)
        if len({self.pf_input.ano, self.simples_input.ano, self.dividendos.ano}) != 1:
            raise ValueError("Todos os modelos do comparador devem ter o mesmo ano.")
        if self.pf_input.renda_mensal != self.simples_input.receita_pa:
            raise ValueError("pf_input.renda_mensal deve ser igual a simples_input.receita_pa (mesma receita bruta).")
        if self.simples_input.folha_pa != self.prolabore:
            raise ValueError("No cenário sem empregados, simples_input.folha_pa deve ser igual ao pró-labore.")

    @property
    def ano(self) -> int:
        return self.pf_input.ano


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
