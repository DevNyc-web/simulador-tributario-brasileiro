"""Motor Pessoa Física 2026: TR-001 (IRPF mensal) e TR-002 (INSS autônomo).

O código contém só fórmula; todo parâmetro fiscal vem de rules.json (get_rule).
Aritmética em Decimal exato — sem float e sem arredondamento (Q-02 em aberto);
a formatação em centavos é da camada de apresentação.
"""
from dataclasses import dataclass
from decimal import Decimal

from src.models.tax import (
    ExplanationItem,
    PFSimulationInput,
    PlanoINSS,
    SimulationResult,
    SimulationStatus,
    TaxItem,
)
from src.tax_rules import get_rule, parse_decimal

ANO = 2026
ZERO = Decimal(0)


@dataclass(frozen=True)
class INSSResult:
    plano: PlanoINSS
    base_calculo: Decimal
    aliquota: Decimal
    contribuicao: Decimal
    abaixo_do_minimo: bool
    limitado_ao_teto: bool
    sem_remuneracao: bool = False


@dataclass(frozen=True)
class IRPFResult:
    rendimento: Decimal
    deducao_legal: Decimal
    desconto_simplificado: Decimal
    usou_simplificado: bool
    deducao_utilizada: Decimal
    base_calculo: Decimal
    aliquota: Decimal
    parcela_deduzir: Decimal
    imposto_antes_reducao: Decimal
    reducao: Decimal
    imposto_devido: Decimal


def calculate_inss_autonomo_2026(renda_mensal: Decimal, plano: PlanoINSS) -> INSSResult:
    p = get_rule(ANO, "TR-002").parametros
    minimo = parse_decimal(p["salario_minimo"])
    teto = parse_decimal(p["teto_previdenciario"])

    aliquota = parse_decimal(p["aliquota_simplificado" if plano is PlanoINSS.SIMPLIFICADO else "aliquota_normal"])
    if renda_mensal == 0:
        # Sem remuneração no mês não há contribuição calculada (a facultativa
        # é volitiva e está fora do MVP; IN RFB 2.110/2022).
        return INSSResult(plano, ZERO, aliquota, ZERO, False, False, True)

    if plano is PlanoINSS.SIMPLIFICADO:
        return INSSResult(plano, minimo, aliquota, minimo * aliquota, False, False)

    abaixo = renda_mensal < minimo
    acima = renda_mensal > teto
    # Abaixo do mínimo: o valor econômico para alcançar o mínimo equivale à
    # contribuição sobre o mínimo (complementação = (SM - RC) x 20%; Q-P6).
    base = minimo if abaixo else teto if acima else renda_mensal
    return INSSResult(plano, base, aliquota, base * aliquota, abaixo, acima)


def calculate_irpf_mensal_2026(rendimento: Decimal, contribuicao_previdenciaria: Decimal) -> IRPFResult:
    p = get_rule(ANO, "TR-001").parametros
    simplificado = parse_decimal(p["desconto_simplificado_mensal"])

    # Alternativas (não somam): usa-se a mais benéfica.
    usou_simplificado = simplificado >= contribuicao_previdenciaria
    deducao = simplificado if usou_simplificado else contribuicao_previdenciaria
    base = max(rendimento - deducao, ZERO)

    for faixa in p["faixas"]:
        limite = parse_decimal(faixa["limite_superior"], allow_none=True)
        if limite is None or base <= limite:
            aliquota = parse_decimal(faixa["aliquota"])
            parcela = parse_decimal(faixa["parcela_deduzir"])
            break
    antes = max(base * aliquota - parcela, ZERO)

    # A redução enquadra-se pelo RENDIMENTO tributável, não pela base.
    r = p["reducao"]
    if rendimento <= parse_decimal(r["rendimento_limite_reducao_maxima"]):
        reducao = parse_decimal(r["reducao_maxima"])
    elif rendimento <= parse_decimal(r["rendimento_limite_reducao"]):
        reducao = parse_decimal(r["formula_constante"]) - parse_decimal(r["formula_coeficiente"]) * rendimento
    else:
        reducao = ZERO
    reducao = min(max(reducao, ZERO), antes)

    return IRPFResult(
        rendimento, contribuicao_previdenciaria, simplificado, usou_simplificado, deducao,
        base, aliquota, parcela, antes, reducao, antes - reducao,
    )


def calculate_pf_2026(entrada: PFSimulationInput) -> SimulationResult:
    if entrada.ano != ANO:
        raise ValueError(f"calculate_pf_2026 só suporta {ANO}.")
    renda = entrada.renda_mensal
    inss = calculate_inss_autonomo_2026(renda, entrada.plano_inss)
    irpf = calculate_irpf_mensal_2026(renda, inss.contribuicao)
    total = inss.contribuicao + irpf.imposto_devido

    warnings = ["Ferramenta educacional: não substitui orientação contábil ou jurídica."]
    if inss.sem_remuneracao:
        warnings.append(
            "Não houve remuneração no mês. Eventual contribuição facultativa à Previdência "
            "não é calculada neste cenário do MVP."
        )
    if inss.abaixo_do_minimo:
        warnings.append(
            "A remuneração consolidada ficou abaixo do salário mínimo. Existem mecanismos de "
            "complementação, utilização ou agrupamento de contribuições (EC 103/2019). Na "
            "simplificação adotada pelo MVP, o INSS exibido é o valor considerado para que a "
            "competência alcance o mínimo (contribuição correspondente ao salário mínimo); "
            "não é uma contribuição obrigatória adicional."
        )
    if inss.plano is PlanoINSS.SIMPLIFICADO:
        warnings.append(
            "Plano simplificado: não contempla aposentadoria por tempo de contribuição, salvo "
            "complementação; vale apenas para quem trabalha por conta própria sem prestar "
            "serviços a empresas."
        )
    warnings.append("Não consideradas deduções como dependentes, pensão alimentícia e Livro Caixa.")

    qual = "Desconto simplificado" if irpf.usou_simplificado else "Contribuição previdenciária oficial"
    explicacoes = [
        ExplanationItem(
            "Plano previdenciário",
            f"Plano {inss.plano.value}: alíquota {inss.aliquota:%} sobre base de {inss.base_calculo}."
            + (" Base limitada ao teto." if inss.limitado_ao_teto else ""),
            "TR-002",
        ),
        ExplanationItem(
            "Dedução do IRPF",
            f"{qual} (mais benéfica): {irpf.deducao_utilizada}. Base de cálculo: {irpf.base_calculo}.",
            "TR-001",
        ),
        ExplanationItem(
            "Faixa do IRPF",
            f"Alíquota {irpf.aliquota:%} com parcela a deduzir {irpf.parcela_deduzir}; "
            f"imposto antes da redução: {irpf.imposto_antes_reducao}.",
            "TR-001",
        ),
    ]
    if irpf.reducao > 0:
        explicacoes.append(ExplanationItem(
            "Redução 2026 (Lei 15.270/2025)",
            f"Redução de {irpf.reducao}, calculada sobre o rendimento tributável e limitada ao imposto.",
            "TR-001",
        ))

    return SimulationResult(
        status=SimulationStatus.OK,
        ano=ANO,
        tipo_simulacao="pf",
        total_tributos=total,
        liquido_estimado=renda - total,
        itens=(
            TaxItem("INSS", "Contribuição previdenciária do contribuinte individual",
                    inss.contribuicao, inss.aliquota, inss.base_calculo),
            TaxItem("IRPF", "Imposto de renda mensal (Carnê-Leão)",
                    irpf.imposto_devido, irpf.aliquota, irpf.base_calculo),
        ),
        explicacoes=tuple(explicacoes),
        warnings=tuple(warnings),
    )
