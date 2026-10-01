# MEI — 2026

Pesquisa de TR-003 (Limite anual e proporcional do MEI) e TR-004 (Composição e cálculo do DAS-MEI).
Data da consulta: **2026-09-29** (primeira pesquisa) e **2026-09-29** (passagem final de validação). Status: **PESQUISADA** e **VALIDADA** (revisão independente concluída nesta passagem; ver "Revisão independente final"). Pendências residuais que não bloqueiam a validação: o número exato do artigo da Resolução CGSN nº 140/2018 que regula o vencimento do DAS-MEI (Q-MEI-05, parcial) e o conteúdo linha a linha do Anexo XI (Q-MEI-03, parcial — a lista completa de ocupações não é necessária para a regra de cálculo, apenas para a futura verificação automática de elegibilidade, já fora de escopo do MVP).

> Todo número deste documento foi copiado de fonte oficial listada em "Fontes" (IDs `F-xx`) ou é marcado como *aritmética de conferência* (não é fonte).
> Nada aqui está implementado. Nenhum valor entrou em `data/tax_rules/`.
> **Status posterior (MVP final):** os valores desta pesquisa foram implementados e testados (`TR-001` a `TR-011`; ver `tax-rule-matrix.md`) e constam em `data/tax_rules/2026/rules.json`. As frases abaixo sobre implementação pendente descrevem a fase de pesquisa.

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

- Limite anual: R$ 81.000,00. 20% do limite: R$ 81.000,00 × 0,20 = **R$ 16.200,00**. Limite + 20%: R$ 81.000,00 + R$ 16.200,00 = **R$ 97.200,00**.
- Para o ano de abertura: `limite_20 = limite_proporcional × 1,20` (ex.: início em julho, limite proporcional R$ 40.500,00 → limite + 20% = R$ 48.600,00).

**Q-MEI-01 (RESOLVIDA):** o texto legal usa, em quatro ocorrências (art. 18-A, § 7º, incisos III e IV, alíneas *a* e *b*), a redação "não ter ultrapassado o referido limite **em mais de** 20%" / "ter ultrapassado o referido limite **em mais de** 20%" (F-23). A mesma redação é repetida, verbatim, no material oficial "Perguntas e Respostas MEI e Simei" (F-31, perguntas 6.4 e 6.8), o que confirma que a leitura não é uma inferência isolada do texto da lei, mas a própria formulação usada pela administração tributária. Consequência numérica, para o limite anual (R$ 81.000,00, MEI já existente no início do ano):

| Receita anual | Excesso sobre R$ 81.000,00 | Enquadramento |
|---|---|---|
| até R$ 81.000,00 | — | dentro do limite |
| de R$ 81.000,01 até **R$ 97.200,00** | até 20% | **NÃO superior a 20%** — efeitos a partir de 1º/jan do ano-calendário subsequente |
| a partir de **R$ 97.200,01** | mais de 20% | **superior a 20%** — efeitos retroativos a 1º/jan do ano-calendário do excesso |

Ou seja: uma receita de **exatamente R$ 97.200,00** ainda se enquadra em "não superior a 20%" (o excesso é de exatamente 20%, não "mais de" 20%); só a partir de **R$ 97.200,01** o excesso passa a ser "superior a 20%". A mesma lógica se aplica, proporcionalmente, ao limite do ano de abertura (§ 2º combinado com o § 7º, IV).

Estas fórmulas são **documentadas, não implementadas**.

### Condições básicas para ser MEI (elegibilidade — distinta de regra de cálculo)

Registradas como **validações de elegibilidade**, não como fórmula tributária. Confirmadas, cumulativamente, pelo material oficial "Perguntas e Respostas MEI e Simei" (F-31, Secretaria-Executiva do CGSN, atualizado 29/04/2025, Pergunta 1.2 — "Base legal: art. 18-A da Lei Complementar nº 123, de 2006"), que reproduz e detalha as condições já confirmadas em texto legal (F-23) e na página oficial "Verifique se você atende as condições para ser MEI" (F-28, que cita "Arts. 100, Inciso I e 101" da Resolução CGSN nº 140/2018):

| Condição | Fonte |
|---|---|
| Exercer ocupação entre as permitidas no **Anexo XI da Resolução CGSN nº 140/2018** (ou atividades de comercialização/processamento extrativista, ou industrialização/comercialização/prestação de serviços no âmbito rural) | F-23 (art. 18-A, § 1º, incisos I a III); F-28 (Anexo XI, arts. 100 I e 101); F-31 (Pergunta 1.2) |
| Auferir receita bruta dentro do limite anual (R$ 81.000,00) ou proporcional | F-23 (art. 18-A, §§ 1º e 2º); F-31 (Pergunta 1.2) |
| Possuir um único estabelecimento (sem filial) | F-23 (art. 18-A, § 4º, II); F-28; F-31 (Pergunta 1.2) |
| Não participar de outra empresa como titular, sócio ou administrador | F-23 (art. 18-A, § 4º, III); F-28; F-31 (Pergunta 1.2) |
| Não ser constituído na forma de startup | F-23 (art. 18-A, § 4º, V); F-31 (Pergunta 1.2) |
| Atividade não pode ser tributada pelos Anexos V ou VI do Simples Nacional, salvo autorização isolada do CGSN | F-23 (art. 18-A, § 4º, I) |
| Máximo de um empregado, que só pode receber 1 salário mínimo (federal ou estadual) ou o piso salarial da categoria | F-23 (art. 18-C, caput); F-31 (Pergunta 1.2, citando art. 18-C da LC 123/2006) |
| Não guardar, cumulativamente, com o contratante do serviço, relação de pessoalidade, subordinação e habitualidade | F-31 (Pergunta 1.2) |
| Não realizar suas atividades mediante cessão ou locação de mão de obra | F-31 (Pergunta 1.2, citando art. 112, caput, da Resolução CGSN nº 140/2018) |
| Não pode ser Eireli nem qualquer tipo de sociedade — só empresário individual (art. 966 do Código Civil) | F-31 (Pergunta 1.2, nota 1 e 2, citando art. 18-A § 1º da LC 123/2006) |
| Não pode ser salão-parceiro da Lei nº 12.592/2012 | F-31 (Pergunta 1.2, nota 3, citando art. 100, § 7º, da Resolução CGSN nº 140/2018) |

**Uso na simulação guiada (Fase 5C.1).** A regra do empregado do MEI (máximo de **um** empregado, remunerado com **um salário mínimo ou o piso salarial da categoria** — F-23 art. 18-C; F-28, Portal Empresas & Negócios/gov.br; F-31 Pergunta 1.2) consta em TR-003 apenas como o parâmetro de quantidade `maximo_empregados` ("1") e como o descritor semântico `regra_remuneracao_empregado` ("salario_minimo_ou_piso_da_categoria"). Não há limite numérico de salário no `rules.json`: a simulação guiada adota 1 salário mínimo como **hipótese do cenário**, distinta da regra legal.

**Distinção explícita:** as condições acima são **regras de elegibilidade** (permitem ou não o enquadramento como MEI) e não fazem parte da **regra de cálculo** do DAS (TR-004). O MVP não terá, nesta fase, um sistema completo de validação societária — apenas o registro das condições e avisos educacionais.

### Questões em aberto (TR-003)

| # | Questão | Situação |
|---|---------|----------|
| Q-MEI-01 | Excesso exatamente igual a 20% do limite (anual ou proporcional): a redação legal usa "em mais de 20%", o que sugere que exatamente 20% ainda conta como "não superior a 20%". | **RESOLVIDA** — confirmado pelo texto legal (F-23, art. 18-A § 7º) e pelo material oficial "Perguntas e Respostas MEI e Simei" (F-31, perguntas 6.4 e 6.8), que repete a mesma redação. Exatamente R$ 97.200,00 (81.000 + 20%) ainda é "não superior a 20%"; a partir de R$ 97.200,01 o excesso é "superior a 20%". Ver seção "Cálculo de referência dos 20%" acima. |
| Q-MEI-02 | Texto integral do art. 100 da Resolução CGSN nº 140/2018 (condições de elegibilidade do MEI). | **RESOLVIDA** — confirmado por duas fontes oficiais primárias: a página "Verifique se você atende as condições para ser MEI" do Portal Empresas & Negócios (F-28, que cita explicitamente "Arts. 100, Inciso I e 101") e o material "Perguntas e Respostas MEI e Simei" da Secretaria-Executiva do CGSN (F-31, Pergunta 1.2, que lista as condições cumulativas com base legal e cita também art. 100 §§ 1º e 7º e art. 112). O portal `normas.receita.fazenda.gov.br` continua sem entregar o texto navegável do artigo isolado (mesma limitação de F-10), mas o conteúdo do artigo está confirmado por essas duas fontes primárias convergentes, sem divergência entre si ou com F-23. |
| Q-MEI-03 | Conteúdo integral do Anexo XI da Resolução CGSN nº 140/2018 (lista de ocupações permitidas). | **RESOLVIDA quanto à existência, título e função do Anexo XI** — confirmado por F-31 (citado nominalmente 4 vezes, inclusive como "Anexo XI da Resolução CGSN nº 140, de 2018 – Ocupações Permitidas ao MEI") e F-28. **Aberta quanto ao conteúdo linha a linha**: o PDF oficial (43 páginas, `www8.receita.fazenda.gov.br/simplesnacional/arquivos/manual/anexo_xi.pdf`) não pôde ser extraído pela ferramenta usada nesta pesquisa. Isso não bloqueia a validação da regra de cálculo do MVP, pois a verificação automática de ocupação está deliberadamente fora de escopo (premissa 14 em [calculation-assumptions.md](calculation-assumptions.md)); só afeta uma futura funcionalidade de verificação automática. |
| Q-MEI-04 | Reingresso do MEI e possível parcelamento de débitos do excesso retroativo (>20%). | Fora do escopo desta pesquisa; ver "Casos fora do MVP 1.0". Confirmado por F-31 (capítulo 4) que existe parcelamento convencional (até 60 parcelas) para débitos do MEI, incluindo os do excesso de receita — não implementado nem detalhado aqui. |

### Fontes (TR-003)

F-23, F-25, F-26, F-27, F-28, F-31 — ver [fontes-tributarias.md](fontes-tributarias.md).

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

Tabela **oficial**, publicada pelo Portal Empresas & Negócios (F-30, "Qual o valor das contribuições mensais (Carnê do MEI - DAS) para o ano de 2026?"):

| Categoria | Composição | Total |
|---|---|---|
| Comércio / Indústria (ICMS) | R$ 81,05 (INSS) + R$ 1,00 (ICMS) | **R$ 82,05** |
| Serviços (ISS) | R$ 81,05 (INSS) + R$ 5,00 (ISS) | **R$ 86,05** |
| Comércio e Serviços | R$ 81,05 (INSS) + R$ 1,00 (ICMS) + R$ 5,00 (ISS) | **R$ 87,05** |

A mesma fonte (F-30) traz, para referência (fora do escopo do MVP), os totais do **MEI Caminhoneiro** em 2026: R$ 195,52 (Comércio), R$ 199,52 (Serviços) e R$ 200,52 (Comércio e Serviços) — compostos por R$ 194,52 de INSS (12% do salário mínimo) + R$ 1,00/R$ 5,00/R$ 6,00 de ICMS/ISS.

*Aritmética de conferência (não é fonte, apenas verificação):* 81,05 + 1,00 = 82,05; 81,05 + 5,00 = 86,05; 81,05 + 1,00 + 5,00 = 87,05 — todos batem com a tabela oficial de F-30, sem divergência.

### Vencimento

Confirmado na página oficial "Como pagar seu DAS?" (F-29, Portal Empresas & Negócios): **"Fique atento ao prazo de pagamento: dia 20 de cada mês."** — vencimento do DAS-MEI: dia 20 do mês subsequente à competência. Informação educacional; não faz parte do valor calculado inicialmente.

**Prorrogação em fim de semana/feriado:** corroborada por múltiplas fontes secundárias convergentes, sem divergência entre si (não encontrada, nesta pesquisa, uma página oficial que declare isso explicitamente com o mesmo nível de certeza da regra do "dia 20"). Registrada como informação de alta confiança, mas não como fato 100% confirmado em fonte primária.

**Ressalva de nomenclatura (revisão desta passagem):** a versão anterior deste documento citava "art. 104 da Resolução CGSN nº 140/2018" para o vencimento, com base apenas em mirror privado (LegisWeb). Nesta passagem, ao buscar confirmação em fonte oficial, foram encontradas **citações de artigo divergentes** em diferentes fontes secundárias (art. 40, art. 104, art. 105) para o mesmo dispositivo, e nenhuma delas foi confirmada contra o texto oficial da Resolução (o portal `normas.receita.fazenda.gov.br` continua sem entregar o texto navegável — mesma limitação de F-10/Q-04 em TR-001). **Correção:** a citação "art. 104" foi removida deste documento por falta de confirmação; o fato do "dia 20" permanece registrado com base na fonte oficial F-29 (sem número de artigo), e a prorrogação em dia não útil permanece como informação corroborada, não como citação legal verbatim. Nenhuma ocorrência de "Resolução 100" ou "Resolução 104" (sem o número 140) foi encontrada nos arquivos de pesquisa — não há risco de confusão com as antigas Resoluções CGSN nº 100/2012 e nº 104/2012.

### Relação entre faturamento e DAS

Confirmado: **o SIMEI utiliza valores fixos mensais** e o DAS **não varia proporcionalmente com o faturamento mensal**, desde que o contribuinte permaneça enquadrado nas condições do MEI (F-23, art. 18-A, caput: "valores fixos mensais, **independentemente da receita bruta** por ele auferida no mês").

**Consequência para o motor futuro (documentada, não implementada):** o **faturamento mensal não é multiplicado por alíquota** do DAS-MEI. O faturamento será utilizado principalmente para:

- acompanhar o limite anual/proporcional (TR-003);
- emitir alertas de proximidade ou excesso do limite;
- identificar incompatibilidade/excesso de enquadramento.

### Casos fora do MVP

Ver "Casos fora do MVP 1.0" na seção de escopo, acima. Em particular: MEI Caminhoneiro (regime especial, alíquota de 12% do salário mínimo — R$ 194,52 em 2026, F-24/F-23 art. 18-F — mencionado, não calculado).

### Questões em aberto (TR-004)

| # | Questão | Situação |
|---|---------|----------|
| Q-MEI-05 | Texto integral do artigo da Resolução CGSN nº 140/2018 que trata do vencimento do DAS-MEI (dia 20). | **PARCIALMENTE RESOLVIDA.** O fato "vencimento dia 20 de cada mês" está confirmado em fonte oficial primária (F-29, Portal Empresas & Negócios: "Fique atento ao prazo de pagamento: dia 20 de cada mês"). A prorrogação para dia útil seguinte permanece corroborada apenas por fontes secundárias convergentes. O **número exato do artigo** da Resolução CGSN nº 140/2018 permanece **aberto**: fontes secundárias divergem entre si (art. 40, art. 104, art. 105) e nenhuma foi confirmada contra o texto oficial nesta pesquisa (mesma limitação de acesso de F-10/Q-04). A citação "art. 104", presente em versão anterior deste documento, foi removida por falta de confirmação — ver "Ressalva de nomenclatura" acima. Isso não afeta o valor do DAS (TR-004 é sobre composição/valor, não sobre prazo), apenas a informação educacional do vencimento. |
| Q-MEI-06 | Somatório oficial explícito dos totais por categoria (R$ 82,05 / R$ 86,05 / R$ 87,05) em página única da Receita Federal, em vez de conferência aritmética a partir dos três componentes. | **RESOLVIDA** — a página oficial "Qual o valor das contribuições mensais (Carnê do MEI - DAS) para o ano de 2026?" (F-30, Portal Empresas & Negócios) traz uma tabela única com os três totais por categoria (R$ 82,05 / R$ 86,05 / R$ 87,05) e também os totais do MEI Caminhoneiro, sem necessidade de somar os componentes manualmente. |
| Q-MEI-07 | Receita mensal zero com MEI ativo: o DAS fixo continua devido? | **RESOLVIDA** — confirmado verbatim pelo material oficial "Perguntas e Respostas MEI e Simei" (F-31, Pergunta 3.5): "O MEI inativo está desobrigado de pagar o valor fixo mensal? E se tiver receita zero? **Não.** De qualquer modo, o MEI está obrigado a pagar o valor mensal previsto pelo Simei, porque esse valor é fixo e independe do exercício de atividade e do volume de receita. [...] ainda que esteja inativo ou que tenha receita zero." (Base legal: art. 18-A, "caput", da Lei Complementar nº 123, de 2006 — já confirmado em F-23). Ver TC-MEI-104 abaixo. |

### Fontes (TR-004)

F-23, F-24, F-27, F-29, F-30, F-31 — ver [fontes-tributarias.md](fontes-tributarias.md).

---

## Revisão independente final (2026-09-29)

Conferência cruzada de TR-003 e TR-004 contra as fontes abaixo, sem divergência de valores encontrada.

### TR-003 — conferido contra

- Lei Complementar nº 123/2006, texto compilado (F-23) — art. 18-A confirma limite anual R$ 81.000,00, proporcional R$ 6.750,00 × meses, fração de mês = mês completo, vedações do § 4º e regra dos 20% do § 7º (III e IV).
- Portal do Empreendedor, "Teto do MEI" (F-25) — confere com F-23 em linguagem de página de serviço.
- Resolução CGSN nº 140/2018, condições de elegibilidade (art. 100, inciso I, e art. 101) — **confirmado nesta passagem** por duas fontes oficiais primárias (F-28, F-31), não mais apenas por mirror privado.
- "Perguntas e Respostas MEI e Simei" (F-31, nova nesta passagem) — confirma, com a mesma redação de F-23, a regra dos 20% (resolve Q-MEI-01) e as condições cumulativas de elegibilidade (resolve Q-MEI-02 e, quanto à existência/função, Q-MEI-03).

### TR-004 — conferido contra

- Lei Complementar nº 123/2006, art. 18-A § 3º (F-23) — composição do DAS (INSS 5% do salário mínimo + ICMS R$ 1,00 + ISS R$ 5,00, quando aplicáveis).
- Decreto nº 12.797/2025 (F-27) — salário mínimo de 2026, R$ 1.621,00.
- Receita Federal / Portal do Simples Nacional, "MEI - atualização de valores devidos em 2026" (F-24) — confirma os três componentes individuais.
- Portal Empresas & Negócios, "Qual o valor das contribuições mensais [...] 2026?" (F-30, nova nesta passagem) — **tabela oficial única** com os três totais por categoria; resolve Q-MEI-06.
- Portal Empresas & Negócios, "Como pagar seu DAS?" (F-29, nova nesta passagem) — confirma o vencimento no dia 20.
- "Perguntas e Respostas MEI e Simei" (F-31, nova nesta passagem, Pergunta 3.5) — confirma que o DAS fixo é devido mesmo com receita zero ou inatividade; resolve Q-MEI-07.

### Correção de nomenclatura aplicada nesta passagem

A citação "art. 104 da Resolução CGSN nº 140/2018" (vencimento do DAS-MEI), presente na versão anterior deste documento e baseada apenas em mirror privado (LegisWeb), foi **removida** por não ter sido confirmada contra o texto oficial e por existirem citações divergentes entre fontes secundárias (art. 40, art. 104, art. 105). O fato em si (vencimento dia 20) permanece registrado, agora com base em fonte oficial (F-29), sem número de artigo. Não foi encontrada, em nenhum arquivo de pesquisa, referência a "Resolução 100" ou "Resolução 104" (sem o número 140) que pudesse ser confundida com as antigas Resoluções CGSN nº 100/2012 e nº 104/2012 — todas as ocorrências de "art. 100" já continham a referência completa "Resolução CGSN nº 140/2018".

### Resultado

Nenhuma dúvida normativa nova surgiu nesta revisão que exija reverter a validação. As pendências residuais (Q-MEI-05 quanto ao número exato do artigo de vencimento; Q-MEI-03 quanto ao conteúdo linha a linha do Anexo XI) são de natureza educacional/de implementação futura, não afetam os valores numéricos de TR-003 (limites) nem de TR-004 (composição do DAS), e por isso não bloqueiam a validação.

---

## Casos de teste futuros

Somente **propostas**; nenhum código de teste foi escrito. Os valores esperados só valem depois de revisão independente (status **VALIDADA**).

### TR-003 — limite anual e proporcional

| Caso | Entrada | Situação esperada (a confirmar em validação) |
|------|---------|----------------------------------------------|
| TC-MEI-001 | Receita anual R$ 70.000,00 (MEI o ano todo) | Dentro do limite anual (R$ 81.000,00) |
| TC-MEI-002 | Receita anual exatamente R$ 81.000,00 | No limite (não excedido) |
| TC-MEI-003 | Receita anual R$ 81.000,01 | Excedido; dentro da faixa "não superior a 20%" |
| TC-MEI-004 | Receita anual exatamente R$ 97.200,00 (81.000 × 1,20) | Ainda "não superior a 20%" (Q-MEI-01 RESOLVIDA); efeitos a partir de 1º/jan do ano subsequente |
| TC-MEI-005 | Receita anual R$ 97.200,01 | Excesso superior a 20%; efeitos retroativos a 1º de janeiro do ano do excesso (empresa já existente) |
| TC-MEI-006 | Abertura em julho (6 meses), limite proporcional R$ 40.500,00 | Regra proporcional |
| TC-MEI-007 | Abertura em dezembro (1 mês), limite proporcional R$ 6.750,00 | Regra proporcional, fração de mês = mês completo |

### TR-004 — DAS-MEI

| Caso | Entrada | Esperado (fonte F-30) |
|------|---------|---------------------------------------------|
| TC-MEI-101 | DAS Comércio/Indústria, 2026 | R$ 82,05 |
| TC-MEI-102 | DAS Serviços, 2026 | R$ 86,05 |
| TC-MEI-103 | DAS Comércio e Serviços, 2026 | R$ 87,05 |
| TC-MEI-104 | Receita mensal zero, MEI ativo e optante pelo SIMEI | DAS mensal continua devido conforme categoria (Q-MEI-07 RESOLVIDA, F-31 Pergunta 3.5) |

### Integração MEI (TR-003 + TR-004)

Não há exemplo oficial numérico que combine, em um único caso, o valor do DAS com uma situação de excesso de receita (complementação do § 10 do art. 18-A). Casos combinados exigem revisão independente e, se possível, exemplo oficial antes de virarem teste.
