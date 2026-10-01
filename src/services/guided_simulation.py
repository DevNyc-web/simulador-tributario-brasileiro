"""Simulação guiada: monta cenários de evolução de um negócio usando os motores existentes.

Separação de responsabilidades (também exibida ao usuário em "Premissas"):
- CÁLCULO DO MOTOR: DAS, INSS e IRPF do pró-labore, limite do MEI, Fator R e anexo — vêm de src/tax_engine,
  com parâmetros do rules.json. Nada é recalculado aqui.
- PROJEÇÃO: valores mensais repetidos por 12 e 60 meses (sem crescimento, sem inflação).
- SUPOSIÇÃO OPERACIONAL: faturamento = ticket médio x clientes; salários dos cenários com equipe; pró-labore padrão.
Não há cálculo trabalhista (encargos, férias, 13º, descontos do contracheque): fora do escopo desta fase.
"""
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from src.models.tax import (
    AtividadeSimples,
    CategoriaMEI,
    MEISimulationInput,
    ProLaboreInput,
    SimplesSimulationInput,
    SimulationResult,
    SimulationStatus,
    StatusLimiteMEI,
)
from src.services.presentation import ATIVIDADE_LABELS, ANEXO_LABELS, CATEGORIA_LABELS, brl, pct
from src.tax_engine.mei_2026 import calculate_mei_2026, calculate_mei_limit_2026
from src.tax_engine.pf_2026 import ANO
from src.tax_engine.prolabore_2026 import calculate_prolabore_2026
from src.tax_engine.simples_2026 import SimplesComputation, run_simples_2026
from src.tax_rules import get_rule, parse_decimal

ZERO = Decimal(0)
MESES_12 = 12
MESES_60 = 60

TIPO_MOTOR = "Cálculo do motor"
TIPO_PROJECAO = "Projeção"
TIPO_SUPOSICAO = "Premissa operacional"


class EnquadramentoGuiado(str, Enum):
    MEI = "MEI"
    SIMPLES = "SIMPLES"


class StatusCenario(str, Enum):
    OK = "OK"
    INCOMPATIVEL_MEI = "INCOMPATIVEL_MEI"
    NAO_SUPORTADO = "NAO_SUPORTADO"


ENQUADRAMENTO_LABELS = {EnquadramentoGuiado.MEI: "MEI", EnquadramentoGuiado.SIMPLES: "Simples Nacional"}

# Premissa operacional: múltiplos do salário mínimo de cada função nos cenários com equipe.
CENARIOS = (
    ("base", "Sem funcionário", ()),
    ("f1", "+1 funcionário", (1,)),
    ("f2", "+2 funcionários", (1, 1)),
    ("f2g", "+2 funcionários + gerente", (1, 1, 2)),
)


@dataclass(frozen=True)
class GuidedInput:
    enquadramento: EnquadramentoGuiado
    categoria_mei: CategoriaMEI | None
    atividade: AtividadeSimples | None
    ticket_medio: Decimal
    clientes_mes: int
    meses_atividade_no_ano: int = 12
    prolabore: Decimal | None = None  # None = 1 salário mínimo (suposição operacional)
    optante_simei: bool = True

    def __post_init__(self):
        if not isinstance(self.ticket_medio, Decimal) or not self.ticket_medio.is_finite() or self.ticket_medio < 0:
            raise ValueError("ticket_medio deve ser um Decimal não negativo.")
        if isinstance(self.clientes_mes, bool) or not isinstance(self.clientes_mes, int) or self.clientes_mes < 0:
            raise ValueError("clientes_mes deve ser um inteiro não negativo.")
        if not 1 <= self.meses_atividade_no_ano <= 12:
            raise ValueError("meses_atividade_no_ano deve estar entre 1 e 12.")
        if self.prolabore is not None and (not isinstance(self.prolabore, Decimal) or self.prolabore < 0):
            raise ValueError("prolabore deve ser um Decimal não negativo.")
        if self.enquadramento is EnquadramentoGuiado.MEI and self.categoria_mei is None:
            raise ValueError("MEI exige categoria.")
        if self.enquadramento is EnquadramentoGuiado.SIMPLES and self.atividade is None:
            raise ValueError("Simples Nacional exige atividade.")


@dataclass(frozen=True)
class ItemImposto:
    rotulo: str
    valor: Decimal
    explicacao: str


@dataclass(frozen=True)
class Cenario:
    id: str
    rotulo: str
    funcionarios: int
    tem_gerente: bool
    salarios_mensais: Decimal
    status: StatusCenario
    motivo: str | None = None
    faturamento: Decimal | None = None
    tributos_empresa: Decimal | None = None  # DAS
    tributos_socio: Decimal | None = None  # INSS + IRPF do pró-labore (Simples)
    custo_pessoal: Decimal | None = None  # salários brutos dos funcionários (sem encargos)
    sobra_mensal: Decimal | None = None
    anexo: str | None = None
    aliquota_efetiva: Decimal | None = None
    itens: tuple[ItemImposto, ...] = ()

    @property
    def ok(self) -> bool:
        return self.status is StatusCenario.OK

    @property
    def tributos_totais(self) -> Decimal | None:
        return None if not self.ok else self.tributos_empresa + self.tributos_socio

    def acumulado(self, meses: int, campo: str) -> Decimal | None:
        valor = getattr(self, campo)
        return None if not self.ok or valor is None else valor * meses

    @property
    def tributos_12m(self) -> Decimal | None:
        return self.acumulado_total(MESES_12)

    @property
    def tributos_60m(self) -> Decimal | None:
        return self.acumulado_total(MESES_60)

    def acumulado_total(self, meses: int) -> Decimal | None:
        return None if not self.ok else self.tributos_totais * meses

    @property
    def sobra_12m(self) -> Decimal | None:
        return self.acumulado(MESES_12, "sobra_mensal")

    @property
    def sobra_60m(self) -> Decimal | None:
        return self.acumulado(MESES_60, "sobra_mensal")


@dataclass(frozen=True)
class Barra:
    rotulo: str
    valor: Decimal | None
    pct: Decimal  # largura relativa (apresentação)
    negativo: bool
    nota: str | None = None


@dataclass(frozen=True)
class GuidedResult:
    entrada: GuidedInput
    faturamento_mensal: Decimal
    salario_minimo: Decimal
    prolabore_usado: Decimal | None
    cenarios: tuple[Cenario, ...]
    premissas: tuple[tuple[str, str], ...]
    aviso_principal: str | None

    @property
    def faturamento_12m(self) -> Decimal:
        return self.faturamento_mensal * MESES_12

    @property
    def faturamento_60m(self) -> Decimal:
        return self.faturamento_mensal * MESES_60

    @property
    def base(self) -> Cenario:
        return self.cenarios[0]

    def _barras(self, getter, rotulo_fn=lambda c: c.rotulo) -> tuple[Barra, ...]:
        valores = [getter(c) for c in self.cenarios]
        maximo = max((abs(v) for v in valores if v is not None), default=ZERO)
        barras = []
        for c, v in zip(self.cenarios, valores):
            if v is None:
                barras.append(Barra(rotulo_fn(c), None, ZERO, False, c.motivo))
            else:
                p = ZERO if maximo == 0 else abs(v) / maximo * 100
                barras.append(Barra(rotulo_fn(c), v, p, v < 0))
        return tuple(barras)

    @property
    def barras_sobra_mensal(self) -> tuple[Barra, ...]:
        return self._barras(lambda c: c.sobra_mensal if c.ok else None)

    @property
    def barras_horizonte(self) -> tuple[Barra, ...]:
        """Lucro do cenário base: mês, 12 meses e 60 meses (projeção)."""
        b = self.base
        if not b.ok:
            return ()
        itens = (("1 mês", b.sobra_mensal), ("12 meses", b.sobra_12m), ("60 meses", b.sobra_60m))
        maximo = max(abs(v) for _, v in itens)
        return tuple(
            Barra(r, v, ZERO if maximo == 0 else abs(v) / maximo * 100, v < 0) for r, v in itens
        )

    @property
    def composicao_base(self) -> tuple[Barra, ...]:
        """Como o faturamento do cenário base se divide (apresentação)."""
        b = self.base
        if not b.ok or self.faturamento_mensal <= 0:
            return ()
        fat = self.faturamento_mensal
        partes = (
            ("Tributos", b.tributos_totais),
            ("Pessoal", b.custo_pessoal),
            ("Sobra operacional estimada", max(b.sobra_mensal, ZERO)),
        )
        return tuple(Barra(r, v, v / fat * 100, False) for r, v in partes)


def _salario_minimo() -> Decimal:
    return parse_decimal(get_rule(ANO, "TR-002").parametros["salario_minimo"])


def _incompativel_mei(rotulo, funcionarios, tem_gerente, salarios, motivo) -> Cenario:
    return Cenario(rotulo[0], rotulo[1], funcionarios, tem_gerente, salarios, StatusCenario.INCOMPATIVEL_MEI, motivo)


def _cenario_mei(entrada: GuidedInput, fat: Decimal, definicao, multiplos, sm: Decimal) -> Cenario:
    p = get_rule(ANO, "TR-003").parametros
    max_emp = int(parse_decimal(p["maximo_empregados"]))
    n = len(multiplos)
    gerente = len(multiplos) > 0 and max(multiplos) > 1
    salarios = sum((sm * m for m in multiplos), ZERO)
    base = (definicao[0], definicao[1])
    entrada_mei = MEISimulationInput(
        ANO, fat * entrada.meses_atividade_no_ano, entrada.categoria_mei,
        entrada.meses_atividade_no_ano, entrada.optante_simei,
    )
    res: SimulationResult = calculate_mei_2026(entrada_mei)
    if res.status is not SimulationStatus.OK:  # ex.: não optante pelo SIMEI
        return Cenario(base[0], base[1], n, gerente, salarios, StatusCenario.NAO_SUPORTADO, res.warnings[0])
    if n > max_emp:
        return _incompativel_mei(
            base, n, gerente, salarios,
            f"Não cabe no MEI: o MEI pode ter no máximo {max_emp} empregado (LC 123/2006, art. 18-C). "
            "Nesse porte, avalie o Simples Nacional.",
        )
    limite = calculate_mei_limit_2026(entrada_mei.receita_acumulada, entrada.meses_atividade_no_ano)
    if limite.status is not StatusLimiteMEI.COMPATIVEL:
        return _incompativel_mei(
            base, n, gerente, salarios,
            f"Receita estimada no ano ({brl(entrada_mei.receita_acumulada)}) acima do limite do MEI "
            f"({brl(limite.limite_aplicavel)}). Nesse porte, avalie o Simples Nacional.",
        )
    das = res.total_tributos
    return Cenario(
        base[0], base[1], n, gerente, salarios, StatusCenario.OK, None, fat, das, ZERO, salarios,
        fat - das - salarios, None, None,
        (ItemImposto("DAS-MEI", das, "Guia mensal fixa (previdência + ICMS/ISS): não muda com o faturamento."),),
    )


def _cenario_simples(entrada: GuidedInput, fat: Decimal, definicao, multiplos, sm: Decimal, prolabore: Decimal) -> Cenario:
    n = len(multiplos)
    gerente = n > 0 and max(multiplos) > 1
    salarios = sum((sm * m for m in multiplos), ZERO)
    folha = prolabore + salarios  # folha do Fator R: pró-labore + salários
    m = entrada.meses_atividade_no_ano
    simples_in = SimplesSimulationInput(
        ano=ANO, receita_pa=fat, receitas_anteriores=(fat,) * (m - 1), folha_pa=folha,
        folhas_anteriores=(folha,) * (m - 1), receita_acumulada_ano=fat * m,
        meses_desde_abertura=m, meses_atividade_no_ano=m, atividade=entrada.atividade,
    )
    comp = run_simples_2026(simples_in)
    if not isinstance(comp, SimplesComputation):
        status = StatusCenario.NAO_SUPORTADO
        return Cenario(definicao[0], definicao[1], n, gerente, salarios, status, comp.warnings[0])
    pl = calculate_prolabore_2026(ProLaboreInput(ANO, prolabore))
    socio = pl.inss + pl.irpf
    anexo = ANEXO_LABELS[comp.fator.anexo]
    itens = (
        ItemImposto("DAS do Simples Nacional", comp.das,
                    f"Guia mensal única sobre o faturamento: {anexo}, alíquota efetiva de {pct(comp.eficaz.aliquota)}."),
        ItemImposto("INSS do pró-labore", pl.inss, "Contribuição previdenciária do sócio sobre o pró-labore."),
        ItemImposto("IRPF do pró-labore", pl.irpf, "Imposto de renda mensal do sócio sobre o pró-labore (regras de 2026)."),
    )
    return Cenario(
        definicao[0], definicao[1], n, gerente, salarios, StatusCenario.OK, None, fat, comp.das, socio, salarios,
        fat - comp.das - socio - salarios, anexo, comp.eficaz.aliquota, itens,
    )


def simulate_guided(entrada: GuidedInput) -> GuidedResult:
    sm = _salario_minimo()
    fat = entrada.ticket_medio * entrada.clientes_mes
    mei = entrada.enquadramento is EnquadramentoGuiado.MEI
    prolabore = None if mei else (entrada.prolabore if entrada.prolabore is not None else sm)

    cenarios = tuple(
        _cenario_mei(entrada, fat, d, d[2], sm) if mei
        else _cenario_simples(entrada, fat, d, d[2], sm, prolabore)
        for d in CENARIOS
    )

    premissas = [
        (TIPO_SUPOSICAO, "Faturamento mensal = ticket médio × clientes por mês, constante (sem crescimento)."),
        (TIPO_MOTOR, "Tributos calculados pelo motor com as regras de 2026 (TR-001 a TR-011)."),
        (TIPO_PROJECAO, "As projeções de 12 e 60 meses são aritméticas (valor mensal × 12 e × 60). Mantêm constantes "
                        "o ticket médio, os clientes, a estrutura do cenário, as premissas operacionais e as regras-base "
                        "de 2026. Não representam cálculo tributário definitivo para os anos seguintes: as regras "
                        "futuras podem mudar durante o período."),
        (TIPO_SUPOSICAO, f"Premissa operacional da simulação (não é regra legal de remuneração): funcionário = 1 salário "
                         f"mínimo ({brl(sm)}) e gerente = 2 salários mínimos. Salários brutos, sem cálculo trabalhista "
                         "completo: o custo real é maior."),
        (TIPO_SUPOSICAO, "“Sobra operacional estimada” = faturamento − tributos modelados − salários brutos. Não inclui "
                         "despesas operacionais (aluguel, insumos, marketing, custos fixos), encargos trabalhistas, férias, "
                         "13º, FGTS, benefícios, capital de giro nem a tributação completa da distribuição de lucros. "
                         "O valor potencialmente disponível antes da distribuição é, portanto, menor."),
    ]
    if mei:
        premissas.append((TIPO_MOTOR, "MEI: DAS fixo e limite anual de receita conforme as regras de 2026."))
        premissas.append((TIPO_MOTOR, "Regra legal do MEI: no máximo 1 empregado, remunerado com um salário mínimo ou o piso "
                                      "salarial da categoria (LC 123/2006, art. 18-C). A simulação adota 1 salário mínimo "
                                      "como hipótese do cenário."))
        premissas.append((TIPO_SUPOSICAO, "Obrigações adicionais do MEI com empregado não foram modeladas."))
    else:
        premissas.append((TIPO_SUPOSICAO, f"Pró-labore {'informado' if entrada.prolabore is not None else 'padrão de 1 salário mínimo'}: "
                                          f"{brl(prolabore)}; folha do Fator R = pró-labore + salários, em regime estável "
                                          "(meses anteriores iguais ao atual)."))
        premissas.append((TIPO_MOTOR, "No Simples, mais folha pode alterar o Fator R e, com ele, o anexo e a alíquota."))

    aviso = None
    problemas = [c for c in cenarios if not c.ok]
    if problemas:
        if not cenarios[0].ok:
            aviso = cenarios[0].motivo
        elif mei:
            aviso = "Com equipe, alguns cenários deixam de caber no MEI (veja o quadro da equipe)."
        else:
            aviso = problemas[0].motivo

    return GuidedResult(
        entrada, fat, sm, prolabore, cenarios, tuple(premissas), aviso,
    )


def rotulo_ramo(entrada: GuidedInput) -> str:
    if entrada.enquadramento is EnquadramentoGuiado.MEI:
        return CATEGORIA_LABELS[entrada.categoria_mei]
    return ATIVIDADE_LABELS[entrada.atividade]
