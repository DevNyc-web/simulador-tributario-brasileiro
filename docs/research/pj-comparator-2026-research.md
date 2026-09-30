# Pessoa Jurídica / Comparador — 2026

Status: **PESQUISADA**. Validação: **PENDENTE**. Implementação: **PENDENTE**. Testes: **PENDENTE**. Esta é a primeira passagem de pesquisa de TR-010 e TR-011 — não marcada como VALIDADA nesta etapa, por instrução explícita.

Segue a mesma metodologia de [pf-2026-research.md](pf-2026-research.md), [mei-2026-research.md](mei-2026-research.md) e [simples-2026-research.md](simples-2026-research.md): fonte oficial primária como citação final; fonte secundária só para descoberta; toda afirmação numérica ou de fórmula remete a um ID de fonte (F-XX) em [fontes-tributarias.md](fontes-tributarias.md).

## Escopo

O comparador PF x PJ do MVP **não** classifica qual regime é "melhor". Ele apresenta, lado a lado: tributos estimados, contribuições previdenciárias, líquido estimado, premissas assumidas e diferenças mensais/anuais — deixando a interpretação para o usuário (consistente com a premissa 8 já registrada em [calculation-assumptions.md](calculation-assumptions.md)).

Cenário PJ inicialmente suportado: pessoa jurídica optante pelo Simples Nacional; prestação de serviços tributada pelo Anexo III ou V; um único sócio, pessoa física residente no Brasil, que trabalha efetivamente na empresa; sem empregados; sócio sem participação em outra empresa; sem rendimentos no exterior; ano-calendário 2026.

## TR-010 — Pró-labore e contribuição previdenciária do sócio

### Natureza

O sócio que trabalha efetivamente na empresa tem dois tipos de remuneração possíveis, com naturezas jurídicas distintas: (a) **pró-labore** — remuneração pelo trabalho, base de incidência do INSS (contribuinte individual) e do IRPF; e (b) **distribuição de lucros** — remuneração do capital investido, isenta de IRPF nos termos e limites da LC 123/2006 art. 14 (ver TR-011), sem incidência de INSS. A lei exige que esses dois valores sejam discriminados.

### Contribuinte individual

Decreto nº 3.048/1999, art. 9º, V, "e", item 4 (Regulamento da Previdência Social): o sócio solidário, o sócio gerente, o sócio cotista e o administrador (quando não empregado) de sociedade limitada, urbana ou rural, são segurados obrigatórios na categoria de **contribuinte individual**, **"desde que receba remuneração decorrente de trabalho na empresa"** [F-40]. Ou seja, a obrigação de contribuir nasce especificamente da remuneração pelo trabalho — não da mera condição societária nem do recebimento de lucros.

### Pagamentos ao sócio sem discriminação entre pró-labore e lucro

A LC 123/2006, art. 14, *caput*, já confirmada como fonte primária em TR-011 (F-23/F-34), estabelece o princípio operacional relevante aqui: consideram-se isentos os valores pagos ou distribuídos ao sócio, **"salvo os que corresponderem a pró-labore, aluguéis ou serviços prestados"**. Isto é, a isenção de IRPF e a não incidência de INSS pressupõem que o valor pago seja identificável como retirada de lucro; um pagamento ao sócio que trabalha na empresa e que não seja discriminado como distribuição de lucro (com base de cálculo demonstrável, ver TR-011) não tem, por definição legal, amparo para ser tratado como lucro isento — devendo ser tratado como remuneração pelo trabalho (pró-labore), sujeita a INSS e IRPF. Esta pesquisa não localizou um dispositivo autônomo do Decreto nº 3.048/1999 que trate exaustivamente dessa hipótese de forma expressa e separada; a conclusão decorre da leitura combinada do art. 9º, V, "e" (F-40) com o art. 14 da LC 123/2006 (F-23/F-34). **Não presumido**: qualquer valor pago ao sócio que não seja documentalmente demonstrado como lucro (nos termos de TR-011) deve ser tratado, para fins deste MVP, como pró-labore.

### INSS sobre pró-labore

- **Responsabilidade pelo desconto e recolhimento**: a empresa é obrigada a descontar a contribuição do contribuinte individual a seu serviço da respectiva remuneração e a recolher o valor arrecadado junto com a contribuição a seu cargo até o dia dois do mês seguinte ao da competência (Lei nº 10.666/2003, art. 4º, *caput*, com efeitos desde 1º/4/2003) [F-41, texto integral lido]. Isso vale explicitamente para o sócio de pessoa jurídica que recebe pró-labore — a Lei nº 10.666/2003 é a norma que desloca a responsabilidade pelo desconto/recolhimento do próprio segurado para a empresa tomadora do serviço (diferente do cenário de TR-002, autônomo por conta própria sem relação de trabalho com empresa, que recolhe diretamente).
- **Alíquota**: 11% sobre a remuneração paga ao contribuinte individual a serviço de empresa (a alíquota de retenção pela empresa, distinta da alíquota "20% regra geral / 11% plano simplificado" de TR-002, que se aplica ao contribuinte individual que contribui por iniciativa própria, sem relação de trabalho com empresa) [confirmado por múltiplas fontes secundárias consistentes com a IN RFB nº 2.110/2022, arts. citados em torno do art. 33 — texto integral da IN não obtido diretamente nesta pesquisa devido à extensão do documento; registrado como pendência de confirmação de artigo exato, não de valor — ver Questões em aberto].
- **Base de cálculo**: o valor da remuneração paga a título de pró-labore, limitado ao teto do salário de contribuição.
- **Limites (já validados em TR-002 para 2026)**: mínimo R$ 1.621,00 (salário mínimo, Decreto nº 12.797/2025) e teto R$ 8.475,55 (Portaria Interministerial MPS/MF nº 13/2026) — ver [pf-2026-research.md](pf-2026-research.md), F-11/F-15. **Aplicação ao pró-labore confirmada nesta pesquisa**: o teto de R$ 8.475,55 limita a base de cálculo da contribuição descontada do sócio (o pró-labore pode ser de valor superior ao teto, mas a contribuição previdenciária só incide até o teto); não há, na legislação pesquisada, um "salário mínimo" como piso legal *obrigatório* de pró-labore em si (ver subseção seguinte) — o piso de R$ 1.621,00 é relevante apenas como referência de mercado/prática contábil, não como imposição legal do valor do pró-labore.
- **Tratamento quando o sócio possui outras fontes de contribuição**: fora do escopo do MVP (premissa: sócio único, sem outra empresa, sem outros vínculos) — não pesquisado nesta passagem.
- **Tratamento quando a remuneração fica abaixo do mínimo**: não localizada regra específica nesta pesquisa; registrada como questão em aberto (ver abaixo), já que depende de precisar se há ou não pró-labore mínimo obrigatório.

### Existe pró-labore mínimo?

**Não foi localizada norma oficial que fixe um valor mínimo legal de pró-labore.** A referência ao salário mínimo (R$ 1.621,00 em 2026) encontrada nesta pesquisa é prática de mercado/orientação contábil, não uma exigência normativa (múltiplas fontes secundárias convergem nesse sentido; nenhuma fonte oficial primária pesquisada — Lei nº 8.212/1991, Decreto nº 3.048/1999, Lei nº 10.666/2003 — fixa um piso). O único parâmetro legal encontrado é a classificação do sócio administrador como contribuinte individual **condicionada a receber remuneração decorrente de trabalho** (Decreto 3.048/1999 art. 9º V "e" 4, F-40) — o que estabelece a natureza da obrigação, não um valor mínimo.

**Marcado como QUESTÃO EM ABERTO / DECISÃO DE PRODUTO (Q-PJ-01)**: não criar um "pró-labore mínimo" no motor por costume contábil. O simulador deve permitir que o usuário informe qualquer valor de pró-labore (inclusive R$ 0,00, hipótese em que não há contribuinte individual por ausência de remuneração pelo trabalho, condição do art. 9º V "e" 4), sem impor um piso artificial.

### Responsabilidade da empresa

A empresa (fonte pagadora) é responsável por: (a) descontar os 11% do pró-labore do sócio; (b) recolher esse valor junto com sua própria contribuição, até o dia 2 do mês seguinte (Lei nº 10.666/2003, art. 4º, F-41); (c) inscrever o sócio no INSS como contribuinte individual, se ainda não inscrito (art. 4º, §2º, F-41).

### CPP no Simples (Anexo III/V)

Confirmado por leitura direta da LC 123/2006, já lida integralmente em fase anterior (F-23/F-34): art. 13, VI — a Contribuição Patronal Previdenciária (CPP), de que trata o art. 22 da Lei nº 8.212/1991, está incluída no recolhimento único do Simples Nacional (DAS), **exceto** no caso de ME/EPP que se dediquem às atividades de prestação de serviços referidas no § 5º-C do art. 18 (Anexo IV — construção civil, vigilância/limpeza, advocacia, etc.). Como o MVP 1.0 suporta apenas Anexo III e Anexo V (premissa 3, já aprovada), a CPP patronal **já está embutida no DAS** em todos os cenários suportados.

**Implicação direta para o motor futuro**: o cálculo do comparador **não deve adicionar** 20% de CPP patronal separadamente sobre o pró-labore para os cenários Anexo III/V — isso duplicaria uma contribuição já incluída no DAS. O único desconto adicional é o INSS do **segurado** (11% sobre o pró-labore, retido pela empresa e recolhido ao INSS, distinto e não incluído no DAS, já que o DAS cobre apenas a CPP patronal, não a contribuição do segurado).

### IRPF sobre pró-labore

O pró-labore é rendimento tributável da pessoa física, sujeito à tabela progressiva mensal do IRPF (LC 123/2006, art. 14, *caput*, ao excluir expressamente o pró-labore da isenção, confirma seu caráter tributável, F-23/F-34). Aplicam-se, para 2026: a tabela progressiva mensal e a redução do art. 3º-A da Lei nº 9.250/1995 (incluído pela Lei nº 15.270/2025), já documentadas em [pf-2026-research.md](pf-2026-research.md) (TR-001, F-01/F-02/F-08/F-20); a dedução da contribuição previdenciária retida (11% do pró-labore, base de cálculo do IRPF); o desconto simplificado mensal, quando mais vantajoso (mesma lógica de TR-001). A fonte pagadora (a própria empresa) é responsável pela retenção do IRRF sobre o pró-labore, na forma geral de retenção na fonte sobre rendimentos do trabalho.

**Este documento não duplica as tabelas do IRPF 2026** — TR-010 depende de [pf-2026-research.md](pf-2026-research.md) (TR-001) para o cálculo do IRPF sobre o pró-labore.

### Relação com o Fator R (TR-009)

O pró-labore efetivamente pago (regime de caixa) integra a FS12 do Fator R (LC 123/2006, art. 18 § 24; confirmado por regime de caixa obrigatório na Solução de Consulta Cosit nº 17/2021 — já documentado em [simples-2026-research.md](simples-2026-research.md), TR-009, F-38). Esta pesquisa **não recalcula** o Fator R; apenas documenta a dependência: **TR-010 → TR-009** (o valor de pró-labore informado no cenário PJ deve alimentar o FS12 usado pelo Fator R, quando a atividade do cenário estiver entre as sujeitas ao Fator R).

### Questões em aberto (TR-010)

- **Q-PJ-01**: não há norma oficial confirmando piso legal de pró-labore — decisão de produto de não impor um mínimo (ver acima).
- **Q-PJ-02**: o artigo exato da IN RFB nº 2.110/2022 que fixa a alíquota de 11% de retenção sobre a remuneração do contribuinte individual a serviço de empresa não foi confirmado por leitura direta do texto integral nesta pesquisa (documento extenso, não obtido em uma única leitura) — o valor de 11% está bem corroborado por múltiplas fontes secundárias e é consistente com a prática already confirmada em Lei nº 8.212/1991 e Lei nº 10.666/2003, mas a citação do artigo específico da IN RFB 2.110/2022 fica como pendência de precisão.
- **Q-PJ-03**: tratamento do sócio com múltiplas fontes de contribuição, ou remuneração abaixo do mínimo previdenciário, não pesquisado (fora do escopo do MVP nesta fase).

## TR-011 — Distribuição de lucros

### Regra do Simples Nacional (base legal)

LC 123/2006, art. 14 (já lido integralmente, F-23/F-34): *"Consideram-se isentos do imposto de renda, na fonte e na declaração de ajuste do beneficiário, os valores efetivamente pagos ou distribuídos ao titular ou sócio da microempresa ou empresa de pequeno porte optante pelo Simples Nacional, salvo os que corresponderem a pró-labore, aluguéis ou serviços prestados."* § 1º: a isenção fica limitada ao valor resultante da aplicação dos percentuais do art. 15 da Lei nº 9.249/1995 sobre a receita bruta mensal (antecipação de fonte) ou a receita bruta total anual (declaração de ajuste), subtraído do valor devido no Simples Nacional no período. § 2º: o disposto no § 1º **não se aplica** quando a pessoa jurídica mantiver escrituração contábil e evidenciar lucro superior àquele limite.

Resolução CGSN nº 140/2018, art. 145, regulamenta o mesmo mecanismo com redação equivalente (conteúdo confirmado via fonte secundária consistente com a leitura primária do art. 14 da LC 123/2006 — o texto integral oficial da Resolução não foi obtido diretamente nesta passagem, mas seu conteúdo, tal como reproduzido por fontes profissionais especializadas e por Solução de Consulta oficial recente — ver abaixo —, replica o mesmo texto do art. 14) [F-42].

### Sem escrituração contábil

O lucro passível de distribuição isenta corresponde ao **percentual do art. 15 da Lei nº 9.249/1995** aplicado sobre a receita bruta (mensal, para antecipação de fonte; total anual, para a declaração de ajuste), **subtraído o valor devido no Simples Nacional no período**.

Percentual aplicável às atividades suportadas no MVP: **32%**, correspondente a "prestação de serviços em geral" (Lei nº 9.249/1995, art. 15, § 1º, III, "a") [F-43, texto integral lido, mirror oficial Câmara/CEDI]. Confirmado, sem presumir: a exceção do próprio inciso III "a" (redução para serviços hospitalares e de diagnóstico específicos — patologia clínica, imagenologia, medicina nuclear, etc., exigindo organização como sociedade empresária registrada na Anvisa) **não se aplica** a nenhuma das 9 atividades suportadas no MVP (desenvolvimento de software, consultoria, engenharia, arquitetura, medicina "de consultório" comum, odontologia, psicologia, fisioterapia, academias) — nenhuma delas é serviço hospitalar/diagnóstico por imagem no sentido restrito da norma. As alíquotas de 16% (transporte, exceto carga) e 1,6% (combustíveis) também não se aplicam a nenhuma atividade do MVP. **Conclusão**: 32% é o percentual correto para todo o subconjunto de atividades do MVP.

### Com escrituração contábil

Quando a ME/EPP mantém **escrituração contábil regular** e evidencia lucro superior ao limite presumido (32% − IRPJ do Simples), a distribuição isenta pode ultrapassar aquele limite (LC 123/2006, art. 14 § 2º, F-23/F-34).

Achado desta pesquisa — **Solução de Consulta Cosit nº 244, de 28/11/2025** (ato oficial e vinculante da Receita Federal, publicado no DOU) [F-44, conteúdo obtido por fonte secundária especializada que resume com precisão o ato oficial; texto integral do PDF oficial não obtido diretamente nesta passagem — registrado como limitação de acesso, não de conteúdo]: confirma que o **lucro mensal** distribuído a cada sócio não sofre retenção mensal de IRRF quando a ME/EPP **possui escrituração contábil e demonstra a existência de lucro mensal superior ao limite do art. 14 § 1º, apurado por meio de balanços intermediários mensais**. Ou seja, a demonstração não precisa esperar o balanço anual — balanços/balancetes intermediários mensais servem de base, desde que a escrituração seja regular. Dispositivos legais citados na própria Solução: LC 123/2006 art. 14; Resolução CGSN nº 140/2018 art. 145; Lei nº 9.249/1995 art. 15.

### Não inventar lucro contábil

O simulador **não pode presumir** "lucro contábil = faturamento − DAS − pró-labore" sem base contábil suficiente — essa fórmula ignora custos, despesas operacionais, depreciação, capital de giro etc., e não corresponde a nenhuma norma pesquisada.

Duas alternativas identificadas para o escopo futuro do MVP (não decididas nesta pesquisa):

- **Opção A**: o usuário informa diretamente um "lucro contábil disponível para distribuição" e confirma que a empresa possui escrituração contábil regular (o simulador aceita o valor informado como dado de entrada, sem recalculá-lo). Vantagem: simples de implementar, reflete a realidade de quem já tem contabilidade. Limitação: depende inteiramente da informação do usuário, sem verificação; risco de uso incorreto por quem não entende a exigência de "escrituração regular + balanços intermediários" (Cosit 244/2025).
- **Opção B**: o simulador calcula **apenas o limite fiscal de distribuição sem escrituração contábil** (32% da receita − IRPJ do Simples), sem oferecer a opção de "lucro contábil maior". Vantagem: sempre calculável a partir dos dados já coletados (receita, DAS), sem exigir informação extra nem risco de mau uso. Limitação: subestima sistematicamente o valor distribuível de empresas que efetivamente têm contabilidade regular e lucro maior — não reflete a realidade de todas as PJs.

Nota: a própria Lei nº 15.270/2025 (art. 16-B § 6º, F-39) trouxe um terceiro conceito de "lucro contábil simplificado" — mas esse mecanismo serve a um propósito distinto (calcular o **redutor da tributação mínima anual de altas rendas** do art. 16-B, não o limite de distribuição isenta do art. 14 da LC123). Não deve ser confundido com o cálculo do limite de distribuição do Simples Nacional; é citado aqui apenas para registro, caso seja útil em fase futura de TR-011/TR-015+ relacionada à tributação mínima anual.

### Alterações da Lei nº 15.270/2025 — limite mensal de R$ 50 mil

LC 9.250/1995, art. 6º-A (incluído pela Lei nº 15.270/2025, texto integral lido, F-39): a partir de janeiro/2026, o pagamento, creditamento, emprego ou entrega de lucros/dividendos por uma mesma PJ a uma mesma PF residente no Brasil, em montante superior a R$ 50.000,00 em um mesmo mês, sujeita-se à retenção de **10% sobre o total do valor pago** (não apenas sobre o excedente). § 1º: vedada qualquer dedução da base. § 2º: múltiplos pagamentos no mesmo mês, pela mesma PJ à mesma PF, são somados e a retenção recalculada sobre o total mensal.

Casos confirmados por leitura literal do texto legal (F-39):
- R$ 50.000,00 exatos → **sem retenção** (o gatilho é "superior a", não "igual ou superior a").
- R$ 50.000,01 → retenção de 10% **sobre o total** (R$ 50.000,01), não apenas sobre o centavo excedente.
- Múltiplos pagamentos no mês pela mesma PJ à mesma PF → somados; a retenção é recalculada sobre o total mensal (§ 2º).

### Aplicação ao Simples Nacional

Confirmado pela Receita Federal em documento oficial "Perguntas e Respostas — Tributação de Altas Rendas — Considerações sobre Lucros e Dividendos" (16/12/2025, F-45, texto integral lido, 13 páginas), pergunta 10: **"Sim. A retenção na fonte prevista na lei também se aplica aos pagamentos de lucros e dividendos efetuados por empresas do Simples Nacional... Com a Lei nº 15.270/25, a isenção prevista no art. 14 da Lei Complementar nº 123/06 deixou de ser aplicada de modo que os lucros e dividendos pagos passarão a estar sujeitos a retenção na fonte do IRRF quando se tratar de pagamentos a uma mesma pessoa física residente no Brasil que supere R$ 50.000,00 em um mesmo mês."**

**Controvérsia jurídica identificada (registrar, não resolver)**: notícias de imprensa especializada (não confirmadas por fonte oficial nesta pesquisa) relatam decisão judicial de primeira instância (liminar) suspendendo a exigência da retenção de 10% para empresas do Simples Nacional, sob o argumento de que lei ordinária (Lei nº 15.270/2025, que altera a Lei nº 9.250/1995) não poderia restringir isenção concedida por lei complementar (LC 123/2006, art. 14). Trata-se de decisão não definitiva, de alcance restrito (sujeita a recurso), **não confirmada por fonte oficial primária nesta pesquisa** — registrada como Q-PJ-04 (questão em aberto de relevância jurídica real, distinta das pendências residuais de baixa relevância). O posicionamento administrativo oficial da Receita Federal (F-45) permanece o de que a retenção se aplica ao Simples Nacional.

### Regra dos R$ 50 mil — resumo de casos de fronteira

Ver "Casos de teste futuros" abaixo.

### Tributação anual de altas rendas (> R$ 600 mil)

Lei nº 9.250/1995, art. 16-A (incluído pela Lei nº 15.270/2025, texto integral lido, F-39): a partir do exercício de 2027 (ano-calendário 2026), pessoa física cuja soma de todos os rendimentos recebidos no ano-calendário for superior a R$ 600.000,00 sujeita-se à tributação mínima anual do IRPF.

- **Base de cálculo** (§ 1º): a soma de rendimentos recebidos no ano-calendário, inclusive tributados exclusivamente na fonte, isentos ou sujeitos a alíquota zero/reduzida, **deduzindo-se exclusivamente** (lista fechada de 12 incisos): ganhos de capital (exceto bolsa/balcão com apuração por ganho líquido); RRA tributados exclusivamente na fonte (sem opção por ajuste anual); doações em adiantamento de legítima/herança; poupança; diversos títulos isentos (LCI, CRI, LIG, LCD, CDA, WA, CDCA, LCA, CRA, CPR, FII/Fiagro com ≥100 cotistas); parcela isenta de atividade rural; indenizações por acidente/dano (exceto lucros cessantes); certos rendimentos isentos do art. 6º da Lei 7.713/1988; rendimentos de títulos isentos (exceto ações/participações societárias); e **lucros e dividendos relativos a resultados apurados até 2025, com distribuição aprovada até 31/12/2025 e pagos nos anos-calendário de 2026 a 2028 nos termos do ato de aprovação** (mesma regra de transição do art. 6º-A).
- **Fórmula de alíquota** (§ 2º): rendimentos ≥ R$ 1.200.000,00 → alíquota de 10%; rendimentos entre R$ 600.000,00 (exclusive) e R$ 1.200.000,00 (exclusive) → **Alíquota % = (REND / 60.000) − 10**.
- **Apuração do valor devido** (§ 3º): alíquota × base de cálculo, deduzidos: o IRPF da declaração de ajuste anual; o IRRF retido exclusivamente na fonte sobre os rendimentos incluídos na base; o IR apurado sob a Lei nº 14.754/2023 (offshore/fundos exclusivos); o IR pago definitivamente sobre rendimentos computados e não considerados nos itens anteriores; e o redutor do art. 16-B.
- **Redutor de dupla tributação** (art. 16-B): quando a soma da alíquota efetiva de tributação dos lucros da PJ com a alíquota efetiva da tributação mínima da PF ultrapassa a soma das alíquotas nominais de IRPJ+CSLL (34% regra geral; 40% para seguradoras/instituições específicas da LC105/2001 incisos II-X; 45% para bancos), concede-se um redutor, condicionado à apresentação de demonstrações financeiras da PJ (art. 16-B § 4º). O § 6º permite, para empresas não sujeitas ao lucro real, um "cálculo simplificado do lucro contábil" (faturamento menos folha de salários+encargos, custo de mercadoria/matéria-prima, aluguéis com IRRF retido, juros de financiamento institucional, depreciação de equipamentos) — mecanismo específico do redutor do art. 16-B, distinto do limite de distribuição isenta do art. 14 da LC123 (ver "Não inventar lucro contábil").

### Lucros anteriores a 2026

Regra de transição confirmada tanto na Lei nº 15.270/2025 (art. 6º-A § 3º e art. 16-A § 1º XII, F-39) quanto no Perguntas e Respostas oficial (F-45, perguntas 7-9): não se sujeitam à retenção de 10% nem à base da tributação mínima anual os lucros/dividendos (a) relativos a resultados apurados até o ano-calendário de 2025; (b) cuja distribuição tenha sido aprovada pelo órgão societário competente até 31/12/2025; e (c) cujo pagamento, crédito, emprego ou entrega ocorra nos anos-calendário de 2026 a 2028, nos termos originalmente previstos no ato de aprovação. O Perguntas e Respostas esclarece que essa aprovação pode se basear em balanço intermediário/balancete de verificação (ex.: janeiro a novembro de 2025), desde que formalizada até 31/12/2025 pelo órgão competente (assembleia-geral, no caso de S.A.; sócios, conforme o contrato social, em outras formas societárias).

**Premissa adotada para o MVP**: o comparador considera **somente lucro gerado no próprio ano-calendário de 2026**. Lucros acumulados de 2025 ou anteriores (e a mecânica de transição correspondente) ficam **fora do MVP 1.0**.

### EFD-Reinf

Informação operacional apenas (não implementar no motor): desde a IN RFB nº 2.096/2022 (evento R-4000), reforçada pela IN RFB nº 2.163/2023, a distribuição de lucros/dividendos deve ser informada na EFD-Reinf, ainda que isenta, com a natureza de rendimento "12001 – Lucro e dividendo" no evento R-4010, e um novo tipo de isenção "12" específico para essa distribuição, com vigência a partir de 01/01/2026 (substituindo o antigo tipo de isenção "5"/código "10001" a partir da apuração de maio/2026). Empresas do Simples Nacional também estão abrangidas por essa obrigação acessória. [Fontes secundárias especializadas consistentes entre si; texto oficial das INs não obtido diretamente nesta pesquisa — registrado como informação operacional, não como fonte de fórmula.]

### Limitações do comparador (nesta fase de pesquisa)

Sem cálculo de: tributação mínima anual de altas rendas (ver "Alternativas de escopo" abaixo); redutor do art. 16-B; capitalização de lucros; devolução de capital social; lucros de 2025 ou anteriores; múltiplas fontes de rendimento do sócio; distribuição via demonstrações financeiras consolidadas.

### Questões em aberto (TR-011)

- **Q-PJ-04** (relevância jurídica real, não apenas residual): controvérsia judicial sobre a aplicação da retenção de 10% (art. 6º-A) a empresas do Simples Nacional — RFB confirma administrativamente que se aplica (F-45); há notícia de decisão judicial de primeira instância em sentido contrário, não confirmada por fonte oficial nesta pesquisa. Para o MVP, adotar o posicionamento oficial da Receita Federal (retenção aplicável), registrando a controvérsia como nota educacional na interface.
- **Q-PJ-05**: artigo exato da Resolução CGSN nº 140/2018 (art. 145) não confirmado por leitura direta do texto oficial integral nesta passagem (conteúdo obtido por fonte secundária, consistente com a leitura primária do art. 14 da LC123/2006).
- **Q-PJ-06**: texto integral oficial da Solução de Consulta Cosit nº 244/2025 não obtido diretamente (conteúdo obtido por fonte secundária especializada, com ementa e conclusões citadas de forma consistente por múltiplas fontes independentes).

## Alternativas de escopo do comparador

Avaliação solicitada sobre a complexidade da tributação mínima anual de altas rendas (art. 16-A):

- **Opção 1 — implementar integralmente**: maior precisão para cenários de alta renda, mas exige base de cálculo com 12 exclusões específicas (§1º), redutor de dupla tributação com dependência de demonstrações financeiras da PJ (art. 16-B), e regras de transição — complexidade e risco de erro elevados para um MVP educacional.
- **Opção 2 — limitar o cálculo completo a cenários com soma anual relevante ≤ R$ 600.000,00**: simplicidade máxima e baixo risco de erro; deixa de fora, porém, justamente os cenários de "altas rendas" que motivaram a lei — perde parte do valor didático de mostrar o efeito da nova tributação mínima.
- **Opção 3 — calcular mensalmente (retenção de 10% sobre dividendos, IRPF sobre pró-labore) e, apenas quando a soma anual ultrapassar o gatilho de R$ 600.000,00, marcar o resultado anual como "cálculo anual de altas rendas não suportado integralmente pelo MVP"**: equilíbrio entre utilidade (cobre o cálculo mensal, que é a maior parte dos casos de uso educacional) e honestidade sobre a limitação (sinaliza claramente quando o resultado anual apresentado é incompleto), com complexidade de implementação moderada.

Recomendação preliminar (não decidida nesta pesquisa, apenas documentada para decisão futura): a Opção 3 parece a mais adequada ao escopo acadêmico do projeto — precisão no caso comum (mensal), honestidade explícita no caso raro/complexo (anual de altas rendas), sem exigir a implementação do redutor do art. 16-B (que depende de demonstrações financeiras da PJ, fora do escopo de um simulador educacional).

## Resultado futuro do comparador (conceitual, não é fórmula final)

```
PF:
  receita
  - INSS
  - IRPF
  = líquido estimado

PJ:
  faturamento
  - DAS
  - pró-labore (retirado da PJ, vira despesa da PJ / receita da PF)
  + pró-labore líquido recebido pela PF (pró-labore - INSS segurado - IRPF)
  + distribuição de lucros líquida (lucro distribuído - eventual IRRF do art. 6º-A)
  = líquido econômico estimado da PF
```

**Atenção — não transformado em fórmula final nesta pesquisa.** Antes de qualquer implementação, é preciso pesquisar como despesas empresariais reais, o próprio conceito de lucro contábil (ver "Não inventar lucro contábil"), necessidades de capital de giro e distribuição não realizada (lucro apurado mas não efetivamente pago ao sócio) afetam esse conceito. Não se afirma, nesta pesquisa, que todo saldo de caixa da empresa é lucro distribuível — pelo contrário, a "Opção A/B" acima existe justamente porque o comparador não pode presumir isso.

## Casos de teste futuros (propostos, não implementados)

**TR-010**:
- Pró-labore abaixo do limite de isenção do IRPF (ex.: R$ 2.428,80, valor de referência de TR-001).
- Pró-labore em cada faixa da tabela progressiva do IRPF 2026.
- Pró-labore igual ao teto previdenciário (R$ 8.475,55).
- Pró-labore acima do teto previdenciário (ex.: R$ 15.000,00 — confirmar que o desconto do segurado não excede o teto).
- Interação com a redução de IRPF da Lei nº 15.270/2025 (art. 3º-A).
- Pró-labore compondo o FS12 do Fator R (referenciar TR-009, não recalcular aqui).
- Pró-labore = R$ 0,00 (sem contribuinte individual, ausência de remuneração pelo trabalho).

**TR-011**:
- Distribuição de lucro = R$ 0,00.
- R$ 49.999,99 (sem retenção).
- R$ 50.000,00 (sem retenção — gatilho é "superior a").
- R$ 50.000,01 (retenção de 10% sobre o total).
- R$ 60.000,00 (retenção de 10% sobre o total).
- Múltiplos pagamentos no mesmo mês que juntos ultrapassem R$ 50.000,00 (recálculo sobre o total).
- Distribuição sem escrituração contábil (limite = 32% da receita − IRPJ do Simples).
- Distribuição com escrituração contábil regular e balanço intermediário mensal (Cosit 244/2025).
- Renda anual (para fins de art. 16-A) exatamente R$ 600.000,00 (sem tributação mínima).
- R$ 600.000,01 (tributação mínima com alíquota marginal próxima de 0%).
- R$ 1.200.000,00 (alíquota de 10%, teto da fórmula linear).
- Lucro relativo a resultado apurado até 2025, com distribuição aprovada até 31/12/2025 (fora do MVP, isento das novas regras).
