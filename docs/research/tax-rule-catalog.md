# Catálogo de Regras Tributárias do MVP

> Nenhum valor, fórmula ou base legal foi preenchido. Todo campo fiscal é `PENDENTE` até pesquisa em fonte oficial primária.
> Nenhuma regra é implementada em `tax_engine` ou `data/tax_rules/` sem status `VALIDADA` e linha correspondente em [fontes-tributarias.md](fontes-tributarias.md).

## Estados

`PENDENTE` → `PESQUISADA` → `VALIDADA` → `IMPLEMENTADA` → `TESTADA`

- **Pesquisa:** fonte oficial primária localizada e lida.
- **Validação:** conferida por segunda pessoa (orientador/contador) contra a fonte.
- **Implementação:** regra codificada em dados (`rules.json`) e motor.
- **Testes:** casos de teste automatizados com valores rastreáveis à fonte.

Entradas e saídas abaixo vêm da [especificação do MVP](../project/mvp-specification.md) e não são dados fiscais.
O campo "Fonte oficial primária" traz só o órgão prioritário onde procurar; não é fonte validada.

## TR-001 — IRPF mensal 2026

| Campo | Valor |
|-------|-------|
| ID | TR-001 |
| Nome | IRPF mensal 2026 |
| Módulo | Pessoa Física / Autônomo |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Determinar o imposto de renda mensal incidente sobre a renda da pessoa física. |
| Entradas necessárias | ano; renda mensal; base considerada (deduções somente se suportadas) |
| Saídas produzidas | IRPF estimado |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: Receita Federal) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-002 — Contribuição previdenciária do contribuinte individual

| Campo | Valor |
|-------|-------|
| ID | TR-002 |
| Nome | Contribuição previdenciária do contribuinte individual |
| Módulo | Pessoa Física / Autônomo |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Determinar a contribuição previdenciária do profissional autônomo. |
| Entradas necessárias | ano; renda mensal |
| Saídas produzidas | contribuição previdenciária estimada |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: INSS / Planalto) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-003 — Limite anual e proporcional do MEI

| Campo | Valor |
|-------|-------|
| ID | TR-003 |
| Nome | Limite anual e proporcional do MEI |
| Módulo | MEI |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Determinar a situação do faturamento frente ao limite do MEI. |
| Entradas necessárias | ano; faturamento mensal; faturamento anual; categoria/atividade |
| Saídas produzidas | situação; % do limite utilizado; alertas de incompatibilidade |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: Receita Federal / Portal do Empreendedor (Ministério do Empreendedorismo)) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-004 — Composição e cálculo do DAS-MEI

| Campo | Valor |
|-------|-------|
| ID | TR-004 |
| Nome | Composição e cálculo do DAS-MEI |
| Módulo | MEI |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Determinar o valor do DAS do MEI conforme a categoria suportada. |
| Entradas necessárias | ano; categoria/atividade |
| Saídas produzidas | DAS estimado; líquido estimado |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: Receita Federal / Portal do Simples Nacional) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-005 — Limite de receita para permanência no Simples Nacional

| Campo | Valor |
|-------|-------|
| ID | TR-005 |
| Nome | Limite de receita para permanência no Simples Nacional |
| Módulo | Simples Nacional |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Determinar se a receita do cenário permite permanecer no Simples Nacional. |
| Entradas necessárias | ano; RBT12; faturamento mensal |
| Saídas produzidas | situação de enquadramento; alertas |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: Portal do Simples Nacional / CGSN) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-006 — Tabela do Anexo III

| Campo | Valor |
|-------|-------|
| ID | TR-006 |
| Nome | Tabela do Anexo III |
| Módulo | Simples Nacional |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Fornecer faixas, alíquotas nominais e parcelas a deduzir do Anexo III. |
| Entradas necessárias | ano; RBT12 |
| Saídas produzidas | faixa; alíquota nominal; parcela a deduzir |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: Portal do Simples Nacional / CGSN / Planalto) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-007 — Tabela do Anexo V

| Campo | Valor |
|-------|-------|
| ID | TR-007 |
| Nome | Tabela do Anexo V |
| Módulo | Simples Nacional |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Fornecer faixas, alíquotas nominais e parcelas a deduzir do Anexo V. |
| Entradas necessárias | ano; RBT12 |
| Saídas produzidas | faixa; alíquota nominal; parcela a deduzir |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: Portal do Simples Nacional / CGSN / Planalto) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-008 — Fórmula da alíquota efetiva do Simples Nacional

| Campo | Valor |
|-------|-------|
| ID | TR-008 |
| Nome | Fórmula da alíquota efetiva do Simples Nacional |
| Módulo | Simples Nacional |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Definir como a alíquota efetiva é obtida a partir dos dados da tabela aplicável. |
| Entradas necessárias | RBT12; faixa; alíquota nominal; parcela a deduzir |
| Saídas produzidas | alíquota efetiva; DAS estimado |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: Portal do Simples Nacional / CGSN / Planalto) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-009 — Fator R

| Campo | Valor |
|-------|-------|
| ID | TR-009 |
| Nome | Fator R |
| Módulo | Simples Nacional |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Definir o critério que determina o anexo aplicável às atividades sujeitas ao Fator R. |
| Entradas necessárias | folha dos últimos 12 meses; RBT12; pró-labore |
| Saídas produzidas | Fator R; anexo aplicável (III ou V) |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: Portal do Simples Nacional / CGSN / Planalto) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-010 — Pró-labore e contribuição previdenciária do sócio

| Campo | Valor |
|-------|-------|
| ID | TR-010 |
| Nome | Pró-labore e contribuição previdenciária do sócio |
| Módulo | Pessoa Jurídica |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Determinar a contribuição previdenciária (e eventual IRPF) associada ao pró-labore. |
| Entradas necessárias | ano; pró-labore |
| Saídas produzidas | contribuição previdenciária do pró-labore; eventual IRPF do pró-labore |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: INSS / Receita Federal / Planalto) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-011 — Distribuição de lucros relevante ao comparador PF x PJ

| Campo | Valor |
|-------|-------|
| ID | TR-011 |
| Nome | Distribuição de lucros relevante ao comparador PF x PJ |
| Módulo | Pessoa Jurídica |
| Ano de vigência | Alvo do MVP: 2026. Vigência legal: PENDENTE |
| Objetivo da regra | Definir o tratamento tributário da distribuição de lucros que afete o comparador. |
| Entradas necessárias | ano; faturamento; resultado distribuível (a definir) |
| Saídas produzidas | tratamento da distribuição de lucros no cenário PJ |
| Fórmula/regra | PENDENTE |
| Fonte oficial primária | PENDENTE (órgão prioritário: Receita Federal / Ministério da Fazenda / Planalto) |
| URL | PENDENTE |
| Base legal | PENDENTE |
| Artigo/item relevante | PENDENTE |
| Data da consulta | PENDENTE |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | PENDENTE |
| Casos especiais | PENDENTE |
| Status de pesquisa | PENDENTE |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |
