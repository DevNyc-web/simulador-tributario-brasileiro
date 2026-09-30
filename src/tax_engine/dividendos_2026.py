"""TR-011: distribuição de lucros (limite sem escrituração, IRRF do art. 6º-A, altas rendas).

Parâmetros em rules.json. Decimal exato; sem arredondamento. O simulador não calcula
lucro contábil e não modela a tributação do excedente ao limite sem escrituração.
"""
from dataclasses import dataclass
from decimal import Decimal

from src.models.tax import AnexoSimples, DividendosInput, ModoApuracaoLucro, SimulationStatus
from src.tax_rules import get_rule, parse_decimal

from .pf_2026 import ANO, ZERO


@dataclass(frozen=True)
class DividendosResult:
    status: SimulationStatus
    bruto: Decimal
    limite_isento_sem_escrituracao: Decimal | None = None
    irpj_no_das: Decimal | None = None
    irrf: Decimal | None = None
    liquido: Decimal | None = None
    warnings: tuple[str, ...] = ()


def calculate_irpj_no_das_2026(
    anexo: AnexoSimples, faixa: int, aliquota_efetiva: Decimal, receita_pa: Decimal
) -> Decimal:
    """IRPJ embutido no DAS: receita x alíquota efetiva x % de repartição do IRPJ da faixa
    (Anexos III/V, LC 123/2006). Anexo III, 5ª faixa com alíquota efetiva acima do limite do
    próprio Anexo: IRPJ = receita x (alíquota efetiva - teto do ISS) x percentual específico."""
    p = get_rule(ANO, "TR-011").parametros
    percentual = parse_decimal(p["reparticao_irpj"][anexo.value][faixa - 1])
    redist = p["redistribuicao_iss"].get(anexo.value)
    if (
        redist
        and faixa == int(redist["faixa"])
        and aliquota_efetiva > parse_decimal(redist["aliquota_efetiva_acima_de"])
    ):
        return receita_pa * (aliquota_efetiva - parse_decimal(redist["teto_iss"])) * parse_decimal(
            redist["percentual_irpj"]
        )
    return receita_pa * aliquota_efetiva * percentual


def calculate_irrf_dividendos_2026(total_mensal: Decimal) -> Decimal:
    """Art. 6º-A (Lei 9.250/1995): acima do limite mensal, alíquota sobre o TOTAL pago."""
    r = get_rule(ANO, "TR-011").parametros["irrf_dividendos"]
    if total_mensal > parse_decimal(r["limite_mensal_isencao"]):
        return total_mensal * parse_decimal(r["aliquota"])
    return ZERO


def calculate_dividendos_2026(
    entrada: DividendosInput, *, receita_pa: Decimal | None = None, irpj_no_das: Decimal | None = None
) -> DividendosResult:
    if entrada.ano != ANO:
        raise ValueError(f"calculate_dividendos_2026 só suporta {ANO}.")
    p = get_rule(ANO, "TR-011").parametros
    bruto = entrada.valor_distribuido
    warnings = [
        "Considera apenas lucros de resultados de 2026; lucros de 2025 ou anteriores (regra de transição) "
        "estão fora do MVP.",
        "O valor distribuído deve ser a soma de todos os pagamentos do mês da mesma PJ à mesma PF.",
        "Retenção de 10% aplicada também ao Simples Nacional, conforme a orientação da Receita Federal; "
        "existe liminar isolada em sentido contrário (MS 5002505-76.2026.4.03.6100), sem efeito geral.",
    ]

    limite = None
    if entrada.modo_apuracao is ModoApuracaoLucro.SEM_ESCRITURACAO:
        if receita_pa is None or irpj_no_das is None:
            raise ValueError("SEM_ESCRITURACAO exige receita_pa e irpj_no_das.")
        limite = max(receita_pa * parse_decimal(p["percentual_presuncao_servicos"]) - irpj_no_das, ZERO)
        if bruto > limite:
            return DividendosResult(
                SimulationStatus.NAO_SUPORTADO, bruto, limite, irpj_no_das, None, None,
                ("A distribuição informada excede o limite de isenção calculado para o cenário sem "
                 "escrituração contábil. A tributação do excedente não é modelada pelo MVP.",),
            )
        warnings.append(
            "Limite sem escrituração = percentual de presunção x receita do mês - IRPJ devido no DAS "
            "(LC 123/2006, art. 14, § 1º); é limite fiscal de isenção, não lucro contábil."
        )
    else:
        if bruto > entrada.lucro_contabil_disponivel:
            return DividendosResult(
                SimulationStatus.INCOMPATIVEL, bruto, None, irpj_no_das, None, None,
                ("A distribuição informada é maior que o lucro contábil disponível informado.",),
            )
        warnings.append(
            "O valor informado pressupõe escrituração contábil regular e lucro efetivamente demonstrado; "
            "o simulador não verifica balanço, balancete, escrituração nem disponibilidade societária."
        )

    renda = entrada.renda_anual_relevante_informada
    if renda is None:
        warnings.append(
            "A tributação mínima anual de altas rendas não foi avaliada, pois depende de informações "
            "anuais adicionais."
        )
    elif renda > parse_decimal(p["altas_rendas"]["limite_anual"]):
        warnings.append(
            "Este cenário pode estar sujeito à tributação mínima anual de altas rendas. O cálculo anual "
            "completo está fora do MVP."
        )

    irrf = calculate_irrf_dividendos_2026(bruto)
    return DividendosResult(SimulationStatus.OK, bruto, limite, irpj_no_das, irrf, bruto - irrf, tuple(warnings))
