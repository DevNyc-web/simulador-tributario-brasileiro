# Matriz de Regras Tributárias

Resumo de [tax-rule-catalog.md](tax-rule-catalog.md). Atualizar as duas juntas.

| ID | Regra | Módulo | Ano | Fonte | Pesquisa | Validação | Implementação | Testes |
|----|-------|--------|-----|-------|----------|-----------|---------------|--------|
| TR-001 | IRPF mensal 2026 | Pessoa Física / Autônomo | 2026 | F-01..F-10, F-19, F-20 | PESQUISADA | VALIDADA | IMPLEMENTADA | TESTADA |
| TR-002 | Contribuição previdenciária do contribuinte individual | Pessoa Física / Autônomo | 2026 | F-11..F-18, F-21, F-22, F-47 | PESQUISADA | VALIDADA | IMPLEMENTADA | TESTADA |
| TR-003 | Limite anual e proporcional do MEI | MEI | 2026 | F-23, F-25, F-26, F-27, F-28, F-31 | PESQUISADA | VALIDADA | IMPLEMENTADA | TESTADA |
| TR-004 | Composição e cálculo do DAS-MEI | MEI | 2026 | F-23, F-24, F-27, F-29, F-30, F-31 | PESQUISADA | VALIDADA | IMPLEMENTADA | TESTADA |
| TR-005 | Limite de receita para permanência no Simples Nacional | Simples Nacional | 2026 | F-23, F-32, F-34, F-35, F-36 | PESQUISADA | VALIDADA | PENDENTE | PENDENTE |
| TR-006 | Tabela do Anexo III | Simples Nacional | 2026 | F-23, F-32, F-34 | PESQUISADA | VALIDADA | PENDENTE | PENDENTE |
| TR-007 | Tabela do Anexo V | Simples Nacional | 2026 | F-23, F-32, F-34 | PESQUISADA | VALIDADA | PENDENTE | PENDENTE |
| TR-008 | Fórmula da alíquota efetiva do Simples Nacional | Simples Nacional | 2026 | F-23, F-32, F-34 | PESQUISADA | VALIDADA | PENDENTE | PENDENTE |
| TR-009 | Fator R | Simples Nacional | 2026 | F-23, F-32, F-34, F-38 | PESQUISADA | VALIDADA | PENDENTE | PENDENTE |
| TR-010 | Pró-labore e contribuição previdenciária do sócio | Pessoa Jurídica | 2026 | F-23/F-34, F-40, F-41, F-18, F-21, F-22 | PESQUISADA | VALIDADA | PENDENTE | PENDENTE |
| TR-011 | Distribuição de lucros relevante ao comparador PF x PJ | Pessoa Jurídica | 2026 | F-23/F-34, F-39, F-42, F-43, F-44, F-45, F-46 | PESQUISADA | VALIDADA | PENDENTE | PENDENTE |

Detalhes e questões em aberto de TR-001/TR-002: [pf-2026-research.md](pf-2026-research.md). Detalhes e questões em aberto de TR-003/TR-004: [mei-2026-research.md](mei-2026-research.md). Detalhes e questões em aberto de TR-005 a TR-009: [simples-2026-research.md](simples-2026-research.md). Detalhes e questões em aberto de TR-010/TR-011: [pj-comparator-2026-research.md](pj-comparator-2026-research.md). **Estado final desta fase de pesquisa**: TR-001 a TR-011 alcançaram `VALIDADA` (TR-001–004 em 2026-09-29; TR-005–011 em 2026-09-30, após passagens finais de validação). TR-001 a TR-004 estão `IMPLEMENTADA` e `TESTADA` (Fases 4B e 4C); TR-005 a TR-011 permanecem com Implementação e Testes `PENDENTE`.
