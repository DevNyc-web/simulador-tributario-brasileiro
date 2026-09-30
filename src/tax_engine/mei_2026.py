"""Motor MEI 2026: TR-003 (limite de receita) e TR-004 (DAS-MEI).

O código contém só fórmula; todo parâmetro fiscal vem de rules.json (get_rule).
Decimal exato, sem float e sem arredondamento de cálculo (Q-02 é decisão
técnica em aberto também para o motor PF).
"""
from dataclasses import dataclass
from decimal import Decimal

from src.models.tax import (
    CategoriaMEI,
    ExplanationItem,
    MEISimulationInput,
    SimulationResult,
    SimulationStatus,
    StatusLimiteMEI,
    TaxItem,
)
from src.tax_rules import get_rule, parse_decimal

ANO = 2026
UM = Decimal(1)


@dataclass(frozen=True)
class LimiteMEIResult:
    limite_aplicavel: Decimal
    limite_com_tolerancia: Decimal
    percentual_utilizado: Decimal
    status: StatusLimiteMEI


@dataclass(frozen=True)
class DASMEIResult:
    previdencia: Decimal
    icms: Decimal
    iss: Decimal
    total: Decimal


def calculate_mei_limit_2026(receita: Decimal, meses_atividade: int) -> LimiteMEIResult:
    p = get_rule(ANO, "TR-003").parametros
    anual = parse_decimal(p["limite_anual"])
    mensal = parse_decimal(p["limite_proporcional_mensal"])
    tolerancia = parse_decimal(p["percentual_excesso_tolerado"])

    # 12 meses = MEI enquadrado desde janeiro (limite anual); senão, proporcional.
    limite = anual if meses_atividade == 12 else mensal * meses_atividade
    com_tolerancia = limite * (UM + tolerancia)

    if receita <= limite:
        status = StatusLimiteMEI.COMPATIVEL
    elif receita <= com_tolerancia:  # "em mais de 20%": exatamente 20% ainda não é superior
        status = StatusLimiteMEI.EXCESSO_ATE_20
    else:
        status = StatusLimiteMEI.EXCESSO_MAIS_20
    return LimiteMEIResult(limite, com_tolerancia, receita / limite, status)


def calculate_das_mei_2026(categoria: CategoriaMEI) -> DASMEIResult:
    """DAS fixo mensal: independe da receita (inclusive receita zero)."""
    p = get_rule(ANO, "TR-004").parametros
    previdencia = parse_decimal(p["salario_minimo"]) * parse_decimal(p["percentual_previdenciario"])
    icms = parse_decimal(p["parcela_icms"]) if categoria is not CategoriaMEI.SERVICOS else Decimal(0)
    iss = parse_decimal(p["parcela_iss"]) if categoria is not CategoriaMEI.COMERCIO_INDUSTRIA else Decimal(0)
    return DASMEIResult(previdencia, icms, iss, previdencia + icms + iss)


def calculate_mei_2026(entrada: MEISimulationInput) -> SimulationResult:
    if entrada.ano != ANO:
        raise ValueError(f"calculate_mei_2026 só suporta {ANO}.")
    if not entrada.optante_simei:
        return SimulationResult(
            status=SimulationStatus.NAO_SUPORTADO,
            ano=ANO,
            tipo_simulacao="mei",
            total_tributos=None,
            liquido_estimado=None,
            warnings=("O cálculo do MVP considera MEI enquadrado no SIMEI. Baixa, desenquadramento já efetivado "
                      "ou período posterior ao encerramento não são calculados nesta versão.",),
        )

    limite = calculate_mei_limit_2026(entrada.receita_acumulada, entrada.meses_atividade_no_ano)
    das = calculate_das_mei_2026(entrada.categoria)

    partes = [f"previdência {das.previdencia}"]
    if das.icms:
        partes.append(f"ICMS {das.icms}")
    if das.iss:
        partes.append(f"ISS {das.iss}")

    warnings = [
        "Ferramenta educacional: não substitui orientação contábil ou jurídica.",
        "Pressupõe ocupação permitida para MEI (Anexo XI da Resolução CGSN nº 140/2018); "
        "a elegibilidade não é verificada.",
    ]
    if limite.status is StatusLimiteMEI.EXCESSO_ATE_20:
        warnings.append(
            "Receita acima do limite, mas sem superar 20% dele: a legislação prevê efeitos do "
            "desenquadramento a partir de 1º de janeiro do ano seguinte, com recolhimento da "
            "diferença do DAS sem acréscimos (LC 123/2006, art. 18-A, §§ 7º e 10). "
            "Este valor não é calculado pelo MVP."
        )
    elif limite.status is StatusLimiteMEI.EXCESSO_MAIS_20:
        inicio = "1º de janeiro do ano do excesso" if entrada.meses_atividade_no_ano == 12 else "o início da atividade"
        warnings.append(
            f"Receita superior ao limite em mais de 20%: a legislação prevê efeitos retroativos a "
            f"{inicio} (LC 123/2006, art. 18-A, § 7º). O cálculo retroativo não é realizado pelo MVP."
        )

    return SimulationResult(
        status=SimulationStatus.OK,
        ano=ANO,
        tipo_simulacao="mei",
        total_tributos=das.total,
        liquido_estimado=None,  # receita_acumulada é anual; o DAS é mensal — não há líquido coerente
        itens=(TaxItem("DAS-MEI", "DAS mensal fixo do MEI", das.total, None, None),),
        explicacoes=(
            ExplanationItem(
                "Limite de receita",
                f"Limite aplicável: {limite.limite_aplicavel} ({entrada.meses_atividade_no_ano} mês(es) "
                f"de atividade no ano). Receita acumulada: {entrada.receita_acumulada} "
                f"({limite.percentual_utilizado:.2%} do limite). Situação: {limite.status.value}.",
                "TR-003",
            ),
            ExplanationItem(
                "Composição do DAS-MEI",
                f"Categoria {entrada.categoria.value}: " + " + ".join(partes)
                + f" = {das.total} por mês, valor fixo independente da receita.",
                "TR-004",
            ),
        ),
        warnings=tuple(warnings),
    )
