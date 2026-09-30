"""Motor Simples Nacional 2026 (Anexo III/V com Fator R): TR-005 a TR-009.

O código contém só fórmula; todo parâmetro fiscal vem de rules.json (get_rule).
Decimal exato, sem float. Sem arredondamento no DAS (Q-SN-04 em aberto); a única
operação de truncamento é a do Fator R (duas casas, sem arredondar; TR-009).
"""
from dataclasses import dataclass
from decimal import ROUND_DOWN, Decimal

from src.models.tax import (
    AnexoSimples,
    ExplanationItem,
    SimplesSimulationInput,
    SimulationResult,
    SimulationStatus,
    StatusSimples,
    TaxItem,
)
from src.tax_rules import get_rule, parse_decimal

ANO = 2026
MESES_ANO = 12  # definição de RBT12 (doze meses) e anualização da RBT12p
MESES_MATURIDADE = MESES_ANO + 1  # 13+ meses: usa RBT12 (12 meses anteriores)


class FatorRIndefinidoError(ValueError):
    """Combinação de zeros que a pesquisa validada não define (1º mês, folha = receita = 0)."""


@dataclass(frozen=True)
class RBTResult:
    valor: Decimal
    proporcionalizada: bool  # True = RBT12p (empresa com menos de 13 meses)


@dataclass(frozen=True)
class LimiteSimplesResult:
    limite_aplicavel: Decimal
    sublimite: Decimal
    status: StatusSimples


@dataclass(frozen=True)
class FatorRResult:
    fator: Decimal  # já truncado em duas casas
    anexo: AnexoSimples


@dataclass(frozen=True)
class FaixaResult:
    numero: int  # 1-based
    aliquota_nominal: Decimal
    parcela_deduzir: Decimal


@dataclass(frozen=True)
class AliquotaEfetivaResult:
    base_rbt: Decimal  # RBT12/RBT12p efetivamente usada na fórmula
    aliquota: Decimal


def calculate_rbt12_2026(receitas_anteriores: tuple[Decimal, ...]) -> Decimal:
    """RBT12: soma dos 12 meses imediatamente anteriores ao PA (o PA não entra)."""
    return sum(receitas_anteriores[-MESES_ANO:], Decimal(0))


def calculate_rbt12p_2026(receita_pa: Decimal, receitas_anteriores: tuple[Decimal, ...]) -> Decimal:
    """RBT12p (menos de 13 meses): 1º mês = receita do PA x 12; demais = média dos
    meses anteriores ao PA x 12 (o PA não entra)."""
    if not receitas_anteriores:
        return receita_pa * MESES_ANO
    return sum(receitas_anteriores, Decimal(0)) / len(receitas_anteriores) * MESES_ANO


def calculate_rbt_2026(entrada: SimplesSimulationInput) -> RBTResult:
    if entrada.meses_desde_abertura >= MESES_MATURIDADE:
        return RBTResult(calculate_rbt12_2026(entrada.receitas_anteriores), False)
    return RBTResult(calculate_rbt12p_2026(entrada.receita_pa, entrada.receitas_anteriores), True)


def calculate_simples_limit_2026(
    receita_acumulada_ano: Decimal, meses_atividade_no_ano: int, rbt: Decimal
) -> LimiteSimplesResult:
    """Limite de permanência (receita do ano) — independente da faixa tributária.

    `rbt` (RBT12/RBT12p) só serve para o teto legal e o sublimite funcional do MVP.
    """
    p = get_rule(ANO, "TR-005").parametros
    geral = parse_decimal(p["limite_geral"])
    mensal = parse_decimal(p["limite_proporcional_mensal"])
    sublimite = parse_decimal(p["sublimite_icms_iss"])

    # 12 meses = empresa já existente (limite geral); senão, proporcional (abertura no ano).
    limite = geral if meses_atividade_no_ano == MESES_ANO else mensal * meses_atividade_no_ano
    if receita_acumulada_ano > limite or rbt > geral:
        status = StatusSimples.FORA_LIMITE_SIMPLES
    elif rbt > sublimite:
        status = StatusSimples.ACIMA_SUBLIMITE_MVP
    else:
        status = StatusSimples.COMPATIVEL
    return LimiteSimplesResult(limite, sublimite, status)


def calculate_fator_r_2026(folha: Decimal, receita: Decimal, *, primeiro_mes: bool) -> FatorRResult:
    """Fator R = folha / receita, truncado em duas casas (sem arredondar).

    Primeiro mês: folha/receita = FSPA/RPA. Demais: FS12/RBT12 (13+ meses) ou
    folha/receita acumuladas desde a abertura até o mês anterior ao PA.
    Zeros: folha = 0 (receita > 0 ou, fora do 1º mês, também receita = 0) -> fator
    de folha zero; folha > 0 e receita = 0 -> fator de receita zero. No 1º mês,
    folha = receita = 0 não é definido pela pesquisa -> FatorRIndefinidoError.
    """
    p = get_rule(ANO, "TR-009").parametros
    corte = parse_decimal(p["corte"])
    if receita == 0:
        if folha > 0:
            fator = parse_decimal(p["fator_folha_positiva_receita_zero"])
        elif primeiro_mes:
            raise FatorRIndefinidoError("Fator R indefinido: 1º mês com folha e receita iguais a zero.")
        else:
            fator = parse_decimal(p["fator_folha_zero"])
    elif folha == 0:
        fator = parse_decimal(p["fator_folha_zero"])
    else:
        fator = (folha / receita).quantize(parse_decimal(p["precisao"]), rounding=ROUND_DOWN)
    return FatorRResult(fator, AnexoSimples.III if fator >= corte else AnexoSimples.V)


def fator_r_inputs_2026(entrada: SimplesSimulationInput) -> tuple[Decimal, Decimal, bool]:
    """(folha, receita, primeiro_mes) do Fator R — mecanismo distinto da RBT12p."""
    if entrada.meses_desde_abertura == 1:
        return entrada.folha_pa, entrada.receita_pa, True
    if entrada.meses_desde_abertura >= MESES_MATURIDADE:
        return calculate_rbt12_2026(entrada.folhas_anteriores), calculate_rbt12_2026(entrada.receitas_anteriores), False
    return sum(entrada.folhas_anteriores, Decimal(0)), sum(entrada.receitas_anteriores, Decimal(0)), False


def select_tax_bracket(rbt: Decimal, faixas: list[dict]) -> FaixaResult:
    """Seleciona a faixa (limite superior inclusivo) de qualquer anexo."""
    for i, faixa in enumerate(faixas, start=1):
        if rbt <= parse_decimal(faixa["limite_superior"]):
            return FaixaResult(i, parse_decimal(faixa["aliquota_nominal"]), parse_decimal(faixa["parcela_deduzir"]))
    raise ValueError("RBT12/RBT12p acima da última faixa da tabela.")


def calculate_effective_rate(rbt: Decimal, faixa: FaixaResult) -> AliquotaEfetivaResult:
    """((RBT x alíquota nominal) - PD) / RBT; RBT = 0 é substituída pelo valor de TR-008."""
    base = rbt if rbt > 0 else parse_decimal(get_rule(ANO, "TR-008").parametros["rbt12_substituto_quando_zero"])
    return AliquotaEfetivaResult(base, (base * faixa.aliquota_nominal - faixa.parcela_deduzir) / base)


def _anexo_faixas(anexo: AnexoSimples) -> list[dict]:
    rule_id = "TR-006" if anexo is AnexoSimples.III else "TR-007"
    return get_rule(ANO, rule_id).parametros["faixas"]


def _pendente(status: SimulationStatus, warnings: tuple[str, ...]) -> SimulationResult:
    return SimulationResult(
        status=status, ano=ANO, tipo_simulacao="simples",
        total_tributos=None, liquido_estimado=None, warnings=warnings,
    )


def calculate_simples_2026(entrada: SimplesSimulationInput) -> SimulationResult:
    if entrada.ano != ANO:
        raise ValueError(f"calculate_simples_2026 só suporta {ANO}.")
    if not entrada.optante_simples:
        return _pendente(SimulationStatus.NAO_SUPORTADO, (
            "O cálculo do MVP considera empresa optante pelo Simples Nacional.",
        ))

    rbt = calculate_rbt_2026(entrada)
    limite = calculate_simples_limit_2026(entrada.receita_acumulada_ano, entrada.meses_atividade_no_ano, rbt.valor)
    if limite.status is StatusSimples.FORA_LIMITE_SIMPLES:
        return _pendente(SimulationStatus.INCOMPATIVEL, (
            f"Receita acima do limite de permanência no Simples Nacional aplicável ({limite.limite_aplicavel}) "
            "ou RBT12/RBT12p acima do limite geral: cenário incompatível com o regime. "
            "Excesso e desenquadramento não são calculados pelo MVP.",
        ))
    if limite.status is StatusSimples.ACIMA_SUBLIMITE_MVP:
        return _pendente(SimulationStatus.NAO_SUPORTADO, (
            f"RBT12/RBT12p acima do sublimite de ICMS/ISS ({limite.sublimite}): a empresa ainda pode "
            "permanecer no Simples Nacional até o limite legal, mas o cálculo integral não é suportado "
            "pelo MVP porque o ISS passa a ser apurado fora do DAS.",
        ))

    folha, receita_fr, primeiro_mes = fator_r_inputs_2026(entrada)
    try:
        fator = calculate_fator_r_2026(folha, receita_fr, primeiro_mes=primeiro_mes)
    except FatorRIndefinidoError as exc:
        return _pendente(SimulationStatus.NAO_SUPORTADO, (
            f"{exc} A pesquisa validada não define esse caso; o anexo não pode ser escolhido.",
        ))

    faixa = select_tax_bracket(rbt.valor, _anexo_faixas(fator.anexo))
    eficaz = calculate_effective_rate(rbt.valor, faixa)
    das = entrada.receita_pa * eficaz.aliquota

    nome_rbt = "RBT12p (proporcionalizada, empresa com menos de 13 meses)" if rbt.proporcionalizada else "RBT12"
    return SimulationResult(
        status=SimulationStatus.OK,
        ano=ANO,
        tipo_simulacao="simples",
        total_tributos=das,
        liquido_estimado=None,  # depende de custos/pró-labore, fora desta fase (TR-010/TR-011)
        itens=(TaxItem("DAS_SIMPLIFICADO", "DAS do Simples Nacional (estimado)", das, eficaz.aliquota, entrada.receita_pa),),
        explicacoes=(
            ExplanationItem(
                "Limite de permanência",
                f"Receita acumulada no ano {entrada.receita_acumulada_ano} frente ao limite aplicável "
                f"{limite.limite_aplicavel} ({entrada.meses_atividade_no_ano} mês(es) de atividade no ano). "
                f"Sublimite ICMS/ISS: {limite.sublimite}. Situação: {limite.status.value}.",
                "TR-005",
            ),
            ExplanationItem(
                "Receita bruta de 12 meses",
                f"{nome_rbt}: {rbt.valor} ({entrada.meses_desde_abertura}º mês de atividade).",
                "TR-008",
            ),
            ExplanationItem(
                "Fator R",
                f"Fator R = {fator.fator} (folha {folha} / receita {receita_fr}, truncado em duas casas): "
                f"Anexo {fator.anexo.value}.",
                "TR-009",
            ),
            ExplanationItem(
                f"Faixa do Anexo {fator.anexo.value}",
                f"{faixa.numero}ª faixa: alíquota nominal {faixa.aliquota_nominal:%}, parcela a deduzir "
                f"{faixa.parcela_deduzir}.",
                "TR-006" if fator.anexo is AnexoSimples.III else "TR-007",
            ),
            ExplanationItem(
                "Alíquota efetiva e DAS",
                f"Alíquota efetiva {eficaz.aliquota} = ((RBT x alíquota nominal) - parcela a deduzir) / RBT; "
                f"DAS = receita do PA {entrada.receita_pa} x alíquota efetiva.",
                "TR-008",
            ),
        ),
        warnings=(
            "Ferramenta educacional: não substitui orientação contábil ou jurídica.",
            "Premissas do MVP: prestação de serviços no mercado interno, um estabelecimento, sem exportação, "
            "ST, monofásico, retenção de ISS, benefícios ou múltiplas segregações de receita.",
            "Cálculo completo suportado apenas com RBT12/RBT12p até o sublimite de ICMS/ISS.",
            "A folha do Fator R (FS12) é apurada pelo regime de caixa; RBT12 pelo de competência. "
            "Valor do DAS sem arredondamento (política em aberto).",
        ),
    )
