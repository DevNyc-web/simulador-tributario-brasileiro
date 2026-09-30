# Fontes Tributárias

Nenhuma regra pode entrar em `data/tax_rules/` sem linha validada nesta tabela.
Cada fonte se relaciona explicitamente a um ou mais IDs de [tax-rule-catalog.md](tax-rule-catalog.md).

## Fontes permitidas (prioridade)

Receita Federal · Portal do Simples Nacional · CGSN · Planalto (legislação federal) · INSS · Ministério da Fazenda · Ministério do Empreendedorismo · Diário Oficial (quando necessário).

Fontes secundárias servem só para **descoberta**; nunca são fonte final de fórmula do motor.

## Fluxo por regra

`TR-XXX` → órgão → documento/tabela → URL → legislação → data da consulta → validação.

## Registro

Um ID TR pode ter várias fontes (uma linha por fonte); uma fonte pode atender vários IDs (liste-os na coluna ID TR).

| ID TR | Regra | Tributo | Ano | Fonte oficial | Documento/tabela | URL | Legislação | Data da consulta | Status de validação | Observações |
|-------|-------|---------|-----|---------------|------------------|-----|------------|------------------|---------------------|-------------|
| TR-001 | IRPF mensal 2026 | PENDENTE | 2026 | PENDENTE (prioritário: Receita Federal) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
| TR-002 | Contribuição previdenciária do contribuinte individual | PENDENTE | 2026 | PENDENTE (prioritário: INSS / Planalto) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
| TR-003 | Limite anual e proporcional do MEI | PENDENTE | 2026 | PENDENTE (prioritário: Receita Federal / Portal do Empreendedor (Ministério do Empreendedorismo)) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
| TR-004 | Composição e cálculo do DAS-MEI | PENDENTE | 2026 | PENDENTE (prioritário: Receita Federal / Portal do Simples Nacional) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
| TR-005 | Limite de receita para permanência no Simples Nacional | PENDENTE | 2026 | PENDENTE (prioritário: Portal do Simples Nacional / CGSN) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
| TR-006 | Tabela do Anexo III | PENDENTE | 2026 | PENDENTE (prioritário: Portal do Simples Nacional / CGSN / Planalto) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
| TR-007 | Tabela do Anexo V | PENDENTE | 2026 | PENDENTE (prioritário: Portal do Simples Nacional / CGSN / Planalto) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
| TR-008 | Fórmula da alíquota efetiva do Simples Nacional | PENDENTE | 2026 | PENDENTE (prioritário: Portal do Simples Nacional / CGSN / Planalto) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
| TR-009 | Fator R | PENDENTE | 2026 | PENDENTE (prioritário: Portal do Simples Nacional / CGSN / Planalto) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
| TR-010 | Pró-labore e contribuição previdenciária do sócio | PENDENTE | 2026 | PENDENTE (prioritário: INSS / Receita Federal / Planalto) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
| TR-011 | Distribuição de lucros relevante ao comparador PF x PJ | PENDENTE | 2026 | PENDENTE (prioritário: Receita Federal / Ministério da Fazenda / Planalto) | PENDENTE | PENDENTE | PENDENTE | PENDENTE | [REGRA PENDENTE DE VALIDAÇÃO] | |
