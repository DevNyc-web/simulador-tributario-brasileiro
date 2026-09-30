# MEI — 2026

Pesquisa de TR-003 (Limite anual e proporcional do MEI) e TR-004 (Composição e cálculo do DAS-MEI).
Data da consulta: **2026-09-29**. Status: **PESQUISADA** (não **VALIDADA**; validação segue PENDENTE — revisão independente ainda não realizada nesta primeira passagem).

> Todo número deste documento foi copiado de fonte oficial listada em "Fontes" (IDs `F-xx`) ou é marcado como *aritmética de conferência* (não é fonte).
> Nada aqui está implementado. Nenhum valor entrou em `data/tax_rules/`.

## Escopo do MVP

O módulo MEI 1.0 terá foco no **MEI comum**, com três categorias tributárias suportadas para fins de cálculo do DAS:

1. **Comércio / Indústria** — incidência de ICMS;
2. **Serviços** — incidência de ISS;
3. **Comércio e Serviços** — incidência de ICMS + ISS.

Essas três opções representam a **categoria tributária** usada para calcular o DAS (F-23, art. 18-A § 3º, incisos b e c — parcelas de ICMS e ISS condicionadas a "caso seja contribuinte do ICMS" / "caso seja contribuinte do ISS"). **Elas não substituem** a verificação de que a ocupação concreta do usuário está entre as ocupações permitidas do **Anexo XI da Resolução CGSN nº 140/2018** (F-26).

**Premissa registrada:** o MVP pressupõe que a ocupação informada pelo usuário seja uma ocupação permitida para MEI. O sistema deverá exibir **aviso educacional** de que a atividade concreta precisa constar da lista oficial de ocupações permitidas (Anexo XI, F-26) — o MVP não verifica isso automaticamente nesta primeira versão.

### Casos fora do MVP 1.0

Documentados explicitamente como fora do cálculo inicial:

- **MEI Caminhoneiro / Transportador Autônomo de Cargas** — regime especial existente (F-23, art. 18-F: limite anual R$ 251.600,00; limite proporcional R$ 20.966,67 × meses; contribuição previdenciária de 12% sobre o salário mínimo, correspondente a R$ 194,52 em 2026 — F-24), **mencionado mas não calculado** pelo MVP 1.0;
- atividades não constantes do Anexo XI;
- regras trabalhistas detalhadas do empregado do MEI (F-23, art. 18-C);
- parcelamentos;
- multas e juros por atraso;
- DAS em atraso;
- restituições;
- baixa do MEI;
- múltiplas atividades com situações especiais;
- obrigações estaduais/municipais específicas fora do DAS;
- cálculo de tributos após desenquadramento retroativo (o MVP documenta a regra, mas não recalcula os tributos devidos pelo regime geral do Simples Nacional após o desenquadramento).

---

## TR-003 — Limite anual e proporcional

### Limite anual

"Para os efeitos desta Lei Complementar, considera-se MEI quem tenha auferido receita bruta, no ano-calendário anterior, de até **R$ 81.000,00** (oitenta e um mil reais) [...]" (F-23, LC 123/2006, art. 18-A, § 1º).

Confirmado também pelo Portal do Empreendedor: "Atualmente, o limite de faturamento anual do Microempreendedor Individual (MEI) é de R$ 81 mil." (F-25).

### Ano de abertura / Limite proporcional

"No caso de início de atividades, o limite de que trata o § 1º será de **R$ 6.750,00** (seis mil, setecentos e cinquenta reais) multiplicados pelo número de meses compreendido entre o início da atividade e o final do respectivo ano-calendário, **consideradas as frações de meses como um mês inteiro**." (F-23, art. 18-A, § 2º).

Confirmado também pelo Portal do Empreendedor: "O limite de faturamento é calculado proporcionalmente ao número de meses de atividade, considerando-se a fração de mês como mês completo." e "[...] o valor proporcional corresponde a R$ 6.750 por mês de atividade." (F-25).

**Fórmula (documental, não implementada):**

```
limite_proporcional = 6.750,00 × número_de_meses
```

### Exemplos documentais (aritmética de conferência — não são exemplos oficiais)

| Início da atividade | Meses até 31/12 (fração = mês inteiro) | Limite proporcional |
|---|---|---|
| Janeiro | 12 | R$ 81.000,00 |
| Junho | 7 (jun a dez) | R$ 47.250,00 |
| Julho | 6 (jul a dez) | R$ 40.500,00 |
| Dezembro | 1 | R$ 6.750,00 |

*Aritmética de conferência (não é fonte):* 6.750,00 × 12 = 81.000,00; 6.750,00 × 7 = 47.250,00; 6.750,00 × 6 = 40.500,00; 6.750,00 × 1 = 6.750,00.

### Excesso de receita — regra dos 20%

Texto legal (F-23, LC 123/2006, art. 18-A, § 7º, incisos III e IV):

> "III - obrigatoriamente, quando o MEI exceder, no ano-calendário, o limite de receita bruta previsto no § 1º deste artigo, devendo a comunicação ser efetuada até o último dia útil do mês subsequente àquele em que ocorrido o excesso, produzindo efeitos:
> a) a partir de 1º de janeiro do ano-calendário subsequente ao da ocorrência do excesso, na hipótese de não ter ultrapassado o referido limite em mais de 20% (vinte por cento);
> b) retroativamente a 1º de janeiro do ano-calendário da ocorrência do excesso, na hipótese de ter ultrapassado o referido limite em mais de 20% (vinte por cento);
> IV - obrigatoriamente, quando o MEI exceder o limite de receita bruta previsto no § 2º deste artigo, devendo a comunicação ser efetuada até o último dia útil do mês subsequente àquele em que ocorrido o excesso, produzindo efeitos:
> a) a partir de 1º de janeiro do ano-calendário subsequente ao da ocorrência do excesso, na hipótese de não ter ultrapassado o referido limite em mais de 20% (vinte por cento);
> b) retroativamente ao início de atividade, na hipótese de ter ultrapassado o referido limite em mais de 20% (vinte por cento)."

Confirmação **(1) excesso não superior a 20% do limite (§1º — MEI já existente no início do ano):** efeitos a partir de 1º de janeiro do ano-calendário **subsequente** ao da ocorrência do excesso (inciso III, alínea a). Confirmado também pelo Portal do Empreendedor: "Você deve recolher um DAS complementar sobre o valor excedente e passará a pagar o imposto como Microempresa (ME) no ano seguinte." (F-25).

Confirmação **(2) excesso superior a 20% do limite (§1º — MEI já existente no início do ano):** efeitos **retroativos a 1º de janeiro do ano-calendário da ocorrência do excesso** — não à data de abertura, pois a empresa já existia no início do ano (inciso III, alínea b).

Confirmação **(3) excesso superior a 20% do limite proporcional (§2º — ano de início da atividade):** efeitos **retroativos ao início de atividade** (inciso IV, alínea b) — não a 1º de janeiro do ano-calendário, pois a empresa não existia antes de sua abertura.

**Complementação do DAS (excesso ≤ 20%):** "Nas hipóteses previstas nas alíneas *a* dos incisos III e IV do § 7º deste artigo, o MEI deverá recolher a diferença, **sem acréscimos**, em parcela única, juntamente com a da apuração do mês de janeiro do ano-calendário subsequente ao do excesso [...]" (F-23, art. 18-A, § 10).

Não presumido: a distinção entre os três cenários acima está sustentada literalmente pelos incisos III e IV do § 7º; não foi inferida.

### Cálculo de referência dos 20% (aritmética de conferência — não é fonte)

- Limite anual: R$ 81.000,00. Limite + 20%: R$ 81.000,00 × 1,20 = **R$ 97.200,00**.
- Para o ano de abertura: `limite_20 = limite_proporcional × 1,20` (ex.: início em julho, limite proporcional R$ 40.500,00 → limite + 20% = R$ 48.600,00).

**Q-MEI-01 (aberta):** o texto legal usa a redação "não ter ultrapassado o referido limite **em mais de** 20%" (F-23). Isso indica que um excesso **exatamente igual** a 20% (ex.: receita de exatamente R$ 97.200,00) ainda se enquadra em "não superior a 20%" — a norma não diz "20% ou mais", diz "mais de 20%". Esta leitura textual não foi confirmada por exemplo oficial numérico (Receita Federal ou CGSN); registrada como leitura do texto legal, não como fato validado por segunda fonte.

Estas fórmulas são **documentadas, não implementadas**.

### Condições básicas para ser MEI (elegibilidade — distinta de regra de cálculo)

Registradas como **validações de elegibilidade**, não como fórmula tributária:

| Condição | Fonte |
|---|---|
| Ocupação deve estar entre as permitidas no **Anexo XI da Resolução CGSN nº 140/2018** | F-26 |
| Não pode ser titular, sócio ou administrador de outra empresa | F-23 (art. 18-A, § 4º, III); F-26 (art. 100) |
| Não pode possuir filial (só um estabelecimento) | F-23 (art. 18-A, § 4º, II); F-26 (art. 100) |
| Atividade não pode ser tributada pelos Anexos V ou VI do Simples Nacional, salvo autorização isolada do CGSN | F-23 (art. 18-A, § 4º, I) |
| Não pode ser constituído como startup | F-23 (art. 18-A, § 4º, V) |
| Máximo de um empregado | F-23 (art. 18-C, caput); F-26 (art. 100) |
| O empregado do MEI deve receber exclusivamente um salário mínimo ou o piso salarial da categoria profissional | F-23 (art. 18-C, caput) |
| Demais requisitos previstos no art. 100 da Resolução CGSN nº 140/2018 | F-26 (não obtido texto integral verbatim — ver Q-MEI-02) |

**Distinção explícita:** as condições acima são **regras de elegibilidade** (permitem ou não o enquadramento como MEI) e não fazem parte da **regra de cálculo** do DAS (TR-004). O MVP não terá, nesta fase, um sistema completo de validação societária — apenas o registro das condições e avisos educacionais.

### Questões em aberto (TR-003)

| # | Questão | Situação |
|---|---------|----------|
| Q-MEI-01 | Excesso exatamente igual a 20% do limite (anual ou proporcional): a redação legal usa "em mais de 20%", o que sugere que exatamente 20% ainda conta como "não superior a 20%". | Aberta. Leitura textual do art. 18-A § 7º (F-23); sem exemplo oficial numérico que confirme o caso-limite. |
| Q-MEI-02 | Texto integral do art. 100 da Resolução CGSN nº 140/2018 (condições de elegibilidade do MEI). | Aberta. Conteúdo obtido apenas via fonte secundária (F-26, LegisWeb) para descoberta; o portal `normas.receita.fazenda.gov.br` e o portal `in.gov.br` não entregaram o texto navegável nesta pesquisa (mesma limitação técnica já registrada para F-10 em TR-001). |
| Q-MEI-03 | Conteúdo integral do Anexo XI da Resolução CGSN nº 140/2018 (lista de ocupações permitidas). | Aberta. O PDF oficial foi localizado em `www8.receita.fazenda.gov.br` (F-26), 43 páginas, mas seu conteúdo não pôde ser extraído pela ferramenta usada nesta pesquisa (arquivo binário/comprimido). A existência e a URL oficial do documento estão confirmadas; o conteúdo linha a linha não foi lido. |
| Q-MEI-04 | Reingresso do MEI e possível parcelamento de débitos do excesso retroativo (>20%). | Fora do escopo desta pesquisa; ver "Casos fora do MVP 1.0". |

### Fontes (TR-003)

F-23, F-25, F-26, F-27 — ver [fontes-tributarias.md](fontes-tributarias.md).

---

## TR-004 — DAS-MEI

### Estrutura do SIMEI

"O Microempreendedor Individual - MEI poderá optar pelo recolhimento dos impostos e contribuições abrangidos pelo Simples Nacional em **valores fixos mensais, independentemente da receita bruta por ele auferida no mês**, na forma prevista neste artigo." (F-23, LC 123/2006, art. 18-A, caput).

"[...] o MEI, com receita bruta anual igual ou inferior a R$ 81.000,00 (oitenta e um mil reais), recolherá, na forma regulamentada pelo Comitê Gestor, valor fixo mensal correspondente à soma das seguintes parcelas [...]" (F-23, art. 18-A, § 3º, V).

O texto literal da Lei Complementar 123/2006 (art. 18-A, § 3º, V, alínea *a*) traz o valor histórico de **R$ 45,65** para a parcela previdenciária — valor desatualizado no próprio texto da lei, que **não é o valor vigente em 2026**. O § 11 do mesmo artigo determina: "O valor referido na alínea *a* do inciso V do § 3º deste artigo será reajustado, na forma prevista em lei ordinária, na mesma data de reajustamento dos benefícios de que trata a Lei nº 8.213, de 24 de julho de 1991, **de forma a manter equivalência com a contribuição** de que trata o § 2º do art. 21 da Lei nº 8.212, de 24 de julho de 1991." (F-23). Ou seja, a lei complementar fixa o **mecanismo de reajuste**, mas o **valor vigente em cada ano** é divulgado administrativamente pela Receita Federal/INSS, não pelo texto literal (desatualizado) da LC 123/2006. Os valores de 2026 usados neste documento vêm da fonte oficial de valores vigentes (F-24), não do texto literal da lei.

### Previdência

Valor oficial de 2026, conforme Receita Federal / Portal do Simples Nacional (F-24, notícia "MEI - atualização de valores devidos em 2026", publicada 02/01/2026):

> "R$ 81,05 de INSS (5% do valor do salário-mínimo, de R$ 1.621,00)"

- Alíquota: **5% do salário mínimo** (não os 20%/11% do contribuinte individual comum de TR-002 — regime distinto e específico do MEI).
- Salário mínimo de 2026: **R$ 1.621,00** (F-27, Decreto nº 12.797, de 23/12/2025, art. 1º: "A partir de 1º de janeiro de 2026, o valor do salário mínimo será de R$ 1.621,00"; mesmo valor confirmado por F-15/F-11 em TR-002, para fins previdenciários).
- Contribuição: **R$ 81,05**.

*Aritmética de conferência (não é fonte):* 5% × 1.621,00 = 81,05.

### ICMS

"R$ 1,00 (um real), a título do imposto referido no inciso VII do caput do art. 13 desta Lei Complementar, caso seja contribuinte do ICMS" (F-23, art. 18-A, § 3º, V, alínea *b*). Confirmado para 2026 por F-24: "[...] e R$ 1,00 de ICMS".

### ISS

"R$ 5,00 (cinco reais), a título do imposto referido no inciso VIII do caput do art. 13 desta Lei Complementar, caso seja contribuinte do ISS" (F-23, art. 18-A, § 3º, V, alínea *c*). Confirmado para 2026 por F-24: "R$ 5,00 de ISS, caso seja contribuinte deste imposto".

### Valores de 2026

| Categoria | Composição | Total |
|---|---|---|
| Comércio / Indústria | 81,05 (INSS) + 1,00 (ICMS) | **R$ 82,05** |
| Serviços | 81,05 (INSS) + 5,00 (ISS) | **R$ 86,05** |
| Comércio e Serviços | 81,05 (INSS) + 1,00 (ICMS) + 5,00 (ISS) | **R$ 87,05** |

*Aritmética de conferência (não é fonte):* 81,05 + 1,00 = 82,05; 81,05 + 5,00 = 86,05; 81,05 + 1,00 + 5,00 = 87,05. A fonte oficial (F-24) confirma os três componentes individuais (81,05 / 1,00 / 5,00) e, separadamente, cita os totais de R$ 82,05 / R$ 86,05 / R$ 87,05 em páginas complementares de imprensa oficial (F-24, notícias relacionadas) e em múltiplas fontes contábeis independentes que reproduzem a mesma soma sem divergência.

### Vencimento

"O DAS é devido até o dia 20 de cada mês" — vencimento do DAS-MEI: **dia 20 do mês subsequente** à competência (F-26, Resolução CGSN nº 140/2018, art. 104, citado via fonte secundária de descoberta). Quando o dia 20 recai em final de semana ou feriado, o vencimento é **prorrogado para o próximo dia útil** (F-26). Informação educacional; não faz parte do valor calculado inicialmente.

**Ressalva de fonte:** o número exato do artigo (art. 104) e a redação verbatim não foram confirmados diretamente no portal oficial `normas.receita.fazenda.gov.br` (mesma limitação técnica de Q-04/F-10 em TR-001) nem em `in.gov.br` (falha de conexão nesta pesquisa). A regra do dia 20 e a prorrogação para dia útil são corroboradas por múltiplas fontes secundárias convergentes (LegisWeb, páginas contábeis, Agência Sebrae) sem divergência entre si — suficiente para status **PESQUISADA**, mas o texto literal do artigo permanece pendência de confirmação para VALIDADA (Q-MEI-02).

### Relação entre faturamento e DAS

Confirmado: **o SIMEI utiliza valores fixos mensais** e o DAS **não varia proporcionalmente com o faturamento mensal**, desde que o contribuinte permaneça enquadrado nas condições do MEI (F-23, art. 18-A, caput: "valores fixos mensais, **independentemente da receita bruta** por ele auferida no mês"; F-26, art. 104).

**Consequência para o motor futuro (documentada, não implementada):** o **faturamento mensal não é multiplicado por alíquota** do DAS-MEI. O faturamento será utilizado principalmente para:

- acompanhar o limite anual/proporcional (TR-003);
- emitir alertas de proximidade ou excesso do limite;
- identificar incompatibilidade/excesso de enquadramento.

### Casos fora do MVP

Ver "Casos fora do MVP 1.0" na seção de escopo, acima. Em particular: MEI Caminhoneiro (regime especial, alíquota de 12% do salário mínimo — R$ 194,52 em 2026, F-24/F-23 art. 18-F — mencionado, não calculado).

### Questões em aberto (TR-004)

| # | Questão | Situação |
|---|---------|----------|
| Q-MEI-05 | Texto integral do art. 104 da Resolução CGSN nº 140/2018 (vencimento do DAS-MEI). | Aberta. Mesma limitação de Q-MEI-02: conteúdo obtido só via fonte secundária de descoberta (F-26). |
| Q-MEI-06 | Somatório oficial explícito dos totais por categoria (R$ 82,05 / R$ 86,05 / R$ 87,05) em página única da Receita Federal, em vez de conferência aritmética a partir dos três componentes. | Registrada, baixa prioridade — os três componentes individuais estão confirmados na fonte oficial (F-24); os totais coincidem em todas as fontes secundárias consultadas, sem divergência. |
| Q-MEI-07 | Receita mensal zero com MEI ativo: o DAS fixo continua devido? | Aberta. Decorre diretamente da regra "valores fixos mensais, independentemente da receita bruta" (F-23, art. 18-A caput), que não distingue receita zero de receita positiva — mas nenhuma fonte oficial consultada trata explicitamente do caso de receita zero. Ver TC-MEI-104 abaixo. |

### Fontes (TR-004)

F-23, F-24, F-26, F-27 — ver [fontes-tributarias.md](fontes-tributarias.md).

---

## Casos de teste futuros

Somente **propostas**; nenhum código de teste foi escrito. Os valores esperados só valem depois de revisão independente (status **VALIDADA**).

### TR-003 — limite anual e proporcional

| Caso | Entrada | Situação esperada (a confirmar em validação) |
|------|---------|----------------------------------------------|
| TC-MEI-001 | Receita anual R$ 70.000,00 (MEI o ano todo) | Dentro do limite anual (R$ 81.000,00) |
| TC-MEI-002 | Receita anual exatamente R$ 81.000,00 | No limite (não excedido) |
| TC-MEI-003 | Receita anual R$ 81.000,01 | Excedido; dentro da faixa "não superior a 20%" (Q-MEI-01 para o caso-limite) |
| TC-MEI-004 | Receita anual exatamente R$ 97.200,00 (81.000 × 1,20) | Ver Q-MEI-01: pela redação "em mais de 20%", ainda não seria "superior a 20%" |
| TC-MEI-005 | Receita anual R$ 97.200,01 | Excesso superior a 20%; efeitos retroativos a 1º de janeiro do ano do excesso (empresa já existente) |
| TC-MEI-006 | Abertura em julho (6 meses), limite proporcional R$ 40.500,00 | Regra proporcional |
| TC-MEI-007 | Abertura em dezembro (1 mês), limite proporcional R$ 6.750,00 | Regra proporcional, fração de mês = mês completo |

### TR-004 — DAS-MEI

| Caso | Entrada | Esperado (fonte F-24, sujeito a validação) |
|------|---------|---------------------------------------------|
| TC-MEI-101 | DAS Comércio/Indústria, 2026 | R$ 82,05 |
| TC-MEI-102 | DAS Serviços, 2026 | R$ 86,05 |
| TC-MEI-103 | DAS Comércio e Serviços, 2026 | R$ 87,05 |
| TC-MEI-104 | Receita mensal zero, MEI ativo | A pesquisar antes de implementar: DAS fixo permanece devido (decorre do texto legal, Q-MEI-07), mas nenhum exemplo oficial trata explicitamente do caso |

### Integração MEI (TR-003 + TR-004)

Não há exemplo oficial numérico que combine, em um único caso, o valor do DAS com uma situação de excesso de receita (complementação do § 10 do art. 18-A). Casos combinados exigem revisão independente e, se possível, exemplo oficial antes de virarem teste.
