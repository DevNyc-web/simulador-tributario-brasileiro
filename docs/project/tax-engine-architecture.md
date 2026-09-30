# Motor Tributário

> **Status posterior (MVP final):** este documento registra a arquitetura da **Fase 4A** (fundação do motor) e foi preservado como histórico. Nas fases seguintes, TR-001 a TR-011 foram implementadas e testadas (`pf_2026.py`, `mei_2026.py`, `simples_2026.py`, `prolabore_2026.py`, `dividendos_2026.py`, `comparator_2026.py`), o `calculator.py` passou a despachar os cenários `pf`, `mei`, `simples` e `comparar` para 2026, e o `rules.json` de 2026 contém TR-001 a TR-011 com status `TESTADA` (2027–2033 seguem com `regras: []`). Onde este texto diz "hoje", "nesta fase" ou "fase futura", leia-se o estado da Fase 4A. Visão final: [relatório acadêmico](../academic/relatorio-final.md), seção 14.

Documento técnico da infraestrutura do motor de cálculo. Não contém nenhuma
fórmula, alíquota, faixa ou limite fiscal — apenas a arquitetura que permitirá
implementar TR-001 a TR-011 (ver [tax-rule-catalog.md](../research/tax-rule-catalog.md))
em uma fase futura.

## Camadas

```
Interface (Flask, templates)
        ↓
Service (src/services/simulation_service.py)
        ↓
Tax Engine (src/tax_engine/calculator.py)
        ↓
Tax Rules (src/tax_rules/rule_loader.py)
        ↓
rules.json (data/tax_rules/<ano>/rules.json)
```

## Responsabilidades

- **Interface**: rotas Flask e templates. Só renderiza; nunca contém regra
  tributária, alíquota ou fórmula. As rotas atuais (`app.py`) apenas
  devolvem templates estáticos.
- **Service** (`src/services/simulation_service.py`): orquestra — recebe a
  entrada do usuário, chama o carregamento de regras por ano e o motor de
  cálculo, devolve o resultado. Não decide nenhuma regra fiscal.
- **Tax Engine** (`src/tax_engine/calculator.py`): núcleo de cálculo,
  independente de Flask — pode ser testado isoladamente. *(Estado na Fase 4A; hoje despacha os motores de 2026.)* Devolvia
  sempre um `SimulationResult` com status `PENDENTE`, pois nenhuma regra
  está validada para uso em cálculo real.
- **Tax Rules** (`src/tax_rules/`): carrega e valida a *forma* do arquivo de
  regras de um ano (`rule_loader.py`), converte valores decimais de forma
  explícita (`decimal_utils.py`) e define os erros próprios do domínio
  (`exceptions.py`). Nunca executa cálculo.
- **rules.json**: dado puro, um arquivo por ano, sem nenhuma lógica.

## Modelos (`src/models/tax.py`)

Dataclasses imutáveis (`@dataclass(frozen=True)`), sem Pydantic e sem
dependências novas:

- `TaxRuleMetadata` — metadados de uma regra (TR-XXX): id, nome, ano,
  status, vigência, fontes. Não carrega os parâmetros fiscais em si.
- `SimulationInput` — entrada genérica de uma simulação (ano, tipo de
  simulação). Campos específicos de cada cenário (PF, MEI, Simples, PJ)
  serão adicionados quando as regras correspondentes forem implementadas.
- `TaxItem` — um tributo/contribuição individual dentro de um resultado.
- `ExplanationItem` — texto explicativo, opcionalmente ligado a uma regra
  (`rule_id`).
- `SimulationResult` — resultado de uma simulação: status, ano, tipo,
  total de tributos, líquido estimado, itens, explicações, avisos.

Dois enums fecham o conjunto de valores possíveis, para impedir strings
livres:

- `SimulationStatus`: `OK`, `PENDENTE`, `NAO_SUPORTADO`, `INCOMPATIVEL`.
- `RuleStatus`: `PENDENTE`, `PESQUISADA`, `VALIDADA`, `IMPLEMENTADA`,
  `TESTADA` — com duas propriedades distintas (ver "Segurança normativa"
  abaixo): `esta_validada_normativamente` (verdadeira a partir de
  `VALIDADA`) e `pode_produzir_resultado_fiscal` (verdadeira só a partir de
  `IMPLEMENTADA`). **`VALIDADA` sozinha não autoriza cálculo** — significa
  apenas que a regra foi confirmada contra fonte oficial, não que exista
  código pronto para calculá-la.

## Política Decimal

- Todo valor monetário ou alíquota fiscal usa `decimal.Decimal`, nunca
  `float` — `float` introduz erro de arredondamento binário inaceitável em
  cálculo tributário.
- No JSON (`rules.json`), todo número decimal fiscal é representado como
  **string** (`"1621.00"`, `"0.1100"`), nunca como número JSON literal
  (`1621.00`, `0.11`) — um número JSON é sempre desserializado como `float`
  pelo `json` da biblioteca padrão, o que reintroduziria o problema acima.
- A conversão de string para `Decimal` é sempre explícita e estrita, através
  de `parse_decimal(value, *, allow_none=False)`
  (`src/tax_rules/decimal_utils.py`):
  - `parse_decimal("10.00")` → `Decimal("10.00")`.
  - `parse_decimal(10)`, `parse_decimal(10.0)`, `parse_decimal(True)`,
    `parse_decimal([])`, `parse_decimal({})` → todos levantam
    `InvalidDecimalValueError` (apenas `str` é aceita).
  - `parse_decimal("")`, `parse_decimal("abc")`, `parse_decimal("1,50")`
    (vírgula não é separador decimal aceito) → `InvalidDecimalValueError`.
  - `parse_decimal("NaN")`, `parse_decimal("Infinity")`,
    `parse_decimal("-Infinity")` → `InvalidDecimalValueError` (valores não
    finitos nunca são um decimal fiscal válido, mesmo sendo aceitos pelo
    `Decimal()` da biblioteca padrão).
  - `parse_decimal(None)` → **levanta `InvalidDecimalValueError` por
    padrão**. Só devolve `None` quando o chamador pedir explicitamente com
    `parse_decimal(None, allow_none=True)` — nunca implicitamente.
- Não existe conversão implícita de string arbitrária para `Decimal` em
  nenhum ponto do carregamento de regras.

## Política None vs. zero

Um valor fiscal **pendente** (ainda não calculável, porque a regra não está
validada, ou porque o dado de entrada não foi informado) é sempre `None`.

Zero é um valor real e nunca deve ser usado como placeholder para "não
sei"/"ainda não calculado". Todos os modelos (`TaxItem.valor`,
`SimulationResult.total_tributos`, `SimulationResult.liquido_estimado`
etc.) aceitam `Decimal | None` exatamente por esse motivo.

## Ciclo da regra

```
PENDENTE → PESQUISADA → VALIDADA → IMPLEMENTADA → TESTADA
```

Ver definição de cada estágio e o estado atual de TR-001 a TR-011 em
[tax-rule-catalog.md](../research/tax-rule-catalog.md) e
[tax-rule-matrix.md](../research/tax-rule-matrix.md).

## Segurança normativa

`VALIDADA` significa apenas que a regra foi **confirmada jurídica/
normativamente contra fonte oficial** (ver
[tax-rule-catalog.md](../research/tax-rule-catalog.md)) — isso **não**
significa que exista código capaz de calculá-la. Por isso o modelo separa
duas perguntas diferentes:

- `RuleStatus.esta_validada_normativamente` → `True` a partir de
  `VALIDADA` (isto é, `VALIDADA`, `IMPLEMENTADA` ou `TESTADA`).
- `RuleStatus.pode_produzir_resultado_fiscal` → `True` **somente** a partir
  de `IMPLEMENTADA` (isto é, `IMPLEMENTADA` ou `TESTADA`). Uma regra
  apenas `VALIDADA` **não** autoriza a produção de um resultado fiscal —
  falta o código que a implementa.

| Status | `esta_validada_normativamente` | `pode_produzir_resultado_fiscal` |
|---|---|---|
| PENDENTE | False | False |
| PESQUISADA | False | False |
| VALIDADA | True | False |
| IMPLEMENTADA | True | True |
| TESTADA | True | True |

Nesta fase (Fase 4A), essa verificação ainda não é exercida por nenhuma
regra real — nenhum `rules.json` contém regras (`"regras": []` em todos os
anos), e nenhum dispatcher fiscal foi implementado. O `tax_engine.calculate`
reflete essa ausência devolvendo sempre
`SimulationResult(status=SimulationStatus.PENDENTE, ...)` com
`total_tributos=None` e `liquido_estimado=None`. Quando regras reais forem
adicionadas, o motor deverá consultar `pode_produzir_resultado_fiscal` (não
apenas `esta_validada_normativamente`) antes de calcular qualquer valor —
isso ainda não está implementado nesta fase.

## Estrutura de rules.json

Formato do arquivo (schema versão 1):

```json
{
  "schema_version": 1,
  "ano": 2026,
  "regras": []
}
```

`schema_version` e `ano` são validados por `rule_loader.load_year_rules`
antes de qualquer uso: `schema_version` deve ser exatamente o valor
suportado (`SCHEMA_VERSION = 1`); `ano` deve ser idêntico ao número do
diretório; `regras` deve ser uma lista (vazia, nesta fase, para todos os
anos).

O arquivo tinha, em uma versão anterior desta fase, um campo top-level
`"status"` (`"[REGRA PENDENTE DE VALIDAÇÃO]"`). Esse campo foi retirado por
ser legado e redundante com o status por regra (`RuleStatus`, dentro de
cada item de `"regras"`) — não havia nenhum consumidor de produção lendo
esse campo (só um teste, já ajustado). O estado "pendente" do arquivo é
simplesmente `"regras": []`.

### Representação futura de uma regra dentro de `"regras"`

Contrato estrutural apenas — nenhuma regra real foi inserida ainda:

```json
{
  "id": "TR-XXX",
  "nome": "...",
  "ano": 2026,
  "status": "VALIDADA",
  "vigencia_inicio": "2026-01-01",
  "vigencia_fim": null,
  "fontes": ["F-XX"],
  "parametros": {}
}
```

O conteúdo de `"parametros"` varia por regra (percentuais, faixas, limites
etc.) e será definido quando cada TR for de fato implementada. Todo valor
decimal dentro de `"parametros"` segue a política Decimal acima (string no
JSON, convertida com `parse_decimal`).

## Escopo temporal

- **Motor real inicial**: ano-calendário **2026** — é o único ano cujas
  regras (TR-001 a TR-011) já estão `VALIDADA` (ver
  [tax-rule-matrix.md](../research/tax-rule-matrix.md)).
- **2027–2033**: estrutura de arquivo preparada (mesmo schema, `"regras":
  []`), mas nenhum cálculo será implementado para esses anos nesta fase —
  eles permanecem parte da timeline educacional da transição da Reforma
  Tributária (ver premissa 9 em
  [calculation-assumptions.md](../research/calculation-assumptions.md)).

## SUPPORTED_YEARS — fonte única

`SUPPORTED_YEARS = range(2026, 2034)` é definido **uma única vez**, em
`src/tax_rules/rule_loader.py`, e reexportado por `src/tax_rules/__init__.py`.
Todo consumidor (Flask/contexto compartilhado em `app.py`, o loader, os
testes) importa esse mesmo objeto — não há lista de anos duplicada em
nenhum outro módulo.

## Resolução de caminho do loader

`DATA_DIR` é resolvido a partir de `Path(__file__).resolve().parents[2] /
"data" / "tax_rules"` — ou seja, a partir da localização do próprio
`rule_loader.py` dentro do repositório, nunca do diretório de trabalho
atual (`os.getcwd()`). Isso garante que `load_year_rules` funcione
independentemente de onde o processo Python foi iniciado (ver
`tests/test_rule_loader.py::test_loader_is_independent_of_cwd`, que muda o
cwd para um diretório temporário e confirma que o carregamento continua
funcionando).

## Erros do domínio (`src/tax_rules/exceptions.py`)

- `TaxRuleError` — classe-base.
- `UnsupportedTaxYearError` — ano fora de 2026–2033.
- `InvalidRuleFileError` — arquivo ausente, JSON malformado, ou fora do
  schema esperado (`schema_version`, `ano` ou `regras` inválidos).
- `InvalidDecimalValueError` — valor passado a `parse_decimal` que não é
  `None` nem uma string decimal válida (inclui `float`, propositalmente
  rejeitado).

## Testes

- `tests/test_rule_loader.py` — contrato do loader (todos os anos
  suportados carregam sem o campo `"status"` legado; ano não suportado,
  arquivo ausente, JSON inválido, `schema_version` e `ano` divergentes
  levantam erro explícito; independência do diretório de trabalho) e do
  `parse_decimal` estrito (rejeita tipos não-`str`, strings malformadas,
  valores não finitos, e `None` sem `allow_none=True`).
- `tests/test_tax_models.py` — imutabilidade real dos modelos (inclusive
  tentativa de mutar as coleções internas, que são sempre `tuple`, nunca
  `list`), a semântica correta de `RuleStatus` para os cinco estados
  (`esta_validada_normativamente` × `pode_produzir_resultado_fiscal`),
  política None-vs-zero, e o contrato futuro de regra aplicado a um
  fixture fictício (`tests/fixtures/fictitious_rule_example.json`, nunca
  usado em produção).
