# Requisitos do MVP

> **Status posterior (MVP final):** especificação original das fases iniciais, preservada como histórico. Todos os valores fiscais hoje vêm de regras validadas (TR-001 a TR-011) em `data/tax_rules/2026/rules.json`; o relatório final consolida os requisitos implementados (RF-01..RF-14, RNF-01..RNF-14) em [../academic/relatorio-final.md](../academic/relatorio-final.md), seção 9.
>
> Itens desta especificação **não entregues ou parciais** na versão final: RF-002 (renda anual automática na tela), RF-003/RF-012/RF-016/RF-017 (exibição de **carga efetiva** em percentual), RF-008 e CA-03 (botão MEI → Simples com dados preservados), RF-018 (diferença **anual** no comparador), RF-020 (gráfico), RF-023 e CA-07 (**atendidos depois**: a linha do tempo da Reforma agora exibe conteúdo educacional por etapa, com fonte oficial; o placeholder de pendência não é mais usado), RF-030 (preservar dados entre telas) e a seleção de ano nas telas (a interface opera em 2026; VAL-01 e RF-028 ficam restritos a esse ano). Os demais requisitos foram atendidos ou reformulados conforme o relatório final.

> Nenhum valor tributário (alíquota, faixa, limite, teto) é definido neste documento.
> Todo valor fiscal é `[REGRA PENDENTE DE VALIDAÇÃO]` até constar em `docs/research/fontes-tributarias.md` com fonte oficial.

## 1. Requisitos funcionais

### Pessoa Física / Autônomo
| ID | Requisito |
|----|-----------|
| RF-001 | O usuário informa ano, renda mensal e perfil de recebimento na tela PF. |
| RF-002 | O sistema calcula e exibe a renda anual (renda mensal × 12) automaticamente, sem regra fiscal. |
| RF-003 | O sistema exibe: renda bruta, base considerada, IRPF estimado, contribuição previdenciária (quando aplicável), total de tributos, carga efetiva, renda líquida. |
| RF-004 | Despesas/deduções só aparecem como campo quando houver regra validada que as suporte. |
| RF-005 | O resultado PF traz explicação passo a passo do cálculo, citando a regra e a fonte usadas. |

### MEI
| ID | Requisito |
|----|-----------|
| RF-006 | O usuário informa ano, faturamento mensal e atividade/categoria suportada. |
| RF-007 | O sistema exibe faturamento anual, situação frente ao limite, % do limite utilizado, DAS estimado e valor líquido. |
| RF-008 | Se o cenário exceder o limite ou for incompatível, o sistema exibe alerta e o botão "Simular no Simples Nacional", levando os dados já informados. |

### Simples Nacional
| ID | Requisito |
|----|-----------|
| RF-009 | O usuário informa ano, faturamento mensal, RBT12, folha 12 meses, pró-labore, atividade e categoria de serviço. |
| RF-010 | O sistema calcula e exibe o Fator R e o anexo aplicável (III ou V, quando suportado). |
| RF-011 | O sistema exibe faixa, alíquota nominal, parcela a deduzir, alíquota efetiva e DAS estimado. |
| RF-012 | O sistema exibe contribuição do pró-labore, carga total, percentual efetivo e líquido estimado. |
| RF-013 | O resultado traz explicação detalhada de cada etapa. |
| RF-014 | Atividades fora do suporte do MVP geram mensagem clara de "não suportado", sem cálculo aproximado. |

### Comparador PF x PJ
| ID | Requisito |
|----|-----------|
| RF-015 | O usuário informa um cenário único e vê PF e PJ lado a lado. |
| RF-016 | Coluna PF: renda bruta, IRPF, contribuição previdenciária, total de tributos, carga efetiva, líquido. |
| RF-017 | Coluna PJ: faturamento, regime, DAS, pró-labore, contribuição previdenciária, eventual IRPF do pró-labore, total, carga efetiva, líquido. |
| RF-018 | O sistema exibe diferença mensal e anual (valores absolutos, com sinal e sentido explícitos). |
| RF-019 | O sistema NÃO declara opção "melhor"; apresenta diferenças e premissas. |
| RF-020 | Espaço para gráfico comparativo e texto explicativo (gráfico: Should). |

### Reforma Tributária
| ID | Requisito |
|----|-----------|
| RF-021 | Timeline interativa com os anos 2026 a 2033. |
| RF-022 | Ao selecionar um ano: resumo, tributos envolvidos, etapa da transição, observações e fonte oficial. |
| RF-023 | Enquanto não validado, cada campo exibe `[CONTEÚDO PENDENTE DE VALIDAÇÃO]`. |

### Transversais
| ID | Requisito |
|----|-----------|
| RF-024 | Tela de escolha de simulação (PF, MEI, Simples, Comparador). |
| RF-025 | Página Sobre / Metodologia: finalidade, fontes, limitações, aviso educacional. |
| RF-026 | Aviso "Ferramenta educacional. Não substitui orientação contábil ou jurídica." em todas as páginas. |
| RF-027 | Toda regra usada em um resultado é rastreável a uma entrada em `fontes-tributarias.md` (ano, fonte, status). |
| RF-028 | Se o ano escolhido não tiver regras validadas, o sistema informa e não calcula. |
| RF-029 | Entradas inválidas são rejeitadas com mensagem por campo, antes de chegar ao motor. |
| RF-030 | Resultado permite "Comparar cenário" e "Nova simulação" preservando os dados. |

## 2. Requisitos não funcionais

| ID | Requisito |
|----|-----------|
| RNF-001 | Cálculos tributários exclusivamente em `src/tax_engine`; nunca em HTML, JS ou rotas. |
| RNF-002 | Regras versionadas por ano em `data/tax_rules/<ano>/`; nenhuma constante fiscal em código. |
| RNF-003 | Camadas: Interface → Services → Tax Engine → Tax Rules → Dados. Dependência só no sentido descendente. |
| RNF-004 | Cobertura de testes ≥ 80% no `tax_engine`, `tax_rules` e `services`. |
| RNF-005 | Motor testável sem Flask (funções puras, entradas/saídas por dataclass). |
| RNF-006 | Layout responsivo (≥ 320 px), sem scroll horizontal. |
| RNF-007 | Stack: Python/Flask, HTML/CSS/JS puros; sem frameworks frontend; sem banco no MVP. |
| RNF-008 | Acessibilidade básica: labels associados, foco visível, contraste legível, navegação por teclado. |
| RNF-009 | Valores monetários com `Decimal`; nunca `float`. |
| RNF-010 | Resposta de simulação < 1 s em máquina comum. |
| RNF-011 | Nenhum dado pessoal persistido; simulações não são armazenadas no MVP. |
| RNF-012 | Mensagens e textos em português do Brasil. |
| RNF-013 | Regras não validadas nunca produzem número: retornam estado pendente. |

## 3. Regras de validação de entrada

Limites numéricos fiscais não são definidos aqui; apenas validações estruturais.

| ID | Regra | Mensagem |
|----|-------|----------|
| VAL-01 | Ano ∈ {2026..2033} e presente em `SUPPORTED_YEARS`. | "Selecione um ano entre 2026 e 2033." |
| VAL-02 | Valores monetários: obrigatórios, numéricos, ≥ 0, até 2 casas decimais. | "Informe um valor válido (ex.: 5000,00)." |
| VAL-03 | Renda/faturamento mensal > 0 para simular. | "Informe um valor maior que zero." |
| VAL-04 | Aceita vírgula ou ponto decimal; normalizado no servidor. | — |
| VAL-05 | Campos de seleção (perfil, atividade, categoria) devem ser opção listada. | "Escolha uma das opções." |
| VAL-06 | RBT12 e folha ≥ 0; obrigatórios no Simples. | "Informe o valor acumulado dos últimos 12 meses." |
| VAL-07 | Pró-labore ≥ 0; ≤ faturamento mensal informado (aviso, não bloqueio). | "Pró-labore maior que o faturamento: confira os dados." |
| VAL-08 | Validação JS é só conveniência; o servidor revalida sempre. | — |
| VAL-09 | Valores implausíveis (ex.: > teto técnico de campo) rejeitados por tamanho, não por regra fiscal. | "Valor fora do intervalo aceito." |

## 4. Casos de uso principais

| ID | Caso de uso | Ator | Resultado |
|----|-------------|------|-----------|
| UC-01 | Simular Pessoa Física | Usuário | Resultado PF explicado. |
| UC-02 | Simular MEI | Usuário | Situação e DAS; alerta e atalho ao Simples se incompatível. |
| UC-03 | Simular Simples Nacional | Usuário | Fator R, anexo, DAS, carga e explicação. |
| UC-04 | Comparar PF x PJ | Usuário | Colunas lado a lado, diferenças, sem veredito. |
| UC-05 | Explorar Reforma 2026–2033 | Usuário | Detalhe educacional por ano. |
| UC-06 | Consultar metodologia | Usuário | Fontes, premissas e limites. |

## 5. Critérios de aceite

| ID | Critério (Dado / Quando / Então) | Reqs |
|----|-----------------------------------|------|
| CA-01 | Dado renda mensal válida na tela PF, quando envia, então vê todos os itens de RF-003 e a explicação. | RF-001..005 |
| CA-02 | Dado ano sem regra validada, quando simula, então recebe aviso de pendência e nenhum valor numérico. | RF-028, RNF-013 |
| CA-03 | Dado faturamento acima do limite MEI, então vê alerta e botão "Simular no Simples Nacional" com dados preservados. | RF-008 |
| CA-04 | Dado dados do Simples completos, então vê Fator R, anexo, faixa, alíquotas, DAS e explicação. | RF-009..013 |
| CA-05 | Dado atividade não suportada, então vê "não suportado" e nenhum cálculo. | RF-014 |
| CA-06 | Dado cenário no comparador, então vê PF e PJ lado a lado, diferenças mensal/anual e nenhuma frase "melhor/pior". | RF-015..019 |
| CA-07 | Dado clique em um ano da timeline, então vê os 5 campos do ano (ou o placeholder pendente). | RF-021..023 |
| CA-08 | Dado campo inválido, então a mensagem aparece junto ao campo e nada é enviado ao motor. | RF-029, VAL-* |
| CA-09 | Dado tela de 320 px, então não há scroll horizontal e todos os controles são acionáveis. | RNF-006 |
| CA-10 | `grep` por números fiscais em `templates/`, `static/js/`, `app.py` não encontra regra. | RNF-001 |
| CA-11 | `pytest --cov` reporta ≥ 80% nos módulos do núcleo. | RNF-004 |
| CA-12 | Cada regra em `rules.json` com dados tem linha "validada" em `fontes-tributarias.md`. | RF-027 |
