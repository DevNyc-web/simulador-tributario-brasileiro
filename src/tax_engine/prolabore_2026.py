"""TR-010: pró-labore do sócio único (INSS retido pela empresa + IRPF via TR-001).

Parâmetros em rules.json. A CPP patronal de 20% NÃO é somada: nos Anexos III/V
ela já está no DAS (LC 123/2006, art. 13, VI).
"""
from dataclasses import dataclass
from decimal import Decimal

from src.models.tax import ProLaboreInput
from src.tax_rules import get_rule, parse_decimal

from .pf_2026 import ANO, ZERO, calculate_irpf_mensal_2026


@dataclass(frozen=True)
class ProLaboreResult:
    bruto: Decimal
    base_inss: Decimal
    inss: Decimal
    irpf: Decimal
    liquido: Decimal  # bruto - inss - irpf
    warnings: tuple[str, ...] = ()


def calculate_prolabore_2026(entrada: ProLaboreInput) -> ProLaboreResult:
    if entrada.ano != ANO:
        raise ValueError(f"calculate_prolabore_2026 só suporta {ANO}.")
    p = get_rule(ANO, "TR-010").parametros
    aliquota = parse_decimal(p["aliquota_inss_segurado"])
    teto = parse_decimal(p["teto_previdenciario"])
    minimo = parse_decimal(p["salario_minimo"])
    bruto = entrada.valor

    if bruto == 0:
        return ProLaboreResult(ZERO, ZERO, ZERO, ZERO, ZERO, (
            "Pró-labore zero: o cenário representa ausência de remuneração de pró-labore no período; "
            "implicações societárias e previdenciárias fora do escopo não são inferidas.",
        ))

    base = min(bruto, teto)
    inss = base * aliquota  # retenção sobre a remuneração informada, limitada ao teto
    irpf = calculate_irpf_mensal_2026(bruto, inss).imposto_devido

    warnings = []
    if bruto < minimo:
        warnings.append(
            "Pró-labore abaixo do salário mínimo: o INSS foi calculado sobre o valor informado. Se a "
            "remuneração consolidada da competência ficar abaixo do mínimo, existem mecanismos de "
            "complementação, utilização ou agrupamento (EC 103/2019); nenhuma complementação é calculada."
        )
    if bruto > teto:
        warnings.append("Pró-labore acima do teto previdenciário: INSS limitado ao teto.")
    return ProLaboreResult(bruto, base, inss, irpf, bruto - inss - irpf, tuple(warnings))
