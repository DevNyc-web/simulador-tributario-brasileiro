"""Conversão explícita e estrita de valores decimais fiscais.

Nenhum valor numérico fiscal deve ser lido de JSON como float. Todo decimal
fiscal é representado como string no JSON (ex.: "1621.00", "0.1100") e só
deve virar Decimal através de parse_decimal — nunca por conversão implícita,
por presumir que qualquer string arbitrária é segura de converter, ou por
aceitar None silenciosamente.
"""
from decimal import Decimal, InvalidOperation

from .exceptions import InvalidDecimalValueError


def parse_decimal(value, *, allow_none: bool = False) -> Decimal | None:
    """Converte uma string decimal fiscal em Decimal.

    - Aceita somente `str`. Qualquer outro tipo (int, float, bool, list,
      dict etc.) é rejeitado, mesmo quando pareceria um número válido —
      isso impede que erro de representação binária (float) ou um tipo
      inesperado entre silenciosamente em cálculo fiscal.
    - A string deve ser um decimal finito válido. Strings vazias,
      malformadas (`"abc"`, `"1,50"`) ou que representem valores não
      finitos (`"NaN"`, `"Infinity"`, `"-Infinity"`) são rejeitadas.
    - `None` só é aceito quando o chamador passar `allow_none=True`
      explicitamente — nunca por padrão. Isso cumpre a política do projeto
      de que ausência de valor (`None`) só é permitida onde o chamador
      pediu explicitamente por ela.
    """
    if value is None:
        if allow_none:
            return None
        raise InvalidDecimalValueError(
            "None não é aceito implicitamente por parse_decimal; "
            "passe allow_none=True se a ausência de valor for válida neste contexto."
        )
    if not isinstance(value, str):
        raise InvalidDecimalValueError(
            "Valores decimais fiscais devem ser strings no JSON; "
            f"recebido {type(value).__name__}: {value!r}"
        )
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise InvalidDecimalValueError(f"String decimal inválida: {value!r}") from exc
    if not result.is_finite():
        raise InvalidDecimalValueError(
            f"Valor decimal não finito não é aceito em contexto fiscal: {value!r}"
        )
    return result
