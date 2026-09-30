# Pessoa Física / Autônomo — 2026

Pesquisa de TR-001 (IRPF / Carnê-Leão) e TR-002 (Previdência do contribuinte individual).
Data da consulta: **2026-09-29** (primeira pesquisa) e **2026-09-29** (ajustes da revisão independente). Status: **PESQUISADA** (não **VALIDADA**; validação de TR-001 e TR-002 segue PENDENTE).

> Todo número deste documento foi copiado de fonte oficial listada em "Fontes" (IDs `F-xx`) ou é marcado como *aritmética de conferência* (não é fonte).
> Nada aqui está implementado. Nenhum valor entrou em `data/tax_rules/`.

## Escopo

Cenário aprovado para o MVP (premissa 11 em [calculation-assumptions.md](calculation-assumptions.md)):

- pessoa física residente no Brasil;
- profissional autônomo, prestação de serviços sem vínculo empregatício, por conta própria;
- rendimentos recebidos de **outras pessoas físicas no Brasil**;
- ano-calendário 2026.

Fora do escopo inicial (limitação **deliberada** da primeira versão; os itens existem legalmente):
rendimentos do exterior; serviços prestados a pessoa jurídica; transporte de cargas; transporte de passageiros; representante comercial em situações especiais; leiloeiro; atividade notarial; múltiplas fontes com tratamentos diferentes; **dependentes**; **pensão alimentícia**; **Livro Caixa**.

Existência legal dessas deduções: F-09 (art. 4º, incisos II e III e referência ao art. 6º da Lei 8.134/1990 no inciso I), F-05 (dependentes, pensão alimentícia e Livro Caixa listados como deduções do Carnê-Leão) e F-07 (pergunta 267, itens I, II e VI).

---

## TR-001 — IRPF / Carnê-Leão

### Incidência

- Definição: "Carnê-leão é o imposto sobre a renda mensal de pessoa física residente no Brasil recebida de outra pessoa física ou do exterior." (F-03)
- Sujeita-se ao recolhimento mensal obrigatório a pessoa física residente no Brasil que receber "rendimentos de outras pessoas físicas que não tenham sido tributados na fonte no Brasil, [...] e os decorrentes do trabalho não assalariado, assim compreendidas todas as espécies de remuneração por serviços ou trabalhos prestados sem vínculo empregatício". (F-07, pergunta 266, item 1)
- "Os rendimentos tributados na fonte (salários, por exemplo) pelo imposto de renda não entram no cálculo do carnê-leão." (F-03)
- Prazo: "O imposto deve ser pago até o último dia útil do mês subsequente ao do recebimento do rendimento." (F-03); código de recolhimento 0190 (F-07, pergunta 267).
- Os rendimentos do Carnê-Leão também entram na Declaração de Ajuste Anual; o imposto pago é antecipação (F-07, pergunta 266). *A DAA está fora do escopo do MVP.*
- Tributação sobre "o total recebido no mês", pela tabela vigente no mês do recebimento (F-07, pergunta 267); havendo mais de um recebimento no mês, somam-se (F-07, p. 140; pergunta 267 na p. 139).

**Conclusão (A):** o autônomo do cenário aprovado (serviços a pessoas físicas, sem vínculo) está sujeito ao Carnê-Leão, conforme F-07 (item 1) e F-04 ("Trabalho sem vínculo empregatício").

### Regime mensal aplicável em 2026 (B)

Tabela progressiva mensal "a partir de janeiro de 2026" (F-01) e redução mensal do imposto a partir de janeiro de 2026 (F-08, art. 3º-A da Lei 9.250/1995, incluído pela Lei 15.270/2025; F-01). A Lei 15.270/2025 "entra em vigor na data de sua publicação e produzirá efeitos a partir de 1º de janeiro de 2026" (F-08, art. 8º).

### Deduções

Base de cálculo mensal do Carnê-Leão: podem ser deduzidas, "observados os limites e condições fixados na legislação pertinente e desde que não tenham sido deduzidos de outros rendimentos auferidos no mês sujeitos à tributação na fonte" (F-07, pergunta 267; F-05):

| Dedução | Fonte |
|---------|-------|
| pensão alimentícia (decisão judicial etc.) | F-07 (I), F-09 art. 4º II, F-05 |
| dependentes — F-01: "Dedução mensal por dependente: R$ 189,59" | F-01, F-07 (II), F-05 |
| contribuições à Previdência Social da União, dos estados, do DF e dos municípios, "cujo ônus tenha sido do próprio contribuinte e desde que destinado a seu próprio benefício" | F-07 (III), F-09 art. 4º IV, F-05 ("Previdência oficial") |
| previdência complementar / Fapi (condições específicas) | F-07 (IV, V) |
| despesas escrituradas em livro-caixa (limitada ao rendimento recebido no mês) | F-07 (VI), F-05 |

**Dedutibilidade da previdência oficial paga pelo próprio contribuinte (TR-002 D):** confirmada por F-07 (III), F-09 (art. 4º, IV) e F-05. No MVP só esta dedução (e o desconto simplificado) entra; as demais estão fora do escopo.

### Desconto simplificado

- "Alternativamente às deduções [...], poderá ser utilizado desconto simplificado mensal, correspondente a 25% (vinte e cinco por cento) do valor máximo da faixa com alíquota zero da tabela progressiva mensal, caso seja mais benéfico ao contribuinte, dispensadas a comprovação da despesa e a indicação de sua espécie." (F-09, art. 4º, § 2º, redação da Lei 14.663/2023; F-07, pergunta 267)
- Valor de 2026 informado pela Receita: "Limite mensal de desconto simplificado: R$ 607,20" (F-01).
- *Aritmética de conferência (não é fonte):* 25% × R$ 2.428,80 (limite da faixa zero em F-01) = R$ 607,20.
- **Regra de comparação (Q-03 RESOLVIDA):** o desconto simplificado mensal **substitui** as deduções legais quando for mais benéfico ao contribuinte (F-09, art. 4º, § 2º: "Alternativamente às deduções [...], poderá ser utilizado desconto simplificado mensal [...], caso seja mais benéfico ao contribuinte"; F-07, pergunta 267). O Simulador Oficial da Receita de 2026 (F-19) traz o campo "Dedução utilizada" com a nota "Mais benéfica entre total das deduções ou desconto simplificado mensal" (texto do código publicado do simulador; comportamento numérico não executado por nós). Os exemplos oficiais demonstram a comparação: Rita usa a dedução legal de R$ 649,60, maior que o simplificado de R$ 607,20 (F-02). Portanto a comparação é entre o **total das deduções** e o **desconto simplificado mensal**.

### Tabela progressiva

Tabela de incidência mensal, "a partir de janeiro de 2026" (F-01, copiada literalmente; "Dedução" = parcela a deduzir):

| Base de cálculo | Alíquota | Parcela a deduzir |
|---|---|---|
| Até R$ 2.428,80 | — | — |
| De R$ 2.428,81 até R$ 2.826,65 | 7,5% | R$ 182,16 |
| De R$ 2.826,66 até R$ 3.751,05 | 15,0% | R$ 394,16 |
| De R$ 3.751,06 até R$ 4.664,68 | 22,5% | R$ 675,49 |
| Acima de R$ 4.664,68 | 27,5% | R$ 908,73 |

Fórmula usada nos exemplos oficiais: `imposto = base × alíquota − parcela a deduzir` (F-02; F-07, exemplo do Darf de R$ 20,36).

### Redução de 2026

Texto legal (F-08, art. 3º-A da Lei 9.250/1995):

- "A partir do mês de janeiro do ano-calendário de 2026, será concedida redução do imposto sobre os rendimentos tributáveis sujeitos à incidência mensal [...]".

| Rendimentos tributáveis sujeitos ao ajuste mensal | Redução do imposto de renda |
|---|---|
| até R$ 5.000,00 | até R$ 312,89 (de modo que o imposto devido seja zero) |
| de R$ 5.000,01 até R$ 7.350,00 | R$ 978,62 − (0,133145 × rendimentos tributáveis sujeitos à incidência mensal) (de modo que a redução do imposto seja decrescente linearmente até zerar para rendimentos a partir de R$ 7.350,00) |

- § 1º: "O valor da redução [...] fica limitado ao valor do imposto determinado de acordo com a tabela progressiva mensal e com o disposto no art. 4º desta Lei."
- § 2º: quem tiver rendimentos tributáveis sujeitos à incidência mensal superior a R$ 7.350,00 "não terá redução no imposto devido".
- Mesma tabela e fórmula em F-01.

**F — Valor usado para enquadrar a faixa da redução:** o **rendimento tributável sujeito à incidência mensal** (antes das deduções e do desconto simplificado), **não** a base de cálculo. Sustentação: texto legal ("rendimentos tributáveis sujeitos à incidência mensal", F-08); F-01 (coluna "Rendimentos Tributáveis"); e F-02, exemplos 4 e 5, que afirmam expressamente o uso do rendimento (R$ 6.000,00 e R$ 7.607,20) e não da base (R$ 5.350,40 e R$ 7.000,00).
*Ressalva (Q-01 RESOLVIDA):* os exemplos publicados em F-02 são de **IRRF sobre salários**, mas a aplicabilidade ao recolhimento mensal (Carnê-Leão) decorre do **texto legal**, não da natureza salarial dos exemplos: o art. 3º-A da Lei 9.250/1995, com a redação da Lei 15.270/2025, aplica a redução aos "rendimentos tributáveis sujeitos à incidência mensal do Imposto sobre a Renda das Pessoas Físicas" (F-08; F-09). Evidência operacional complementar: o Simulador Oficial da Receita de 2026 (F-19) contempla o cálculo mensal, o Livro Caixa de Carnê-Leão ("Carne-Leão: Livro Caixa") e traz o campo "Redução" com a nota "Para mais informações sobre redução verificar Lei nº 15.270/2025" (texto do código publicado; comportamento numérico não executado por nós).

### Ordem de cálculo

Sequência sustentada pelas fontes (F-08 art. 3º-A § 1º; F-09 art. 4º e § 2º; F-02 exemplos; F-07 pergunta 267):

1. rendimento tributável do mês (total recebido no mês);
2. deduções legais **ou** desconto simplificado (o mais benéfico) → **base de cálculo**;
3. aplicação da tabela progressiva → **imposto antes da redução**;
4. redução de 2026, calculada sobre o **rendimento tributável** (não sobre a base), **limitada ao imposto do passo 3**;
5. **imposto devido** = imposto do passo 3 − redução.

Confirmada pelos exemplos numéricos de F-02 (ver "Casos de teste futuros"). Enquadramento da faixa da redução: passo 1 (Questão F).

### Casos especiais fora do MVP

Rendimentos do exterior; serviços a embaixadas e organismos internacionais; transporte de carga (mínimo 10% tributável) e de passageiros (mínimo 60% tributável); representante comercial; leiloeiro; serventuários da Justiça; aluguéis; dependentes; pensão alimentícia; Livro Caixa; previdência complementar; 13º salário (F-08 § 3º); recolhimento complementar (F-04, F-07, F-08).

### Questões em aberto

| # | Questão | Situação |
|---|---------|----------|
| Q-01 | Redução de 2026 no cálculo mensal (enquadramento pelo rendimento tributável). | **RESOLVIDA** — Lei 9.250/1995, art. 3º-A, redação da Lei 15.270/2025 (F-08, F-09); evidência complementar: F-19. Exemplos de F-02 são de IRRF; a aplicabilidade decorre do texto legal. |
| Q-02 | **Arredondamento:** as fontes consultadas não trazem regra explícita. Os exemplos oficiais têm valores em centavos e a redução (0,133145 × rendimento) pode gerar mais de duas casas. | **QUESTÃO EM ABERTO.** Não inferir política de arredondamento somente pelos exemplos; não definir no motor sem orientação oficial. |
| Q-03 | Dedução mais benéfica (deduções legais × desconto simplificado). | **RESOLVIDA** — F-09 art. 4º § 2º; F-07 pergunta 267; F-19 ("Dedução utilizada"); exemplos de F-02. |
| Q-04 | Texto integral da **IN RFB nº 1.500/2014** (versão vigente; Anexo X — tabela de redução; art. 52; Anexo II). | Aberta. Não obtido: o portal `normas.receita.fazenda.gov.br` não entregou o texto. Citada apenas via F-07. A regra de redução está sustentada pela lei (F-08). |
| Q-05 | Página "Receita Federal orienta fontes pagadoras e contribuintes a calcular a redução..." (notícia de dez/2025). | Aberta (baixa prioridade). Retornou "conteúdo restrito"; não usada. |
| Q-06 | O F-01 chama R$ 607,20 de "limite mensal"; a lei diz "correspondente a 25%". | Aberta (baixa prioridade). Aparente equivalência; não confirmada. |
| Q-07 | Valor mínimo de recolhimento do Carnê-Leão (Darf) e multa/juros por atraso. | Aberta. Não pesquisado (fora do cálculo do imposto devido do MVP). |
| Q-08 | O Manual do Carnê-Leão (F-06) e as páginas F-03/F-05 (2023–2024) não citam o desconto simplificado nem a redução de 2026. | Registrada. Omissão de documentação oficial desatualizada; sem conflito de valores. |

### Fontes (TR-001)

F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-19 — ver [fontes-tributarias.md](fontes-tributarias.md).

**Ressalvas sobre F-07 (Perguntas e Respostas IRPF 2026):** o documento refere-se ao **exercício 2026, ano-calendário 2025**. Serve para conceito e procedimento; **não** é fonte primária dos valores de 2026. Ele traz ainda dois pontos internos inconsistentes, registrados sem tentar resolver:
(i) a pergunta 267 rotula uma tabela como "ano-calendário de 2023, durante os meses de maio a dezembro", com valores idênticos à tabela de 2026 de F-01;
(ii) a pergunta 266 remete às perguntas 474 e 475 para a redução, mas essas tratam de aplicações e entidades no exterior.

---

## TR-002 — Previdência

### Contribuinte individual

- Contribuinte individual que trabalha **por conta própria**: contribui por 20% ou pela alíquota reduzida de 11%, pagamento por GPS "até dia 15" (F-12).
- "Prestando serviço a empresa": "desde 04/2003 a responsabilidade pelo recolhimento das contribuições é da empresa" (F-12). **Não se aplica ao cenário aprovado** (serviços a pessoas físicas).
- MEI usa 5% (F-11 legenda; F-12). Fora deste módulo.

### Base do salário de contribuição (Q-P1 RESOLVIDA)

- Para o contribuinte individual, salário de contribuição é "a remuneração auferida em uma ou mais empresas ou pelo exercício de sua atividade por conta própria, durante o mês, observado o limite máximo a que se refere o § 5º" (F-14, Lei 8.212/1991, art. 28, III, redação da Lei 9.876/1999).
- Alíquota do contribuinte individual: "vinte por cento sobre o respectivo salário-de-contribuição" (F-14, art. 21, caput). O plano de 11% incide sobre "o valor correspondente ao limite mínimo mensal do salário-de-contribuição" para quem trabalha por conta própria, sem relação de trabalho com empresa, e opta pela exclusão do direito à aposentadoria por tempo de contribuição (F-14, art. 21, § 2º).
- Limite mínimo: "o salário mínimo nacional vigente na competência a ser recolhida" (F-18); a lei fala em piso da categoria ou, inexistindo, salário mínimo (F-14, art. 28, § 3º). Limite máximo: o teto previdenciário vigente (F-18). Valores de 2026 na Portaria (F-15, art. 2º): mínimo R$ 1.621,00 e máximo R$ 8.475,55.
- **Consequência para o MVP:** a base do plano normal **não** é valor arbitrariamente escolhido; relaciona-se à **remuneração mensal do trabalho por conta própria**, observados os limites mínimo e máximo.
- **Tratamento pendente (produto):** quando a remuneração ficar **abaixo do limite mínimo**, o MVP precisa de tratamento documentado (Q-P6). Não decidir sem definição de produto.

### Plano normal

| Item | Valor / regra | Fonte |
|------|---------------|-------|
| Alíquota | 20% | F-11, F-12 |
| Base | Salário de contribuição do contribuinte individual = "a remuneração auferida em uma ou mais empresas ou pelo exercício de sua atividade por conta própria, durante o mês, observado o limite máximo a que se refere o § 5º" (F-14, art. 28, III); limites mínimo e máximo aplicáveis. Ver "Base do salário de contribuição (Q-P1)" | F-14, F-12, F-18 |
| Limite mínimo (contribuição) | R$ 324,20 | F-11 |
| Limite máximo (contribuição) | R$ 1.695,11 | F-11 |
| Faixa do salário de contribuição | R$ 1.621,00 até R$ 8.475,55 | F-11 |
| Responsável pelo recolhimento | o próprio contribuinte (por conta própria), via GPS | F-12 |
| Vencimento (Q-P4 RESOLVIDA) | GPS do contribuinte individual por conta própria: dia 15 do mês seguinte à competência, prorrogado para o primeiro dia útil seguinte quando não houver expediente bancário | F-14 (art. 30, II), F-17, F-18, F-16 |

*Aritmética de conferência (não é fonte):* 20% × 1.621,00 = 324,20; 20% × 8.475,55 = 1.695,11.

### Plano simplificado

| Item | Valor / regra | Fonte |
|------|---------------|-------|
| Alíquota | 11% sobre o valor do salário mínimo vigente | F-13; F-11 |
| Valor em 2026 | R$ 178,31 | F-11 |
| Quem pode | "Contribuinte Individual: Trabalhador que atua por conta própria" e facultativo | F-13 |
| Restrição | "Trabalhador que atua por conta própria e não presta serviços a empresas" | F-13 |
| Consequência | "esse plano não contempla a aposentadoria por tempo de contribuição"; para contá-la é necessário complementar "com mais 9% sobre o valor do salário mínimo" | F-13 |
| Benefícios listados | aposentadoria por idade, auxílio-doença, aposentadoria por invalidez, pensão por morte, salário-maternidade, auxílio-reclusão | F-13 |
| Base legal citada na página | Lei Complementar nº 123/2006 e Decreto nº 6.042/2007 | F-13 |
| Vencimento | não especificado em F-13; mesma regra do plano normal (dia 15; ver Q-P4 RESOLVIDA) | F-14, F-16, F-17 |

*Aritmética de conferência (não é fonte):* 11% × 1.621,00 = 178,31.

### Limites 2026 (C)

Base normativa informada pelo INSS: **Portaria Interministerial MPS/MF nº 13, de 09/01/2026** (F-11; página atualizada em 13/01/2026):

- salário mínimo: **R$ 1.621,00**
- teto: **R$ 8.475,55**
- contribuição mínima (plano normal): **R$ 324,20**
- contribuição máxima (plano normal): **R$ 1.695,11**
- plano simplificado: **R$ 178,31**

A **Portaria foi lida** na versão do Diário Oficial da União (F-15): "Art. 2º O salário de benefício e o salário de contribuição, a partir de 1º de janeiro de 2026, não poderão ser inferiores a R$ 1.621,00 [...] nem superiores a R$ 8.475,55". Vigência: "Art. 12. Esta Portaria entra em vigor na data de sua publicação" (DOU 12/01/2026, edição 7, seção 1, página 58); valores aplicáveis "a partir de 1º de janeiro de 2026". Os valores de F-11 (INSS) coincidem com a Portaria. Os valores R$ 324,20, R$ 1.695,11 e R$ 178,31 são as contribuições da tabela do INSS (F-11); a Portaria não os traz (conferência aritmética: 20% e 11% dos limites).

### Dedutibilidade no IRPF (D)

**Sim, com condições.** A contribuição à Previdência Social "cujo ônus tenha sido do próprio contribuinte e desde que destinado a seu próprio benefício" é dedutível da base mensal do Carnê-Leão (F-07 pergunta 267 III; F-09 art. 4º IV; F-05). Aplica-se em alternativa ao desconto simplificado (F-09 art. 4º § 2º).
Complementação de 9% do plano simplificado: **FORA DO CÁLCULO DO MVP 1.0 / AVISO EDUCACIONAL** (Q-P3). O plano simplificado possui limitação previdenciária (sem aposentadoria por tempo de contribuição, F-13, F-14 art. 21 § 2º); eventual complementação **não será calculada** nesta primeira versão e aparece só como aviso educacional. A dedutibilidade da complementação não foi confirmada e não afeta o cálculo do MVP.

### Avisos educacionais

- O plano simplificado (11%) não dá direito à aposentadoria por tempo de contribuição, salvo complementação (F-13).
- O plano simplificado não se aplica a quem presta serviços a empresas (F-13); nesse caso a empresa recolhe (F-12).
- Os valores dependem do salário mínimo e do teto de 2026 (F-11) e mudam a cada ano.

### Decisão de produto (plano)

Ambos os planos são compatíveis com o cenário aprovado (autônomo, por conta própria, serviços a pessoas físicas, sem tomadores PJ):

- Opção A — Plano Normal (20%);
- Opção B — Plano Simplificado (11%).

**O sistema não escolhe.** O usuário deve **selecionar o plano**, com o aviso educacional acima. A condição de restrição (não prestar serviços a empresas) já é satisfeita pelo escopo aprovado; se o escopo for ampliado para tomadores PJ, o plano simplificado deixa de ser aplicável (F-13) e a regra precisa ser revista.

### Questões em aberto

| # | Questão | Situação |
|---|---------|----------|
| Q-P1 | Base do plano normal. | **RESOLVIDA** — Lei 8.212/1991, art. 28, III (F-14): remuneração mensal auferida pelo exercício da atividade por conta própria, observados os limites; ver "Base do salário de contribuição (Q-P1)". |
| Q-P2 | Texto integral da Portaria Interministerial MPS/MF nº 13/2026. | **RESOLVIDA** — Portaria lida na versão do DOU (F-15); art. 2º confirma R$ 1.621,00 e R$ 8.475,55 a partir de 1º/01/2026. |
| Q-P3 | Complementação de 9% do plano simplificado (dedutibilidade e cálculo). | **FORA DO CÁLCULO DO MVP 1.0 / AVISO EDUCACIONAL.** Não será calculada nesta versão. |
| Q-P4 | Vencimento da GPS. | **RESOLVIDA** — dia 15 do mês seguinte à competência (F-14 art. 30, II; F-16 Agenda Tributária 2026; F-17; F-18); prorrogação para o primeiro dia útil seguinte quando não houver expediente bancário consta nas páginas do INSS (F-17, F-18); a página da Agenda (F-16) não menciona a prorrogação. |
| Q-P5 | Datas das páginas do INSS: F-12 (19/10/2023), F-13 (28/01/2025), F-17 (17/10/2023) e F-18 (20/10/2023) são anteriores a 2026. | Registrada. Regras qualitativas coincidem com a Lei 8.212 (F-14); valores de 2026 vêm de F-11 e F-15. |
| Q-P6 | Tratamento quando a remuneração mensal está abaixo do limite mínimo. | **Aberta (decisão de produto).** Limite mínimo = salário mínimo vigente (F-18; F-14 art. 28 § 3º; F-15). Efeito no MVP a definir. |

### Fontes (TR-002)

F-11, F-12, F-13, F-14, F-15, F-16, F-17, F-18 (mais F-07, F-09, F-05 para a dedutibilidade).

---

## Casos de teste futuros

Somente **propostas**; nenhum código de teste foi escrito. Os valores esperados só valem depois de revisão independente (status **VALIDADA**).

### TR-001 — exemplos oficiais (F-02)

Fonte dos casos: página "Exemplos de Aplicação da Lei 15.270/2025" (22/12/2025, atualizada 04/03/2026). São exemplos de **salário/IRRF**; usam a mesma tabela, o mesmo desconto simplificado e a mesma redução. Uso para Carnê-Leão sujeito a Q-01.

| Caso | Rendimento | Dedução aplicada | Base | Imposto pela tabela | Redução | Imposto devido |
|------|-----------|------------------|------|---------------------|---------|----------------|
| TC-001 (João) | 3.036,00 | simplificado 607,20 | 2.428,00 | faixa isenta (0%) | — | 0,00 |
| TC-002 (José) | 4.000,00 | simplificado 607,20 | 3.392,80 | 3.392,80 × 15% − 394,16 = 114,76 | 114,76 | 0,00 |
| TC-003 (Maria) | 5.000,00 | simplificado 607,20 | 4.392,80 | 4.392,80 × 22,5% − 675,49 = 312,89 | até 312,89 (zera) | 0,00 |
| TC-004 (Rita) | 6.000,00 | dedução legal 649,60 (contribuição) | 5.350,40 | 5.350,40 × 27,5% − 908,73 = 562,63 | 978,62 − 0,133145 × 6.000,00 = 179,75 | 382,88 |
| TC-005 (Vera) | 7.607,20 | simplificado 607,20 | 7.000,00 | 7.000,00 × 27,5% − 908,73 = 1.016,27 | nenhuma (rendimento > 7.350,00) | 1.016,27 |

Todos os valores da tabela vêm de F-02. (Conferi a aritmética dos cinco exemplos: fecham.)

### TR-001 — exemplo de Carnê-Leão com desconto simplificado (F-07)

- Darf de **R$ 20,36**: `[(3.307,50 − 0,25 × 2.428,80) × 7,5%] − 182,16 = 20,36` (F-07, p. 114; cita IN RFB 1.500/2014, art. 52 § 3º e Anexo II).
- **Cautela:** é de um documento de ano-calendário 2025 e não inclui a redução de 2026. Usar apenas como referência de mecânica; recalcular contra as regras de 2026 antes de tornar caso de teste.

### TR-001 — casos a obter (sem valor oficial ainda)

Todos exigem exemplo oficial ou revisão independente antes de ter valor esperado:

- rendimento exatamente em cada limite de faixa (2.428,80 / 2.826,65 / 3.751,05 / 4.664,68);
- rendimento exatamente R$ 5.000,00 e R$ 5.000,01;
- rendimento exatamente R$ 7.350,00 e R$ 7.350,01;
- desconto simplificado *versus* dedução legal iguais;
- redução limitada ao imposto (§ 1º do art. 3º-A);
- rendimento zero ou abaixo do limite de isenção;
- casos de arredondamento (dependem de Q-02).

### TR-002 — valores do INSS (F-11)

| Caso | Entrada | Esperado (fonte F-11) |
|------|---------|----------------------|
| TC-101 | Plano simplificado, 2026 | contribuição R$ 178,31 |
| TC-102 | Plano normal, salário de contribuição = mínimo (R$ 1.621,00) | contribuição R$ 324,20 |
| TC-103 | Plano normal, salário de contribuição = teto (R$ 8.475,55) | contribuição R$ 1.695,11 |
| TC-104 | Plano normal, salário de contribuição acima do teto | limitado ao teto (a confirmar com fonte; F-14 art. 28 III "observado o limite máximo" e F-15 art. 2º) |

### Integração PF (TR-001 + TR-002)

Não há exemplo oficial que combine INSS e IRPF para autônomo em 2026. Casos combinados exigem revisão independente e exemplo oficial antes de virar teste. Em particular, deve-se cobrir: previdência deduzida × desconto simplificado (o mais benéfico).
