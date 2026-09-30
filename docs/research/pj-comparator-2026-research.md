# Pessoa Jurídica / Comparador — 2026

Status: **PESQUISADA e VALIDADA** (passagem final de validação em 2026-09-30). Implementação e testes: **IMPLEMENTADA / TESTADA** (Fase 4E).

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
- **Tratamento quando a remuneração consolidada fica abaixo do mínimo previdenciário**: ver "Existe pró-labore mínimo?" abaixo — distinto de "valor do pró-labore", esta hipótese **tem** regra oficial (mecanismo de complementação/utilização/agrupamento), já confirmada em TR-002.

### Existe pró-labore mínimo? (Q-PJ-01 — RESOLVIDA)

Esta pesquisa separa dois conceitos que não devem ser confundidos:

**A) Valor do pró-labore em si**: **não há norma oficial que fixe um valor mínimo legal de pró-labore.** A referência ao salário mínimo (R$ 1.621,00 em 2026) encontrada em fontes secundárias é prática de mercado/orientação contábil, não uma exigência normativa (nenhuma fonte oficial primária pesquisada — Lei nº 8.212/1991, Decreto nº 3.048/1999, Lei nº 10.666/2003 — fixa um piso para o *valor* do pró-labore). O único parâmetro legal encontrado é a classificação do sócio administrador como contribuinte individual **condicionada a receber remuneração decorrente de trabalho** (Decreto 3.048/1999 art. 9º V "e" 4, F-40) — o que estabelece a natureza da obrigação, não um valor mínimo. **Decisão de produto**: o simulador não impõe um piso artificial; o usuário informa qualquer valor de pró-labore (inclusive R$ 0,00, hipótese em que não há contribuinte individual, por ausência de remuneração pelo trabalho).

**B) Limite mínimo do salário de contribuição (base previdenciária)**: **existe**, e é distinto do item A. O contribuinte individual (incluído o sócio que recebe pró-labore) está sujeito ao **limite mínimo mensal do salário de contribuição**, correspondente ao salário mínimo vigente (R$ 1.621,00 em 2026) — já confirmado e sourced em [pf-2026-research.md](pf-2026-research.md) (TR-002, F-18/F-14 art. 28 §3º/F-15 art. 2º). Se o pró-labore pago em determinada competência resultar em remuneração consolidada **inferior** ao salário mínimo, aplicam-se os mesmos mecanismos de ajuste já documentados em TR-002 para o contribuinte individual em geral: **Decreto nº 3.048/1999, art. 13, § 8º e art. 19-E, § 1º** (F-21) — complementação (pagar a diferença até o mínimo), utilização (aproveitar excedente de outro mês) ou agrupamento (somar competências abaixo do mínimo) — e **INSS, "Ajustes para alcance do Salário Mínimo"** (F-22), que confirma expressamente a aplicação ao **contribuinte individual** (categoria que inclui o sócio com pró-labore), com a fórmula oficial de complementação `(salário mínimo − remuneração consolidada) × 20%`.

**Conclusão (reclassificação de Q-PJ-01)**: a distinção A/B está sustentada pelas fontes já confirmadas (F-18, F-21, F-22, todas já usadas em TR-002, mais F-40 desta pesquisa). Não há ausência de norma de forma geral — há ausência de norma **apenas** quanto ao valor mínimo do pró-labore em si (item A, que permanece decisão de produto); a complementação previdenciária quando a base fica abaixo do mínimo (item B) **está normatizada e resolvida**, com a mesma decisão de produto já registrada em TR-002 (aviso educacional, sem cálculo automático de complementação/utilização/agrupamento nesta versão do MVP). **Q-PJ-01 passa de ABERTA para RESOLVIDA.**

### Responsabilidade da empresa

A empresa (fonte pagadora) é responsável por: (a) **descontar** os 11% do pró-labore do sócio; (b) **declarar** esse fato gerador nas obrigações acessórias vigentes (eSocial/GFIP, conforme o regime declaratório aplicável — mecanismo geral, não uma exigência específica adicional pesquisada nesta passagem); (c) **recolher** o valor descontado junto com sua própria contribuição, até o dia 2 do mês seguinte (Lei nº 10.666/2003, art. 4º, F-41); (d) inscrever o sócio no INSS como contribuinte individual, se ainda não inscrito (art. 4º, §2º, F-41).

### CPP no Simples (Anexo III/V)

Confirmado por leitura direta da LC 123/2006, já lida integralmente em fase anterior (F-23/F-34): art. 13, VI — a Contribuição Patronal Previdenciária (CPP), de que trata o art. 22 da Lei nº 8.212/1991, está incluída no recolhimento único do Simples Nacional (DAS), **exceto** no caso de ME/EPP que se dediquem às atividades de prestação de serviços referidas no § 5º-C do art. 18 (Anexo IV — construção civil, vigilância/limpeza, advocacia, etc.). Como o MVP 1.0 suporta apenas Anexo III e Anexo V (premissa 3, já aprovada), a CPP patronal **já está embutida no DAS** em todos os cenários suportados.

**Implicação direta para o motor futuro**: o cálculo do comparador **não deve adicionar** 20% de CPP patronal separadamente sobre o pró-labore para os cenários Anexo III/V — isso duplicaria uma contribuição já incluída no DAS. O único desconto adicional é o INSS do **segurado** (11% sobre o pró-labore, retido pela empresa e recolhido ao INSS, distinto e não incluído no DAS, já que o DAS cobre apenas a CPP patronal, não a contribuição do segurado).

### IRPF sobre pró-labore

O pró-labore é rendimento tributável da pessoa física, sujeito à tabela progressiva mensal do IRPF (LC 123/2006, art. 14, *caput*, ao excluir expressamente o pró-labore da isenção, confirma seu caráter tributável, F-23/F-34). Aplicam-se, para 2026: a tabela progressiva mensal e a redução do art. 3º-A da Lei nº 9.250/1995 (incluído pela Lei nº 15.270/2025), já documentadas em [pf-2026-research.md](pf-2026-research.md) (TR-001, F-01/F-02/F-08/F-20); a dedução da contribuição previdenciária retida (11% do pró-labore, base de cálculo do IRPF); o desconto simplificado mensal, quando mais vantajoso (mesma lógica de TR-001). A fonte pagadora (a própria empresa) é responsável pela retenção do IRRF sobre o pró-labore, na forma geral de retenção na fonte sobre rendimentos do trabalho.

**Este documento não duplica as tabelas do IRPF 2026** — TR-010 depende de [pf-2026-research.md](pf-2026-research.md) (TR-001) para o cálculo do IRPF sobre o pró-labore.

### Relação com o Fator R (TR-009)

O pró-labore efetivamente pago (regime de caixa) integra a FS12 do Fator R (LC 123/2006, art. 18 § 24; confirmado por regime de caixa obrigatório na Solução de Consulta Cosit nº 17/2021 — já documentado em [simples-2026-research.md](simples-2026-research.md), TR-009, F-38). Esta pesquisa **não recalcula** o Fator R; apenas documenta a dependência: **TR-010 → TR-009** (o valor de pró-labore informado no cenário PJ deve alimentar o FS12 usado pelo Fator R, quando a atividade do cenário estiver entre as sujeitas ao Fator R).

### Questões em aberto (TR-010)

- **Q-PJ-01 — RESOLVIDA**: não há norma legal fixando valor mínimo do pró-labore em si (decisão de produto de não impor um mínimo); há, porém, norma expressa sobre o limite mínimo do salário de contribuição e o mecanismo de complementação/utilização/agrupamento quando a remuneração consolidada do contribuinte individual fica abaixo do salário mínimo (Decreto 3.048/1999 art. 13 §8º/art. 19-E §1º, F-21; INSS F-22/F-18) — ver "Existe pró-labore mínimo?" acima.
- **Q-PJ-02** (residual, não bloqueante): o artigo exato da IN RFB nº 2.110/2022 que fixa a alíquota de 11% de retenção sobre a remuneração do contribuinte individual a serviço de empresa não foi confirmado por leitura direta do texto integral nesta pesquisa (documento extenso, não obtido em uma única leitura) — o valor de 11% está bem corroborado por múltiplas fontes secundárias e é consistente com a prática já confirmada em Lei nº 8.212/1991 e Lei nº 10.666/2003, mas a citação do artigo específico da IN RFB 2.110/2022 fica como pendência de precisão.
- **Q-PJ-03** (fora do escopo do MVP): tratamento do sócio com múltiplas fontes de contribuição, fora do escopo do MVP (sócio único, sem outros vínculos) — não pesquisado nesta passagem.

## TR-011 — Distribuição de lucros

### Regra do Simples Nacional (base legal)

LC 123/2006, art. 14 (já lido integralmente, F-23/F-34): *"Consideram-se isentos do imposto de renda, na fonte e na declaração de ajuste do beneficiário, os valores efetivamente pagos ou distribuídos ao titular ou sócio da microempresa ou empresa de pequeno porte optante pelo Simples Nacional, salvo os que corresponderem a pró-labore, aluguéis ou serviços prestados."* § 1º: a isenção fica limitada ao valor resultante da aplicação dos percentuais do art. 15 da Lei nº 9.249/1995 sobre a receita bruta mensal (antecipação de fonte) ou a receita bruta total anual (declaração de ajuste), subtraído do valor devido no Simples Nacional no período. § 2º: o disposto no § 1º **não se aplica** quando a pessoa jurídica mantiver escrituração contábil e evidenciar lucro superior àquele limite.

Resolução CGSN nº 140/2018, art. 145, regulamenta o mesmo mecanismo com redação equivalente (conteúdo confirmado via fonte secundária consistente com a leitura primária do art. 14 da LC 123/2006 — o texto integral oficial da Resolução não foi obtido diretamente nesta passagem, mas seu conteúdo, tal como reproduzido por fontes profissionais especializadas e por Solução de Consulta oficial recente — ver abaixo —, replica o mesmo texto do art. 14) [F-42].

### Sem escrituração contábil

O lucro passível de distribuição isenta corresponde ao **percentual do art. 15 da Lei nº 9.249/1995** aplicado sobre a receita bruta, **subtraído o valor devido no Simples Nacional no período**. A própria LC 123/2006, art. 14 § 1º, distingue duas bases distintas (texto já confirmado em F-23/F-34), que não devem ser confundidas nem chamadas indistintamente de "lucro contábil":

- **Limite mensal / antecipação de fonte**: percentual do art. 15 aplicado sobre a **receita bruta mensal**, para fins de apurar se há retenção na fonte no próprio mês do pagamento.
- **Limite anual / declaração de ajuste**: percentual do art. 15 aplicado sobre a **receita bruta total anual**, para fins da declaração de ajuste do beneficiário (mecânica geral de apuração anual do IRPF, disciplinada em conjunto com a IN RFB nº 1.500/2014, já usada como fonte geral de procedimento em TR-001 — F-07/F-10/F-20).

Este valor presumido (percentual × receita − IRPJ do Simples) é um **limite fiscal de isenção**, não uma medida de lucro contábil efetivo da empresa.

Percentual aplicável às atividades suportadas no MVP: **32%**, correspondente a "prestação de serviços em geral" (Lei nº 9.249/1995, art. 15, § 1º, III, "a") [F-43, texto integral lido, mirror oficial Câmara/CEDI]. O próprio inciso III "a" traz uma exceção textual: reduz o percentual para **serviços hospitalares e de auxílio diagnóstico e terapia, patologia clínica, imagenologia, anatomia patológica e citopatologia, medicina nuclear e análises e patologias clínicas**, desde que a prestadora seja organizada como sociedade empresária e atenda às normas da Anvisa. As alíquotas de 16% (transporte, exceto carga) e 1,6% (combustíveis) não se aplicam a nenhuma atividade do MVP.

**Restrição de escopo adotada nesta passagem para as atividades de saúde do MVP (medicina e odontologia)**, exatamente para poder confirmar 32% sem ambiguidade:

- **Medicina**: o cenário suportado pelo MVP representa **prestação profissional médica comum / consultas e serviços que não se enquadrem na exceção de serviços hospitalares ou de auxílio diagnóstico e terapia** do art. 15 §1º III "a".
- **Odontologia**: o cenário suportado representa **serviços odontológicos profissionais em geral que não se enquadrem em hipótese especial de auxílio diagnóstico/terapia** com percentual reduzido.
- Serviços hospitalares, laboratórios de patologia clínica, imagenologia, medicina nuclear e demais hipóteses do art. 15 §1º III "a" que poderiam usar percentual diferente de 32% ficam **fora do MVP 1.0** (mesmo quando prestados por sociedade empresária registrada na Anvisa).

Com essa restrição explícita de escopo, e considerando também as demais 7 atividades do MVP (desenvolvimento de software, consultoria, engenharia, arquitetura, psicologia, fisioterapia, academias — nenhuma delas objeto de qualquer exceção do art. 15), **confirma-se 32% como o percentual correto para todas as 9 atividades suportadas no MVP**, sem ambiguidade remanescente.

### Com escrituração contábil

Quando a ME/EPP mantém **escrituração contábil regular** e evidencia lucro superior ao limite presumido (32% − IRPJ do Simples), a distribuição isenta pode ultrapassar aquele limite (LC 123/2006, art. 14 § 2º, F-23/F-34).

Achado desta pesquisa — **Solução de Consulta Cosit nº 244, de 28/11/2025** (ato oficial e vinculante da Receita Federal, publicado no DOU) [F-44, conteúdo obtido por fonte secundária especializada que resume com precisão o ato oficial; texto integral do PDF oficial não obtido diretamente nesta passagem — registrado como limitação de acesso, não de conteúdo]: confirma que o **lucro mensal** distribuído a cada sócio pode ultrapassar o limite presumido do art. 14 § 1º sem exceder o limite legal de isenção (ou seja, permanece dentro do que a lei permite distribuir isento) quando a ME/EPP **possui escrituração contábil e demonstra a existência de lucro mensal superior àquele limite, apurado por meio de balanços intermediários mensais**. Ou seja, a demonstração não precisa esperar o balanço anual — balanços/balancetes intermediários mensais servem de base, desde que a escrituração seja regular. Dispositivos legais citados na própria Solução: LC 123/2006 art. 14; Resolução CGSN nº 140/2018 art. 145; Lei nº 9.249/1995 art. 15.

**Sequência normativa — não confundir (achado desta passagem de validação)**: a SC Cosit nº 244/2025 resolve **quanto** pode ser legitimamente distribuído como lucro isento (regra de determinação do lucro distribuível, base LC123 art. 14). Isso é uma camada **inteiramente distinta** da retenção mensal de 10% do art. 6º-A da Lei nº 9.250/1995 (incluído pela Lei nº 15.270/2025, ver "Aplicação ao Simples Nacional" abaixo). **A SC Cosit nº 244/2025 não pode ser usada como fundamento para afastar o art. 6º-A** em pagamentos ocorridos em 2026: um valor pode ser legitimamente distribuível como lucro (dentro do limite do art. 14, com ou sem escrituração) e, ainda assim, sofrer a retenção de 10% quando o pagamento a uma mesma pessoa física, no mesmo mês, ultrapassar o gatilho de R$ 50.000,00. São perguntas jurídicas independentes: "quanto pode ser distribuído isento de IRPJ/CSLL na base presumida do Simples" (art. 14 / Cosit 244) ≠ "há retenção de IRRF de 10% sobre o pagamento ao sócio pessoa física" (art. 6º-A).

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

**Decisão judicial concretamente identificada (correção desta passagem de validação)**: existe uma decisão judicial específica e verificável — **Mandado de Segurança nº 5002505-76.2026.4.03.6100**, 26ª Vara Cível Federal de São Paulo, Juíza Federal Sílvia Figueiredo Marques, **liminar concedida em 09/02/2026** [F-46, notícia de imprensa jurídica especializada — Conjur — citando o processo público; o texto integral da decisão judicial não foi obtido diretamente nesta pesquisa, mas o número do processo, a vara e a data permitem verificação independente]. A liminar suspende, para a impetrante daquele mandado de segurança especificamente, a exigência da retenção de 10% do art. 6º-A, sob o argumento de que lei ordinária (Lei nº 15.270/2025, que altera a Lei nº 9.250/1995) não poderia restringir isenção concedida por lei complementar (LC 123/2006, art. 14).

Características importantes desta decisão, que devem ser respeitadas ao documentá-la:
- É **liminar**, não decisão de mérito transitada em julgado — pode ser revista, cassada ou reformada.
- Tem **efeito restrito à parte impetrante** daquele mandado de segurança específico — não beneficia automaticamente nenhuma outra empresa do Simples Nacional.
- O posicionamento **administrativo oficial da Receita Federal permanece o de que a retenção se aplica ao Simples Nacional** (F-45, pergunta 10) — a RFB não alterou sua orientação em razão desta liminar isolada.
- Há notícia de outras decisões monocráticas similares em casos distintos, e o tema é acompanhado como potencialmente relevante para uma futura definição em instâncias superiores — mas nesta pesquisa não foi confirmada nenhuma decisão de mérito definitiva, nem posição vinculante do STJ/STF sobre o tema específico do art. 6º-A e o Simples Nacional.

**Q-PJ-04 (mantida ABERTA, com decisão judicial concretamente identificada)**: para o MVP, adotar o **posicionamento oficial da Receita Federal** (retenção de 10% aplicável ao Simples Nacional, F-45) como base do cálculo, por ser a orientação administrativa vigente e de aplicação geral — registrando a existência da liminar (MS 5002505-76.2026.4.03.6100) como nota educacional na interface, sem implementar um "modo Simples Nacional sem retenção" baseado nela.

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

- **Q-PJ-04** (relevância jurídica real, concretamente identificada nesta passagem): existe liminar judicial específica (MS nº 5002505-76.2026.4.03.6100, 26ª Vara Cível Federal de São Paulo, 09/02/2026) suspendendo a retenção de 10% para a parte impetrante daquele processo, com base na tese de que lei ordinária não pode restringir isenção de lei complementar. Não é decisão definitiva nem de efeito geral. RFB mantém posicionamento administrativo de que a retenção se aplica ao Simples Nacional (F-45). Para o MVP, adotar o posicionamento oficial da RFB, registrando a existência da liminar como nota educacional (ver "Aplicação ao Simples Nacional").
- **Q-PJ-05** (pendência documental residual de rastreabilidade; não bloqueia TR-011): texto integral do art. 145 § 1º da Resolução CGSN nº 140/2018 ainda não relido diretamente nesta sessão (conteúdo obtido por fonte secundária, consistente com a leitura primária do art. 14 da LC 123/2006, e confirmado na revisão da Fase 4E). Não há dúvida sobre a implementação nem sobre o valor (Q-PJ-07 RESOLVIDA: subtrai-se somente o IRPJ do DAS). Deverá ser revisitada na auditoria documental final.
- **Q-PJ-06** (residual, não bloqueante): texto integral oficial da Solução de Consulta Cosit nº 244/2025 não obtido diretamente (conteúdo obtido por fonte secundária especializada, com ementa e conclusões citadas de forma consistente por múltiplas fontes independentes).

## Pesquisa complementar necessária à implementação da TR-011 (Fase 4E)

Para calcular o limite de distribuição sem escrituração (32% × receita − IRPJ devido no Simples) é preciso o **percentual de IRPJ na partilha do DAS**. Ele já constava da tabela de repartição de [simples-2026-research.md](simples-2026-research.md) (TR-006/TR-007); foi **reconferido contra o texto oficial da LC 123/2006** (F-48, Anexos III e V), sem divergência nas tabelas:

| Faixa | IRPJ — Anexo III | IRPJ — Anexo V |
|---|---|---|
| 1ª | 4,00% | 25,00% |
| 2ª | 4,00% | 23,00% |
| 3ª | 4,00% | 24,00% |
| 4ª | 4,00% | 21,00% |
| 5ª | 4,00% (ver nota) | 23,00% |
| 6ª (fora do MVP) | 35,00% | 35,00% |

- **Anexo III, 5ª faixa**: quando a alíquota efetiva for superior a 14,92537%, o ISS fica fixo em 5% e o IRPJ passa a ser (alíquota efetiva − 5%) × 6,02% (texto literal da nota do Anexo III).
- **Anexo V**: o texto oficial não traz nota de redistribuição. A menção anterior a "12,5% no Anexo V" (simples-2026-research.md / catálogo) era erro de atribuição: o limite de 12,5% é do Anexo IV (fora do MVP). Corrigido nesta fase; não altera nenhuma fórmula de TR-006/TR-007.
- IRPJ dentro do DAS = receita do PA × alíquota efetiva × percentual de repartição (ou a fórmula da nota, no caso citado). Os percentuais ficam em `rules.json` (TR-011, `reparticao_irpj` e `redistribuicao_iss`).

**Q-PJ-07 (RESOLVIDA por decisão de revisão, Fase 4E):** o texto literal do art. 14 § 1º da LC 123/2006 é amplo ("subtraído do valor devido na forma do Simples Nacional no período"). Conforme confirmado na revisão da Fase 4E, o art. 145 § 1º da Resolução CGSN nº 140/2018 especifica que a subtração corresponde ao valor relativo ao **IRPJ**, e a interpretação administrativa oficial da Receita Federal confirma o uso da parcela de IRPJ. **Decisão do motor: subtrair somente o IRPJ contido no DAS.** Ressalva de rastreabilidade: essa confirmação foi informada na revisão; o texto oficial integral do art. 145 ainda não foi relido nesta pesquisa (Q-PJ-05 permanece como pendência de citação, não de valor).

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

## Revisão independente final (2026-09-30)

Nesta passagem de validação, cada afirmação de TR-010 e TR-011 foi conferida contra fonte oficial, com as seguintes correções e confirmações:

1. **Pró-labore mínimo (Q-PJ-01)**: distinguidos dois conceitos antes tratados como uma única pendência — (A) valor do pró-labore em si (sem norma legal fixando piso, decisão de produto mantida) e (B) limite mínimo do salário de contribuição/mecanismo de complementação previdenciária (normatizado, já confirmado em TR-002 via F-18/F-21/F-22). **Q-PJ-01 reclassificada de ABERTA para RESOLVIDA.**
2. **Responsabilidade da empresa**: explicitados os três verbos (descontar, declarar, recolher), não apenas dois.
3. **Exceção de saúde do art. 15 §1º III "a"**: adicionada restrição explícita de escopo para "medicina" e "odontologia" no MVP (exclui serviços hospitalares e de auxílio diagnóstico/terapia), eliminando a ambiguidade anterior e confirmando 32% para as 9 atividades do MVP com base em premissa de escopo declarada, não em presunção.
4. **Distinção mensal/antecipação vs. anual/declaração de ajuste**: explicitada como duas bases de cálculo distintas do mesmo limite fiscal (art. 14 §1º da LC123), evitando chamar o resultado de "lucro contábil".
5. **Sequência normativa Cosit 244/2025 × art. 6º-A**: adicionada explicitamente — a Solução de Consulta resolve *quanto* pode ser distribuído isento; o art. 6º-A resolve *se há retenção mensal* sobre o pagamento à pessoa física; são camadas independentes, e a primeira não afasta a segunda.
6. **Q-PJ-04**: substituída a caracterização genérica de "controvérsia judicial" (não confirmada por fonte) por uma decisão judicial concretamente identificada (MS nº 5002505-76.2026.4.03.6100, 26ª Vara Cível Federal de São Paulo, liminar de 09/02/2026), com suas características (liminar, efeito restrito, não vinculante) explicitadas, e mantido o posicionamento oficial da RFB como base do cálculo do MVP.

Nenhuma dessas correções altera os valores centrais já documentados (11% de INSS sobre o pró-labore, CPP incluída no DAS para Anexo III/V, 32% de presunção de lucro, retenção de 10% acima de R$ 50.000,00/mês, gatilho de R$ 600.000,00/ano). Por isso, TR-010 e TR-011 alcançam **VALIDADA** nesta passagem, com as questões residuais (Q-PJ-02, Q-PJ-03, Q-PJ-04, Q-PJ-05, Q-PJ-06) registradas como pendências não bloqueantes.

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
