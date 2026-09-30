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
| Ano de vigência | 2026 (a partir de janeiro; Lei 15.270/2025, art. 8º) |
| Objetivo da regra | Determinar o imposto de renda mensal (Carnê-Leão) do autônomo que presta serviços a pessoas físicas. |
| Entradas necessárias | ano; rendimento tributável do mês; contribuição previdenciária oficial paga pelo contribuinte (TR-002); escolha entre deduções legais e desconto simplificado (o mais benéfico) |
| Saídas produzidas | base de cálculo; imposto pela tabela; redução de 2026; imposto devido |
| Fórmula/regra | Ver [pf-2026-research.md](pf-2026-research.md), seções Tabela progressiva, Redução de 2026 e Ordem de cálculo. Resumo: base = rendimento − (deduções legais ou desconto simplificado, o mais benéfico); imposto = base × alíquota − parcela a deduzir; redução calculada sobre o rendimento tributável, limitada ao imposto; devido = imposto − redução. Arredondamento: QUESTÃO EM ABERTO (Q-02). |
| Fonte oficial primária | Receita Federal (F-01, F-02, F-03, F-04, F-05, F-06); Planalto (F-08 Lei 15.270/2025; F-09 Lei 9.250/1995); F-07 (Perguntas e Respostas IRPF 2026, ano-calendário 2025, só conceitual); F-10 (IN RFB 1.500/2014, texto não obtido); F-19 (Simulador Oficial da Receita, evidência operacional complementar) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-01 a F-10 e F-19 |
| Base legal | Lei nº 9.250/1995 (arts. 3º-A e 4º); Lei nº 15.270/2025; IN RFB nº 1.500/2014 (citada; texto não obtido) |
| Artigo/item relevante | Lei 9.250/1995, art. 3º-A (redução; §§ 1º e 2º) e art. 4º (deduções; § 2º desconto simplificado); Lei 15.270/2025, arts. 2º e 8º |
| Data da consulta | 2026-09-29 |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md), premissa 11 |
| Limitações do MVP | Sem dependentes, pensão alimentícia, Livro Caixa, rendimentos do exterior, tomadores PJ e casos especiais (exclusão deliberada; existem legalmente) |
| Casos especiais | Ver seção Casos especiais fora do MVP em [pf-2026-research.md](pf-2026-research.md) |
| Questões em aberto | Q-01 e Q-03 RESOLVIDAS. Abertas: Q-02 (arredondamento, QUESTÃO EM ABERTO), Q-04 (texto da IN 1.500) e itens de baixa prioridade Q-05 a Q-08. Detalhes em [pf-2026-research.md](pf-2026-research.md) |
| Status de pesquisa | PESQUISADA |
| Status de validação | PENDENTE |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-002 — Contribuição previdenciária do contribuinte individual

| Campo | Valor |
|-------|-------|
| ID | TR-002 |
| Nome | Contribuição previdenciária do contribuinte individual |
| Módulo | Pessoa Física / Autônomo |
| Ano de vigência | 2026 (Portaria Interministerial MPS/MF nº 13, de 09/01/2026) |
| Objetivo da regra | Determinar a contribuição previdenciária do autônomo por conta própria, conforme o plano escolhido. |
| Entradas necessárias | ano; plano (normal ou simplificado, escolhido pelo usuário); remuneração mensal do trabalho por conta própria (base do plano normal) |
| Saídas produzidas | contribuição previdenciária; avisos educacionais; valor dedutível para TR-001 |
| Fórmula/regra | Ver [pf-2026-research.md](pf-2026-research.md), seções Plano normal, Plano simplificado e Limites 2026. Resumo: plano normal 20% sobre o salário de contribuição (remuneração mensal do trabalho por conta própria, entre o limite mínimo e o teto); plano simplificado 11% sobre o limite mínimo (salário mínimo). Base do plano normal: Q-P1 RESOLVIDA (Lei 8.212/1991, art. 28, III). Tratamento abaixo do limite mínimo: Q-P6 em aberto. |
| Fonte oficial primária | INSS (F-11, F-12, F-13, F-17, F-18); Planalto (F-14 Lei 8.212/1991); Ministério da Previdência Social/DOU (F-15 Portaria MPS/MF 13/2026); Receita Federal (F-16 Agenda Tributária 2026; F-05, F-07, F-09 para dedutibilidade) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-11 a F-18 |
| Base legal | Lei nº 8.212/1991 (arts. 21, 28 III e § 3º, 30 II); Portaria Interministerial MPS/MF nº 13, de 09/01/2026 (art. 2º; lida no DOU); LC nº 123/2006 e Decreto nº 6.042/2007 (citados em F-13) |
| Artigo/item relevante | Lei 8.212/1991, art. 28, III (salário de contribuição do contribuinte individual), art. 21 (alíquotas) e art. 30, II (vencimento); Portaria MPS/MF 13/2026, art. 2º (mínimo R$ 1.621,00 e máximo R$ 8.475,55) |
| Data da consulta | 2026-09-29 |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md), premissa 11; usuário seleciona o plano |
| Limitações do MVP | Sem tomador PJ (plano simplificado não se aplica a quem presta serviço a empresas), sem MEI, sem facultativo; complementação de 9% fora do cálculo |
| Casos especiais | Prestação de serviço a empresa (responsabilidade da empresa desde 04/2003, F-12); MEI 5%; facultativo baixa renda 5% |
| Questões em aberto | Q-P1, Q-P2 e Q-P4 RESOLVIDAS. Q-P3 FORA DO CÁLCULO DO MVP 1.0 / AVISO EDUCACIONAL. Abertas: Q-P6 (remuneração abaixo do limite mínimo; decisão de produto). Registrada: Q-P5. Detalhes em [pf-2026-research.md](pf-2026-research.md) |
| Status de pesquisa | PESQUISADA |
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
