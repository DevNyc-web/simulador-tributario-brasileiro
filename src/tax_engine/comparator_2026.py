"""Comparador PF x PJ 2026: compõe os motores existentes, sem recalcular nada.

PF: calculate_pf_2026. PJ: run_simples_2026 + TR-010 (pró-labore) + TR-011 (dividendos).
Apresenta apenas números e diferenças aritméticas; nunca classifica uma estrutura como
melhor/pior nem recomenda.
"""
from dataclasses import dataclass
from decimal import Decimal

from src.models.tax import (
    ComparatorSimulationInput,
    ExplanationItem,
    ProLaboreInput,
    SimulationResult,
    SimulationStatus,
    TaxItem,
)

from .dividendos_2026 import calculate_dividendos_2026, calculate_irpj_no_das_2026
from .pf_2026 import ANO, calculate_pf_2026
from .prolabore_2026 import calculate_prolabore_2026
from .simples_2026 import run_simples_2026

SEM_RESULTADO_PARCIAL = "Cenário PJ sem cálculo: o comparador não apresenta resultado parcial."


@dataclass(frozen=True)
class ComparatorPF:
    receita: Decimal
    inss: Decimal
    irpf: Decimal
    total_tributos: Decimal
    liquido_pessoal: Decimal


@dataclass(frozen=True)
class ComparatorPJ:
    faturamento: Decimal
    das: Decimal
    inss_prolabore: Decimal
    irpf_prolabore: Decimal
    irrf_dividendos: Decimal
    total_tributos: Decimal  # DAS + INSS + IRPF do pró-labore + IRRF dos dividendos (dividendo não é tributo)
    prolabore_liquido: Decimal
    dividendos_liquidos: Decimal
    recebido_pela_pf: Decimal  # valor recebido pela pessoa física no cenário PJ (não é "líquido econômico da PJ")


@dataclass(frozen=True)
class ComparatorResult:
    status: SimulationStatus
    pf: ComparatorPF | None = None
    pj: ComparatorPJ | None = None
    diferenca_tributos: Decimal | None = None  # total_tributos_pj - total_tributos_pf (aritmético, sem juízo)
    diferenca_recebimento_pessoal: Decimal | None = None  # recebido_pela_pf_no_PJ - liquido_pessoal_PF
    warnings: tuple[str, ...] = ()


def compare_pf_pj_2026(entrada: ComparatorSimulationInput) -> ComparatorResult:
    if entrada.ano != ANO:
        raise ValueError(f"O comparador só suporta {ANO}.")
    pf = calculate_pf_2026(entrada.pf_input)

    simples = run_simples_2026(entrada.simples_input)
    if isinstance(simples, SimulationResult):
        return ComparatorResult(simples.status, warnings=simples.warnings + (SEM_RESULTADO_PARCIAL,))

    receita = entrada.simples_input.receita_pa
    prolabore = calculate_prolabore_2026(ProLaboreInput(entrada.ano, entrada.prolabore))
    irpj = calculate_irpj_no_das_2026(simples.fator.anexo, simples.faixa.numero, simples.eficaz.aliquota, receita)
    div = calculate_dividendos_2026(entrada.dividendos, receita_pa=receita, irpj_no_das=irpj)
    if div.status is not SimulationStatus.OK:
        return ComparatorResult(div.status, warnings=div.warnings + (SEM_RESULTADO_PARCIAL,))

    pf_m = ComparatorPF(receita, pf.itens[0].valor, pf.itens[1].valor, pf.total_tributos, pf.liquido_estimado)
    total_pj = simples.das + prolabore.inss + prolabore.irpf + div.irrf
    recebido = prolabore.liquido + div.liquido
    pj_m = ComparatorPJ(
        receita, simples.das, prolabore.inss, prolabore.irpf, div.irrf, total_pj,
        prolabore.liquido, div.liquido, recebido,
    )

    warnings = [
        "Ferramenta educacional: apresenta diferenças numéricas e não recomenda estrutura alguma.",
        "Cenário PJ: Simples Nacional (Anexo III/V), sócio único, sem empregados, sem CPP patronal "
        "adicional (já incluída no DAS).",
        "O valor recebido pela pessoa física no cenário PJ não é lucro líquido nem líquido econômico da "
        "empresa: podem existir lucro retido, despesas, caixa e capital de giro.",
        "Premissas do Simples (um estabelecimento, sem exportação, ST, monofásico, retenção de ISS ou "
        "benefícios) e DAS sem arredondamento (política em aberto).",
    ]
    if entrada.simples_input.atividade.value in ("MEDICINA", "ODONTOLOGIA"):
        warnings.append("Medicina/odontologia: apenas atendimento profissional comum; serviços hospitalares "
                        "e de auxílio diagnóstico/terapia estão fora do MVP.")
    if prolabore.bruto + div.bruto + simples.das > receita:
        warnings.append("Pró-labore, dividendos e DAS informados somam mais que o faturamento do mês; "
                        "verifique os valores (o simulador não presume lucro).")
    warnings += prolabore.warnings + div.warnings
    return ComparatorResult(
        SimulationStatus.OK, pf_m, pj_m,
        total_pj - pf_m.total_tributos, recebido - pf_m.liquido_pessoal, tuple(warnings),
    )


def calculate_comparator_2026(entrada: ComparatorSimulationInput) -> SimulationResult:
    """Adapta ComparatorResult ao contrato SimulationResult (itens + explicações)."""
    r = compare_pf_pj_2026(entrada)
    if r.status is not SimulationStatus.OK:
        return SimulationResult(r.status, ANO, "comparar", None, None, warnings=r.warnings)
    pf, pj = r.pf, r.pj
    itens = tuple(TaxItem(c, d, v, None, None) for c, d, v in (
        ("PF_INSS", "PF: INSS do autônomo", pf.inss),
        ("PF_IRPF", "PF: IRPF mensal", pf.irpf),
        ("PF_TOTAL_TRIBUTOS", "PF: total de tributos", pf.total_tributos),
        ("PJ_DAS", "PJ: DAS do Simples Nacional", pj.das),
        ("PJ_INSS_PROLABORE", "PJ: INSS do pró-labore", pj.inss_prolabore),
        ("PJ_IRPF_PROLABORE", "PJ: IRPF do pró-labore", pj.irpf_prolabore),
        ("PJ_IRRF_DIVIDENDOS", "PJ: IRRF sobre dividendos", pj.irrf_dividendos),
        ("PJ_TOTAL_TRIBUTOS", "PJ: total de tributos", pj.total_tributos),
    ))
    explicacoes = (
        ExplanationItem(
            "Valor recebido pela pessoa física",
            f"PF: {pf.liquido_pessoal}. Cenário PJ (pró-labore líquido {pj.prolabore_liquido} + "
            f"dividendos líquidos {pj.dividendos_liquidos}): {pj.recebido_pela_pf}.",
            None,
        ),
        ExplanationItem(
            "Diferenças aritméticas (sem juízo de valor)",
            f"Tributos PJ - PF: {r.diferenca_tributos}. Valor recebido PJ - PF: {r.diferenca_recebimento_pessoal}.",
            None,
        ),
    )
    return SimulationResult(SimulationStatus.OK, ANO, "comparar", None, None, itens, explicacoes, r.warnings)
