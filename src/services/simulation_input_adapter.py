"""Adaptação dos dados HTTP (strings de formulário) para os modelos de entrada dos motores.

Só converte e valida formato; NÃO contém fórmula, alíquota ou limite fiscal. Toda regra
tributária continua em src/tax_engine + rules.json. Valores monetários viram Decimal
(nunca float). parse_brl_input é entrada de apresentação e NÃO substitui o parse_decimal
estrito de src/tax_rules (que continua restrito às strings do rules.json).
"""
import re
from decimal import Decimal
from enum import Enum
from typing import Mapping

from src.models.tax import (
    AtividadeSimples,
    CategoriaMEI,
    ComparatorSimulationInput,
    DividendosInput,
    MEISimulationInput,
    ModoApuracaoLucro,
    PFSimulationInput,
    PlanoINSS,
    SimplesSimulationInput,
)
from src.tax_engine.pf_2026 import ANO

TIPOS = ("pf", "mei", "simples", "comparar")
MAX_HISTORICO = 12  # linhas de histórico no formulário (estrutura da tela; a regra é validada nos modelos)
MESES_MATURIDADE = 13  # 13+ meses de atividade: usa os 12 meses anteriores

_COMMA = re.compile(r"^(\d{1,3}(\.\d{3})*|\d+),\d{1,2}$")  # 8.000,50 | 8000,50
_DOT_DECIMAL = re.compile(r"^\d+\.\d{1,2}$")  # 8000.50
_THOUSANDS = re.compile(r"^\d{1,3}(\.\d{3})+$")  # 8.000 (milhar, padrão brasileiro)
_INTEGER = re.compile(r"^\d+$")
_MAX_DIGITS = 15


class SimulationInputError(ValueError):
    """Entrada de formulário inválida: erros por campo e/ou mensagens gerais."""

    def __init__(self, errors: dict[str, str] | None = None, general: list[str] | None = None, tipo: str | None = None):
        self.errors = errors or {}
        self.general = general or []
        self.tipo = tipo
        super().__init__("; ".join([*self.general, *self.errors.values()]) or "Entrada inválida.")


def parse_brl_input(text: str, *, allow_negative: bool = False) -> Decimal:
    """Converte "8000", "8000.50", "8000,50", "8.000,50", "R$ 8.000,50" em Decimal.

    "8.000" é lido como oito mil (milhar brasileiro). Rejeita texto arbitrário, NaN,
    Infinity, notação científica e (por padrão) valores negativos.
    """
    if not isinstance(text, str):
        raise ValueError("Informe um valor válido.")
    s = text.replace("R$", "").replace(" ", "").replace(" ", "")
    negative = s.startswith("-")
    if negative:
        if not allow_negative:
            raise ValueError("O valor não pode ser negativo.")
        s = s[1:]
    if _COMMA.match(s):
        normalized = s.replace(".", "").replace(",", ".")
    elif _DOT_DECIMAL.match(s):
        normalized = s
    elif _THOUSANDS.match(s):
        normalized = s.replace(".", "")
    elif _INTEGER.match(s):
        normalized = s
    else:
        raise ValueError("Informe um valor válido (ex.: 8.000,50).")
    if len(normalized.split(".")[0]) > _MAX_DIGITS:
        raise ValueError("Valor muito grande.")
    value = Decimal(normalized)
    return -value if negative else value


class _Reader:
    """Lê campos do formulário acumulando erros por campo."""

    def __init__(self, form: Mapping[str, str]):
        self.form = form
        self.errors: dict[str, str] = {}

    def _raw(self, name: str) -> str:
        return (self.form.get(name) or "").strip()

    def money(self, name: str, *, required: bool = True) -> Decimal | None:
        raw = self._raw(name)
        if not raw:
            if required:
                self.errors[name] = "Campo obrigatório."
            return None
        try:
            return parse_brl_input(raw)
        except ValueError as exc:
            self.errors[name] = str(exc)
            return None

    def integer(self, name: str, *, minimo: int, maximo: int | None = None) -> int | None:
        raw = self._raw(name)
        if not raw:
            self.errors[name] = "Campo obrigatório."
            return None
        if not _INTEGER.match(raw):
            self.errors[name] = "Informe um número inteiro."
            return None
        n = int(raw)
        if n < minimo or (maximo is not None and n > maximo):
            limite = f"entre {minimo} e {maximo}" if maximo is not None else f"maior ou igual a {minimo}"
            self.errors[name] = f"Informe um valor {limite}."
            return None
        return n

    def choice(self, name: str, enum: type[Enum]) -> Enum | None:
        raw = self._raw(name)
        if not raw:
            self.errors[name] = "Selecione uma opção."
            return None
        try:
            return enum(raw)
        except ValueError:
            self.errors[name] = "Selecione uma opção válida."
            return None

    def yes_no(self, name: str, default: bool = True) -> bool:
        raw = self._raw(name)
        if not raw:
            return default
        if raw in ("sim", "nao"):
            return raw == "sim"
        self.errors[name] = "Selecione Sim ou Não."
        return default

    def historico(self, meses_desde_abertura: int | None) -> tuple[tuple[Decimal, ...], tuple[Decimal, ...]]:
        """Histórico anterior ao mês atual. Linha N = N meses antes do atual (1 = mais recente);
        devolve em ordem cronológica. A quantidade exigida é validada aqui no servidor."""
        if meses_desde_abertura is None:
            return (), ()
        necessarias = min(meses_desde_abertura - 1, MAX_HISTORICO) if meses_desde_abertura < MESES_MATURIDADE else MAX_HISTORICO
        receitas, folhas = [], []
        for n in range(necessarias, 0, -1):  # mais antigo primeiro
            r = self.money(f"hist_receita_{n}")
            f = self.money(f"hist_folha_{n}")
            receitas.append(r)
            folhas.append(f)
        if None in receitas or None in folhas:
            return (), ()
        return tuple(receitas), tuple(folhas)


def _finish(reader: _Reader, tipo: str, build):
    if reader.errors:
        raise SimulationInputError(reader.errors, tipo=tipo)
    try:
        return build()
    except (ValueError, TypeError) as exc:
        raise SimulationInputError(general=[str(exc)], tipo=tipo) from exc


def _pf(form) -> dict:
    r = _Reader(form)
    renda = r.money("renda_mensal")
    plano = r.choice("plano_inss", PlanoINSS)
    entrada = _finish(r, "pf", lambda: PFSimulationInput(ANO, renda, plano))
    return {"tipo_simulacao": "pf", "entrada": entrada}


def _mei(form) -> dict:
    r = _Reader(form)
    receita = r.money("receita_acumulada")
    categoria = r.choice("categoria", CategoriaMEI)
    meses = r.integer("meses_atividade_no_ano", minimo=1, maximo=12)
    optante = r.yes_no("optante_simei")
    entrada = _finish(r, "mei", lambda: MEISimulationInput(ANO, receita, categoria, meses, optante))
    return {"tipo_simulacao": "mei", "entrada": entrada}


def _simples(form) -> dict:
    r = _Reader(form)
    receita_pa = r.money("receita_pa")
    folha_pa = r.money("folha_pa")
    acumulada = r.money("receita_acumulada_ano")
    meses_abertura = r.integer("meses_desde_abertura", minimo=1)
    meses_ano = r.integer("meses_atividade_no_ano", minimo=1, maximo=12)
    atividade = r.choice("atividade", AtividadeSimples)
    optante = r.yes_no("optante_simples")
    receitas, folhas = r.historico(meses_abertura)
    entrada = _finish(r, "simples", lambda: SimplesSimulationInput(
        ano=ANO, receita_pa=receita_pa, receitas_anteriores=receitas, folha_pa=folha_pa,
        folhas_anteriores=folhas, receita_acumulada_ano=acumulada, meses_desde_abertura=meses_abertura,
        meses_atividade_no_ano=meses_ano, atividade=atividade, optante_simples=optante,
    ))
    return {"tipo_simulacao": "simples", "entrada": entrada}


def _comparar(form) -> dict:
    r = _Reader(form)
    receita = r.money("receita_mensal")  # mesma receita para PF e PJ
    plano = r.choice("plano_inss", PlanoINSS)
    prolabore = r.money("prolabore")
    acumulada = r.money("receita_acumulada_ano")
    meses_abertura = r.integer("meses_desde_abertura", minimo=1)
    meses_ano = r.integer("meses_atividade_no_ano", minimo=1, maximo=12)
    atividade = r.choice("atividade", AtividadeSimples)
    optante = r.yes_no("optante_simples")
    receitas, folhas = r.historico(meses_abertura)
    distribuido = r.money("dividendos")
    modo = r.choice("modo_apuracao", ModoApuracaoLucro)
    lucro = r.money("lucro_contabil_disponivel") if modo is ModoApuracaoLucro.COM_ESCRITURACAO else None
    renda_anual = r.money("renda_anual_relevante", required=False)

    def build():
        pf = PFSimulationInput(ANO, receita, plano)
        simples = SimplesSimulationInput(  # sem empregados: folha do mês = pró-labore
            ano=ANO, receita_pa=receita, receitas_anteriores=receitas, folha_pa=prolabore,
            folhas_anteriores=folhas, receita_acumulada_ano=acumulada, meses_desde_abertura=meses_abertura,
            meses_atividade_no_ano=meses_ano, atividade=atividade, optante_simples=optante,
        )
        div = DividendosInput(ANO, distribuido, modo, lucro, renda_anual)
        return ComparatorSimulationInput(pf, simples, prolabore, div)

    entrada = _finish(r, "comparar", build)
    return {"tipo_simulacao": "comparar", "entrada": entrada}


_BUILDERS = {"pf": _pf, "mei": _mei, "simples": _simples, "comparar": _comparar}


def build_scenario(form: Mapping[str, str]) -> dict:
    """Constrói o cenário {"tipo_simulacao", "entrada"} aceito por src.tax_engine.calculate."""
    tipo = (form.get("tipo_simulacao") or "").strip()
    if tipo not in _BUILDERS:
        raise SimulationInputError(general=["Tipo de simulação inválido."], tipo=None)
    return _BUILDERS[tipo](form)
