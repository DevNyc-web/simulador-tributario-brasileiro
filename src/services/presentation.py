"""Formatação e rótulos de APRESENTAÇÃO. Nenhuma regra fiscal aqui.

Os arredondamentos deste módulo são apenas visuais (duas casas na tela): o Decimal
guardado nos resultados não é alterado e isto NÃO é política fiscal de arredondamento
(a política continua em aberto: Q-02 / Q-SN-04).
"""
import re
from decimal import ROUND_HALF_UP, Decimal

from src.models.tax import (
    AnexoSimples,
    AtividadeSimples,
    CategoriaMEI,
    ModoApuracaoLucro,
    PlanoINSS,
    SimulationStatus,
    StatusLimiteMEI,
)

PLANO_LABELS = {PlanoINSS.NORMAL: "Plano normal", PlanoINSS.SIMPLIFICADO: "Plano simplificado"}
CATEGORIA_LABELS = {
    CategoriaMEI.COMERCIO_INDUSTRIA: "Comércio / Indústria",
    CategoriaMEI.SERVICOS: "Serviços",
    CategoriaMEI.COMERCIO_E_SERVICOS: "Comércio e Serviços",
}
ATIVIDADE_LABELS = {
    AtividadeSimples.DESENVOLVIMENTO_SOFTWARE: "Desenvolvimento de software",
    AtividadeSimples.CONSULTORIA: "Consultoria",
    AtividadeSimples.ENGENHARIA: "Engenharia",
    AtividadeSimples.ARQUITETURA: "Arquitetura",
    AtividadeSimples.MEDICINA: "Medicina",
    AtividadeSimples.ODONTOLOGIA: "Odontologia",
    AtividadeSimples.PSICOLOGIA: "Psicologia",
    AtividadeSimples.FISIOTERAPIA: "Fisioterapia",
    AtividadeSimples.ACADEMIAS: "Academias",
}
MODO_LABELS = {
    ModoApuracaoLucro.SEM_ESCRITURACAO: "Sem escrituração contábil",
    ModoApuracaoLucro.COM_ESCRITURACAO: "Com escrituração contábil",
}
LIMITE_LABELS = {
    StatusLimiteMEI.COMPATIVEL: "Dentro do limite",
    StatusLimiteMEI.EXCESSO_ATE_20: "Acima do limite, sem superar 20% dele",
    StatusLimiteMEI.EXCESSO_MAIS_20: "Acima do limite em mais de 20%",
}
ANEXO_LABELS = {AnexoSimples.III: "Anexo III", AnexoSimples.V: "Anexo V"}
STATUS_LABELS = {
    SimulationStatus.OK: "Cálculo realizado",
    SimulationStatus.NAO_SUPORTADO: "Cenário não suportado pelo MVP",
    SimulationStatus.INCOMPATIVEL: "Cenário incompatível com o regime",
    SimulationStatus.PENDENTE: "Cálculo pendente",
}

# Tokens de enum que podem aparecer nos textos explicativos dos motores -> texto humano.
_TOKEN_LABELS = {
    "NORMAL": "normal", "SIMPLIFICADO": "simplificado",
    **{m.value: CATEGORIA_LABELS[m] for m in CategoriaMEI},
    **{m.value: LIMITE_LABELS[m] for m in StatusLimiteMEI},
    "COMPATIVEL": "Dentro do limite", "ACIMA_SUBLIMITE_MVP": "Acima do sublimite suportado pelo MVP",
    "FORA_LIMITE_SIMPLES": "Fora do limite do Simples Nacional",
}
_TOKEN_RE = re.compile(r"\b(" + "|".join(sorted(_TOKEN_LABELS, key=len, reverse=True)) + r")\b")
# decimal "1234.50" -> "1.234,50"; ignora referências legais ("15.270/2025", "2026.4.03")
_NUMBER_RE = re.compile(r"(?<![\d./-])(\d+)\.(\d+)(?!\d|/|\.\d)")

def _group(integer: str) -> str:
    return f"{int(integer):,}".replace(",", ".")


def brl(value: Decimal | None) -> str:
    """Decimal -> "R$ 1.234,50" (duas casas, apenas visual)."""
    if value is None:
        return "—"
    q = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    sign = "-" if q < 0 else ""
    integer, frac = f"{abs(q):.2f}".split(".")
    return f"{sign}R$ {_group(integer)},{frac}"


def pct(value: Decimal | None, places: int = 2) -> str:
    """Decimal("0.5") -> "50,00%" (apenas visual)."""
    if value is None:
        return "—"
    q = (Decimal(value) * 100).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    integer, _, frac = f"{q:.{places}f}".partition(".")
    return f"{_group(integer)},{frac}%" if places else f"{_group(integer)}%"


def decimal_br(value: Decimal | None, places: int = 2) -> str:
    """Decimal -> "0,30" (apenas visual)."""
    if value is None:
        return "—"
    q = Decimal(value).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    integer, _, frac = f"{q:.{places}f}".partition(".")
    return f"{_group(integer)},{frac}"


def humanize(text: str) -> str:
    """Texto dos motores -> texto para o usuário: enums viram rótulos e decimais usam vírgula."""
    text = _TOKEN_RE.sub(lambda m: _TOKEN_LABELS[m.group(1)], text)
    # zeros finais de precisão interna são omitidos (mantém ao menos duas casas); valor inalterado
    return _NUMBER_RE.sub(lambda m: f"{_group(m.group(1))},{m.group(2).rstrip('0').ljust(2, '0')}", text)


def choices() -> dict:
    """Opções dos formulários (valor do enum, rótulo amigável)."""
    return {
        "planos": [(m.value, PLANO_LABELS[m]) for m in PlanoINSS],
        "categorias": [(m.value, CATEGORIA_LABELS[m]) for m in CategoriaMEI],
        "atividades": [(m.value, ATIVIDADE_LABELS[m]) for m in AtividadeSimples],
        "modos": [(m.value, MODO_LABELS[m]) for m in ModoApuracaoLucro],
        "meses_historico": list(range(1, 13)),
    }
