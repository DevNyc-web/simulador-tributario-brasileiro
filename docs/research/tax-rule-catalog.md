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
| Status de validação | VALIDADA |
| Status de implementação | IMPLEMENTADA |
| Status de testes | TESTADA |

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
| Fonte oficial primária | INSS (F-11, F-12, F-13, F-17, F-18); Planalto (F-14 Lei 8.212/1991); Ministério da Previdência Social/DOU (F-15 Portaria MPS/MF 13/2026); Receita Federal (F-47 IN RFB 2.110/2022, renda zero; F-16 Agenda Tributária 2026; F-05, F-07, F-09 para dedutibilidade) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-11 a F-18 e F-47 |
| Base legal | Lei nº 8.212/1991 (arts. 21, 28 III e § 3º, 30 II); Portaria Interministerial MPS/MF nº 13, de 09/01/2026 (art. 2º; lida no DOU); LC nº 123/2006 e Decreto nº 6.042/2007 (citados em F-13) |
| Artigo/item relevante | Lei 8.212/1991, art. 28, III (salário de contribuição do contribuinte individual), art. 21 (alíquotas) e art. 30, II (vencimento); Portaria MPS/MF 13/2026, art. 2º (mínimo R$ 1.621,00 e máximo R$ 8.475,55) |
| Data da consulta | 2026-09-29 |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md), premissa 11; usuário seleciona o plano |
| Limitações do MVP | Sem tomador PJ (plano simplificado não se aplica a quem presta serviço a empresas), sem MEI, sem facultativo; complementação de 9% fora do cálculo |
| Casos especiais | Prestação de serviço a empresa (responsabilidade da empresa desde 04/2003, F-12); MEI 5%; facultativo baixa renda 5% |
| Questões em aberto | Q-P1, Q-P2 e Q-P4 RESOLVIDAS. Q-P3 FORA DO CÁLCULO DO MVP 1.0 / AVISO EDUCACIONAL. Abertas: Q-P6 (remuneração abaixo do limite mínimo; decisão de produto). Registrada: Q-P5. Detalhes em [pf-2026-research.md](pf-2026-research.md) |
| Status de pesquisa | PESQUISADA |
| Status de validação | VALIDADA |
| Status de implementação | IMPLEMENTADA |
| Status de testes | TESTADA |

## TR-003 — Limite anual e proporcional do MEI

| Campo | Valor |
|-------|-------|
| ID | TR-003 |
| Nome | Limite anual e proporcional do MEI |
| Módulo | MEI |
| Ano de vigência | 2026 (valores de R$ 81.000,00 e R$ 6.750,00 vigentes desde 2018, LC 155/2016; regra do MVP mira 2026) |
| Objetivo da regra | Determinar a situação do faturamento frente ao limite do MEI. |
| Entradas necessárias | ano; faturamento mensal; faturamento anual; mês de início de atividade; categoria/atividade |
| Saídas produzidas | situação (compatível / excesso ≤ 20% / excesso > 20% / incompatível); % do limite utilizado; alertas de incompatibilidade |
| Fórmula/regra | Ver [mei-2026-research.md](mei-2026-research.md), seções "Limite anual", "Ano de abertura / Limite proporcional" e "Excesso de receita — regra dos 20%". Resumo: limite anual R$ 81.000,00; no ano de abertura, limite proporcional = R$ 6.750,00 × número de meses (fração de mês = mês completo); excesso não superior a 20% → efeitos a partir de 1º de janeiro do ano-calendário subsequente; excesso superior a 20% em MEI já existente → efeitos retroativos a 1º de janeiro do ano do excesso; excesso superior a 20% no ano de abertura → efeitos retroativos ao início da atividade. Arredondamento/implementação: não decidido nesta pesquisa. |
| Fonte oficial primária | Lei Complementar nº 123/2006, art. 18-A (F-23); Portal do Empreendedor, "Teto do MEI" (F-25); Portal Empresas & Negócios, "Verifique se você atende as condições para ser MEI" (F-28); Receita Federal/CGSN, "Perguntas e Respostas MEI e Simei" (F-31) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-23, F-25, F-26, F-27, F-28, F-31 |
| Base legal | Lei Complementar nº 123, de 14/12/2006 (art. 18-A, §§ 1º, 2º, 4º, 7º, 10; art. 18-C; art. 18-F); Resolução CGSN nº 140/2018 (art. 100, inciso I; art. 101; art. 112) |
| Artigo/item relevante | Art. 18-A § 1º (limite anual R$ 81.000,00); § 2º (limite proporcional); § 7º, incisos III e IV (desenquadramento por excesso, regra dos 20%); § 10 (complementação do DAS) |
| Data da consulta | 2026-09-29 (pesquisa); 2026-09-29 (validação) |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md); MVP pressupõe ocupação permitida (Anexo XI da Resolução CGSN 140/2018) |
| Limitações do MVP | Sem MEI Caminhoneiro; sem verificação automática de ocupação permitida; sem cálculo de tributos após desenquadramento retroativo; sem parcelamentos, multas, baixa |
| Casos especiais | MEI Caminhoneiro (regime especial, limite R$ 251.600,00, alíquota previdenciária 12%) mencionado, não calculado (F-23 art. 18-F) |
| Questões em aberto | Q-MEI-01, Q-MEI-02 RESOLVIDAS. Q-MEI-03 resolvida quanto à existência/função do Anexo XI; conteúdo linha a linha segue em aberto (não bloqueia validação). Detalhes em [mei-2026-research.md](mei-2026-research.md) |
| Status de pesquisa | PESQUISADA |
| Status de validação | VALIDADA |
| Status de implementação | IMPLEMENTADA |
| Status de testes | TESTADA |

## TR-004 — Composição e cálculo do DAS-MEI

| Campo | Valor |
|-------|-------|
| ID | TR-004 |
| Nome | Composição e cálculo do DAS-MEI |
| Módulo | MEI |
| Ano de vigência | 2026 |
| Objetivo da regra | Determinar o valor do DAS do MEI conforme a categoria suportada. |
| Entradas necessárias | ano; categoria/atividade (Comércio/Indústria, Serviços, ou Comércio e Serviços) |
| Saídas produzidas | DAS estimado (valor fixo mensal); vencimento educacional |
| Fórmula/regra | Ver [mei-2026-research.md](mei-2026-research.md), seções "Previdência", "ICMS", "ISS" e "Valores de 2026". Resumo: DAS = valor fixo mensal, independente do faturamento do mês, composto por 5% do salário mínimo (previdência, R$ 81,05 em 2026) + R$ 1,00 (ICMS, se contribuinte) + R$ 5,00 (ISS, se contribuinte). Totais 2026: Comércio/Indústria R$ 82,05; Serviços R$ 86,05; Comércio e Serviços R$ 87,05. O faturamento mensal **não** é multiplicado por alíquota do DAS-MEI. |
| Fonte oficial primária | Lei Complementar nº 123/2006, art. 18-A § 3º V (F-23); Receita Federal / Portal do Simples Nacional, "MEI - atualização de valores devidos em 2026" (F-24); Decreto nº 12.797/2025 (salário mínimo, F-27); Portal Empresas & Negócios, "Qual o valor das contribuições mensais [...] 2026?" (F-30, tabela oficial dos três totais); "Como pagar seu DAS?" (F-29, vencimento) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-23, F-24, F-27, F-29, F-30, F-31 |
| Base legal | Lei Complementar nº 123, de 14/12/2006 (art. 18-A, § 3º, V; § 11); Decreto nº 12.797, de 23/12/2025 |
| Artigo/item relevante | Art. 18-A, § 3º, V, alíneas a/b/c (composição do valor fixo); § 11 (reajuste anual da parcela previdenciária, mantendo equivalência com 5% do salário mínimo) |
| Data da consulta | 2026-09-29 (pesquisa); 2026-09-29 (validação) |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md); MVP pressupõe ocupação permitida (Anexo XI) |
| Limitações do MVP | Sem MEI Caminhoneiro (alíquota previdenciária de 12%, não 5%); sem vencimento em atraso/multas/juros; sem cálculo do tributo devido após desenquadramento retroativo |
| Casos especiais | MEI Caminhoneiro: R$ 194,52 de contribuição previdenciária em 2026 (12% do salário mínimo), mencionado, não calculado (F-24, F-30, F-23 art. 18-F) |
| Questões em aberto | Q-MEI-06, Q-MEI-07 RESOLVIDAS. Q-MEI-05 parcialmente resolvida: o dia 20 está confirmado em fonte oficial; o número exato do artigo da Resolução CGSN 140/2018 segue incerto (fontes secundárias divergentes) e não é mais citado neste catálogo. Detalhes em [mei-2026-research.md](mei-2026-research.md) |
| Status de pesquisa | PESQUISADA |
| Status de validação | VALIDADA |
| Status de implementação | IMPLEMENTADA |
| Status de testes | TESTADA |

## TR-005 — Limite de receita para permanência no Simples Nacional

| Campo | Valor |
|-------|-------|
| ID | TR-005 |
| Nome | Limite de receita para permanência no Simples Nacional |
| Módulo | Simples Nacional |
| Ano de vigência | 2026 (limite de R$ 4.800.000,00 e sublimite de R$ 3.600.000,00 vigentes desde 1/1/2018, LC 155/2016; sem alteração para 2026 — ver "Alterações 2027+" em [simples-2026-research.md](simples-2026-research.md)) |
| Objetivo da regra | Determinar se a receita do cenário permite permanecer no Simples Nacional e se permanece dentro do sublimite de ICMS/ISS. |
| Entradas necessárias | ano; RBT12; receita bruta acumulada no ano-calendário; mês de início de atividade |
| Saídas produzidas | situação de enquadramento (dentro do limite / excesso ≤20% / excesso >20%); situação do sublimite ICMS/ISS; alertas |
| Fórmula/regra | Ver [simples-2026-research.md](simples-2026-research.md), seção TR-005. Resumo: limite geral R$ 4.800.000,00/ano (art. 3º II); no ano de abertura, o limite é proporcional ao número de meses de atividade (art. 3º § 2º — sem valor mensal literal na lei, R$ 400.000,00/mês é aritmética de conferência); sublimite ICMS/ISS efetivo de **2026 = R$ 3.600.000,00 para todos os Estados e o Distrito Federal** (Portaria CGSN nº 54/2025, F-36), distinto do limite geral de permanência. **Limite funcional do MVP**: o cálculo completo do simulador só é executado para RBT12 ≤ R$ 3.600.000,00; entre R$ 3.600.000,01 e R$ 4.800.000,00 o Simples é legalmente possível, mas o cenário não é suportado integralmente (decisão de produto, não legal). |
| Fonte oficial primária | Lei Complementar nº 123/2006, art. 3º, art. 13-A, art. 19, art. 20 (F-23/F-34); Manual do PGDAS-D e DEFIS (F-32); Portaria CGSN nº 54/2025 (F-36, sublimite efetivo de 2026); Receita Federal, notícia sobre CGSN 190/191/2026 (F-35, só para snapshot 2027+) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-23, F-32, F-34, F-35, F-36 |
| Base legal | Lei Complementar nº 123, de 14/12/2006, art. 3º (II, § 2º, §§ 7º a 13); art. 13-A; art. 19; art. 20; Portaria CGSN nº 54, de 17/11/2025 |
| Artigo/item relevante | Art. 3º II (limite R$ 4.800.000,00); art. 3º § 2º (proporcionalidade, sem valor mensal literal); art. 13-A (sublimite, regra geral R$ 3.600.000,00); art. 19 §§ 1º/4º (sublimite opcional R$ 1.800.000,00, não aplicável em 2026); art. 20 §§ 1º/1º-A (mecânica de impedimento); Portaria CGSN nº 54/2025 (sublimite efetivo de 2026) |
| Data da consulta | 2026-09-30 (pesquisa); 2026-09-30 (validação) |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md); limite funcional do MVP em R$ 3.600.000,00 |
| Limitações do MVP | Excesso de receita (retroatividade, regra dos 20%) documentado, não implementado; mecânica completa de redistribuição de ICMS/ISS acima do sublimite (art. 18 §17) documentada, não implementada; cálculo completo não cobre RBT12 entre R$ 3.600.000,01 e R$ 4.800.000,00 |
| Casos especiais | Empresa em início de atividade (limite proporcional); sublimite estadual opcional de R$ 1.800.000,00 (art. 19) mencionado como regra geral, mas **não aplicável em 2026** (Portaria CGSN 54/2025 fixou R$ 3.600.000,00 para todos os Estados/DF) |
| Questões em aberto | Q-SN-01 (ABERTA, baixa relevância): confirmar se algum ato do CGSN cita literalmente R$ 400.000,00/mês, ou se é sempre aritmética de conferência. Detalhes em [simples-2026-research.md](simples-2026-research.md) |
| Status de pesquisa | PESQUISADA |
| Status de validação | VALIDADA |
| Status de implementação | IMPLEMENTADA |
| Status de testes | TESTADA |

## TR-006 — Tabela do Anexo III

| Campo | Valor |
|-------|-------|
| ID | TR-006 |
| Nome | Tabela do Anexo III |
| Módulo | Simples Nacional |
| Ano de vigência | 2026 (tabela vigente desde 1/1/2018, LC 155/2016; sem alteração para 2026) |
| Objetivo da regra | Fornecer faixas, alíquotas nominais e parcelas a deduzir do Anexo III. |
| Entradas necessárias | ano; RBT12 |
| Saídas produzidas | faixa; alíquota nominal; parcela a deduzir; percentuais de repartição por tributo |
| Fórmula/regra | Ver [simples-2026-research.md](simples-2026-research.md), seção TR-006. Tabela de 6 faixas (até R$180.000,00 a R$4.800.000,00), alíquotas de 6,00% a 33,00%, com parcela a deduzir por faixa; teto de 5% para o percentual efetivo de ISS, com redistribuição aos tributos federais. |
| Fonte oficial primária | Lei Complementar nº 123/2006, Anexo III (F-23/F-34); Manual do PGDAS-D e DEFIS (F-32) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-23, F-32, F-34 |
| Base legal | Lei Complementar nº 123, de 14/12/2006, Anexo III (redação da LC 155/2016) |
| Artigo/item relevante | Anexo III (tabela de alíquotas/PD e percentuais de repartição); art. 18 § 1º-B I (teto de 5% do ISS) |
| Data da consulta | 2026-09-30 |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | Redistribuição de percentuais na 6ª faixa/casos de ISS acima de 5% documentada, não implementada nesta fase; 6ª faixa legalmente vigente, mas fora do cálculo completo do MVP (RBT12 acima do sublimite efetivo de 2026, R$ 3.600.000,00 — ver TR-005) |
| Casos especiais | Redistribuição do percentual de ISS quando a alíquota efetiva superar 14,92537% na 5ª faixa |
| Status de pesquisa | PESQUISADA |
| Status de validação | VALIDADA |
| Status de implementação | IMPLEMENTADA |
| Status de testes | TESTADA |

## TR-007 — Tabela do Anexo V

| Campo | Valor |
|-------|-------|
| ID | TR-007 |
| Nome | Tabela do Anexo V |
| Módulo | Simples Nacional |
| Ano de vigência | 2026 (tabela vigente desde 1/1/2018, LC 155/2016; sem alteração para 2026) |
| Objetivo da regra | Fornecer faixas, alíquotas nominais e parcelas a deduzir do Anexo V. |
| Entradas necessárias | ano; RBT12 |
| Saídas produzidas | faixa; alíquota nominal; parcela a deduzir; percentuais de repartição por tributo |
| Fórmula/regra | Ver [simples-2026-research.md](simples-2026-research.md), seção TR-007. Tabela de 6 faixas (até R$180.000,00 a R$4.800.000,00), alíquotas de 15,50% a 30,50%, com parcela a deduzir por faixa; teto de 5% para o percentual efetivo de ISS, com redistribuição aos tributos federais. |
| Fonte oficial primária | Lei Complementar nº 123/2006, Anexo V (F-23/F-34); Manual do PGDAS-D e DEFIS (F-32) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-23, F-32, F-34 |
| Base legal | Lei Complementar nº 123, de 14/12/2006, Anexo V (redação da LC 155/2016) |
| Artigo/item relevante | Anexo V (tabela de alíquotas/PD e percentuais de repartição); art. 18 § 1º-B I (teto de 5% do ISS) |
| Data da consulta | 2026-09-30 |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md) |
| Limitações do MVP | Redistribuição de percentuais na 6ª faixa/casos de ISS acima de 5% documentada, não implementada nesta fase; 6ª faixa legalmente vigente, mas fora do cálculo completo do MVP (RBT12 acima do sublimite efetivo de 2026, R$ 3.600.000,00 — ver TR-005) |
| Casos especiais | Redistribuição do percentual de ISS quando a alíquota efetiva superar 12,5% na 5ª faixa |
| Status de pesquisa | PESQUISADA |
| Status de validação | VALIDADA |
| Status de implementação | IMPLEMENTADA |
| Status de testes | TESTADA |

## TR-008 — Fórmula da alíquota efetiva do Simples Nacional

| Campo | Valor |
|-------|-------|
| ID | TR-008 |
| Nome | Fórmula da alíquota efetiva do Simples Nacional |
| Módulo | Simples Nacional |
| Ano de vigência | 2026 (fórmula vigente desde 1/1/2018, LC 155/2016; sem alteração para 2026) |
| Objetivo da regra | Definir como a alíquota efetiva e o DAS mensal são obtidos a partir dos dados da tabela aplicável. |
| Entradas necessárias | RBT12; faixa; alíquota nominal; parcela a deduzir; receita bruta do PA (RPA) |
| Saídas produzidas | alíquota efetiva; DAS estimado |
| Fórmula/regra | Ver [simples-2026-research.md](simples-2026-research.md), seção TR-008. Alíquota efetiva = [(RBT12 × alíquota nominal) − parcela a deduzir] / RBT12 (RBT12=0 → considerar RBT12=1); DAS mensal = RPA × alíquota efetiva. Premissas de segregação de receitas (substituição tributária, monofásica, retenção de ISS, exportação, etc.) documentadas e fora do MVP. |
| Fonte oficial primária | Lei Complementar nº 123/2006, art. 18 §§ 1º-A, 3º, 4º-A, 12-17 (F-23/F-34); Manual do PGDAS-D e DEFIS (F-32) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-23, F-32, F-34 |
| Base legal | Lei Complementar nº 123, de 14/12/2006, art. 18 |
| Artigo/item relevante | Art. 18 § 1º-A (fórmula da alíquota efetiva); art. 18 caput/§ 3º (DAS mensal); art. 18 §§ 4º-A e 12-17 (segregação de receitas) |
| Data da consulta | 2026-09-30 |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md); cenário de prestação de serviços simples no mercado interno, sem segregações especiais |
| Limitações do MVP | Sem segregação de receitas (substituição tributária, monofásica, retenção de ISS, ISS a outro município, exportação, ISS fixo); sem opção pelo regime de caixa |
| Casos especiais | RBT12 = 0 → considerar RBT12 = 1 (regra operacional do PGDAS-D) |
| Questões em aberto | Q-SN-04 (pendência técnica, não legal): nenhuma regra de arredondamento confirmada por fonte oficial para a fórmula geral da alíquota efetiva/DAS mensal (distinta do truncamento específico do fator r, esse sim confirmado — ver TR-009). Análoga a Q-02 de TR-001 |
| Status de pesquisa | PESQUISADA |
| Status de validação | VALIDADA |
| Status de implementação | IMPLEMENTADA |
| Status de testes | TESTADA |

## TR-009 — Fator R

| Campo | Valor |
|-------|-------|
| ID | TR-009 |
| Nome | Fator R |
| Módulo | Simples Nacional |
| Ano de vigência | 2026 (regra vigente desde 1/1/2018, LC 155/2016; sem alteração para 2026) |
| Objetivo da regra | Definir o critério que determina o anexo aplicável (III ou V) às atividades sujeitas ao Fator R. |
| Entradas necessárias | folha de salários dos últimos 12 meses (FS12, incluindo pró-labore, CPP e FGTS efetivamente recolhidos); RBT12; atividade exercida; mês de início de atividade (se aplicável) |
| Saídas produzidas | Fator R; anexo aplicável (III ou V) |
| Fórmula/regra | Ver [simples-2026-research.md](simples-2026-research.md), seção TR-009. Fator r = FS12 / RBT12; r ≥ 0,28 → Anexo III; r < 0,28 → Anexo V. Aplica-se só às atividades do art. 18 § 5º-I / § 5º-B (tabela fechada de atividades suportadas no MVP). **Achado da passagem de validação**: FS12 é sempre apurada pelo regime de caixa, independentemente do regime escolhido pela empresa para o DAS mensal; RBT12 permanece sempre pelo regime de competência (Solução de Consulta Cosit nº 17/2021, F-38). Casos-limite (FS12/RBT12 = 0), empresa em início de atividade e truncamento em 2 casas decimais documentados. |
| Fonte oficial primária | Lei Complementar nº 123/2006, art. 18 §§ 5º-I, 5º-J, 5º-K, 5º-M, 24-26 (F-23/F-34); Resolução CGSN nº 140/2018, art. 26 (citado em F-32); Manual do PGDAS-D e DEFIS (F-32); Solução de Consulta Cosit nº 17/2021 (F-38) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-23, F-32, F-34, F-38 |
| Base legal | Lei Complementar nº 123, de 14/12/2006, art. 18 §§ 5º-B, 5º-I, 5º-J, 5º-K, 5º-M, 24, 25, 26; Resolução CGSN nº 140/2018, art. 18 parágrafo único, art. 26 |
| Artigo/item relevante | Art. 18 §§ 5º-J/5º-M (corte de 28%); § 24 (definição de FS12); § 25 (só remunerações informadas via GFIP/eSocial, efetivamente pagas); § 26 (exclusão de aluguéis e distribuição de lucros); Resolução CGSN 140/2018 art. 18 parágrafo único (FS12 sempre por regime de caixa) |
| Data da consulta | 2026-09-30 (pesquisa); 2026-09-30 (validação) |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md); tabela fechada de 9 atividades suportadas no MVP (todas confirmadas como sujeitas ao Fator R) |
| Limitações do MVP | Cálculo de INSS/IRPF do sócio sobre o pró-labore reservado para TR-010/TR-011; apenas o subconjunto de atividades do art. 18 § 5º-I/§5º-B listado é suportado |
| Casos especiais | FS12=0 e RBT12=0 → r=0,01; FS12=0 e RBT12>0 → r=0,01; FS12>0 e RBT12=0 → r=0,28; mês de abertura → r=FSPA/RPA; empresa com <13 meses → soma acumulada desde a abertura (RBT12r); truncamento em 2 casas decimais sem arredondar (desde 04/2018); CPP paga dentro do próprio Simples Nacional integra a FS12, sem exceção (F-38) |
| Questões em aberto | Q-SN-02 (estagiários não entram na FS12 — inferência sistemática, sem Solução de Consulta específica localizada) e Q-SN-03 (MEI contratado nas hipóteses do art. 18-B) são pendências residuais irrelevantes ao MVP. Detalhes em [simples-2026-research.md](simples-2026-research.md) |
| Status de pesquisa | PESQUISADA |
| Status de validação | VALIDADA |
| Status de implementação | IMPLEMENTADA |
| Status de testes | TESTADA |

## TR-010 — Pró-labore e contribuição previdenciária do sócio

| Campo | Valor |
|-------|-------|
| ID | TR-010 |
| Nome | Pró-labore e contribuição previdenciária do sócio |
| Módulo | Pessoa Jurídica |
| Ano de vigência | 2026 (mecânica de retenção vigente desde 2003, Lei nº 10.666/2003; limites de 2026 já validados em TR-002) |
| Objetivo da regra | Determinar a contribuição previdenciária (INSS) e o IRPF associados ao pró-labore do sócio que trabalha na empresa. |
| Entradas necessárias | ano; valor do pró-labore mensal |
| Saídas produzidas | contribuição previdenciária do segurado (11%, limitada ao teto); IRPF do pró-labore (via TR-001); valor líquido do pró-labore |
| Fórmula/regra | Ver [pj-comparator-2026-research.md](pj-comparator-2026-research.md), seção TR-010. Resumo: sócio que trabalha na empresa é contribuinte individual obrigatório (Decreto 3.048/1999 art. 9º V "e" 4, condicionado a receber remuneração pelo trabalho); a empresa desconta 11% do pró-labore (limitado ao teto de R$ 8.475,55) e recolhe junto com sua própria contribuição até o dia 2 do mês seguinte (Lei 10.666/2003 art. 4º); a CPP patronal já está no DAS para Anexo III/V (LC123 art. 13 VI) — não somar 20% adicional; o IRPF segue a tabela progressiva mensal de TR-001. |
| Fonte oficial primária | Decreto nº 3.048/1999, art. 9º V "e" 4 (F-40); Lei nº 10.666/2003, art. 4º (F-41); Lei Complementar nº 123/2006, art. 13 VI e art. 14 (F-23/F-34); Lei nº 8.212/1991 (F-14, já validada em TR-002) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-23/F-34, F-40, F-41 |
| Base legal | Decreto nº 3.048/1999, art. 9º, V, "e", item 4; Lei nº 10.666/2003, art. 4º; LC 123/2006, art. 13, VI, e art. 14; Lei nº 8.212/1991, arts. 21/22/28/30 (já citados em TR-002) |
| Artigo/item relevante | Decreto 3.048/1999 art. 9º V "e" 4 (classificação como contribuinte individual, condicionada a remuneração pelo trabalho); Lei 10.666/2003 art. 4º (responsabilidade de desconto/recolhimento pela empresa); LC123 art. 13 VI (CPP incluída no DAS, exceto Anexo IV) |
| Data da consulta | 2026-09-30 (pesquisa); 2026-09-30 (validação) |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md); sócio único, sem outras fontes de contribuição, sem outra empresa |
| Limitações do MVP | Sem tratamento de múltiplas fontes de contribuição do sócio (Q-PJ-03); sem valor mínimo de pró-labore imposto pelo motor (decisão de produto, ver Q-PJ-01 RESOLVIDA); artigo exato da IN RFB 2.110/2022 não confirmado (Q-PJ-02, não bloqueia o valor de 11%, já bem corroborado); sem cálculo automático de complementação previdenciária quando a remuneração consolidada fica abaixo do salário mínimo (aviso educacional apenas, mesma decisão de TR-002) |
| Casos especiais | Pró-labore = R$ 0,00 (sem contribuinte individual, por ausência de remuneração pelo trabalho); pró-labore acima do teto (contribuição limitada ao teto, sem limite para o valor do pró-labore em si); pró-labore que resulte em remuneração consolidada abaixo do salário mínimo (mecanismo de complementação/utilização/agrupamento, Decreto 3.048/1999 art. 13 §8º/art. 19-E §1º — F-21; INSS F-22/F-18, já confirmados em TR-002) |
| Questões em aberto | Q-PJ-01 **RESOLVIDA** nesta passagem: distinguidos (A) valor do pró-labore, sem piso legal — decisão de produto — de (B) limite mínimo do salário de contribuição/complementação previdenciária, normatizado (F-18/F-21/F-22). Q-PJ-02 (artigo exato da IN RFB 2.110/2022) e Q-PJ-03 (múltiplas fontes de contribuição) são pendências residuais não bloqueantes. Detalhes em [pj-comparator-2026-research.md](pj-comparator-2026-research.md) |
| Status de pesquisa | PESQUISADA |
| Status de validação | VALIDADA |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |

## TR-011 — Distribuição de lucros relevante ao comparador PF x PJ

| Campo | Valor |
|-------|-------|
| ID | TR-011 |
| Nome | Distribuição de lucros relevante ao comparador PF x PJ |
| Módulo | Pessoa Jurídica |
| Ano de vigência | 2026 (regra geral da LC123 art. 14 desde 2007; alterações relevantes da Lei nº 15.270/2025 com efeitos a partir de janeiro/2026) |
| Objetivo da regra | Definir o tratamento tributário da distribuição de lucros que afete o comparador (isenção limitada, retenção de 10% acima de R$ 50 mil/mês, tributação mínima anual). |
| Entradas necessárias | ano; receita bruta (mensal/anual); IRPJ devido no Simples; valor distribuído ao sócio no mês; (opcional) lucro contábil informado, se houver escrituração |
| Saídas produzidas | limite de distribuição isenta (sem escrituração); IRRF retido (10%, se aplicável); indicação de tributação mínima anual não suportada, quando acima de R$ 600.000,00/ano |
| Fórmula/regra | Ver [pj-comparator-2026-research.md](pj-comparator-2026-research.md), seção TR-011. Resumo: sem escrituração contábil, limite isento = 32% da receita bruta (Lei 9.249/1995 art. 15 §1º III "a" — atividades de serviços do MVP, com restrição explícita de escopo para medicina/odontologia que exclui a exceção de serviços hospitalares/diagnóstico) menos o IRPJ devido no Simples; com escrituração contábil regular e balanços intermediários mensais, o limite pode ser maior (Solução de Consulta Cosit 244/2025) — **isso é independente** da retenção mensal de 10% do art. 6º-A, que incide sobre o pagamento à pessoa física quando ultrapassa R$ 50.000,00/mês (Lei 9.250/1995, incluído pela Lei 15.270/2025), **aplicável também ao Simples Nacional** conforme posição oficial da Receita Federal (há liminar judicial isolada em sentido contrário — MS 5002505-76.2026.4.03.6100 — não adotada como base do cálculo); tributação mínima anual (art. 16-A) para renda anual > R$ 600.000,00, a partir do ano-calendário 2026, não calculada integralmente pelo MVP (Opção 3 — aviso apenas). |
| Fonte oficial primária | LC 123/2006, art. 14 (F-23/F-34); Lei nº 9.249/1995, art. 15 (F-43); Lei nº 9.250/1995, arts. 6º-A/16-A/16-B, incluídos pela Lei nº 15.270/2025 (F-39); Receita Federal, Perguntas e Respostas — Tributação de Altas Rendas (F-45); Resolução CGSN nº 140/2018 art. 145 (F-42, fonte secundária); Solução de Consulta Cosit nº 244/2025 (F-44, fonte secundária); Conjur, notícia do MS 5002505-76.2026.4.03.6100 (F-46) |
| URL | Ver [fontes-tributarias.md](fontes-tributarias.md), registros F-23/F-34, F-39, F-42, F-43, F-44, F-45, F-46 |
| Base legal | LC 123/2006, art. 14; Lei nº 9.249/1995, art. 15; Lei nº 9.250/1995, arts. 6º-A, 16-A, 16-B (incluídos pela Lei nº 15.270/2025); Resolução CGSN nº 140/2018, art. 145 |
| Artigo/item relevante | LC123 art. 14 §§1º/2º (limite sem/com escrituração; distinção mensal/antecipação × anual/ajuste); Lei 9.249/1995 art.15 §1º III "a" (32% para serviços, com exceção de saúde restrita fora do MVP); Lei 9.250/1995 art. 6º-A (retenção de 10%, >R$50.000,00/mês); art. 16-A (tributação mínima anual, >R$600.000,00/ano) |
| Data da consulta | 2026-09-30 (pesquisa); 2026-09-30 (validação) |
| Premissas | Ver [calculation-assumptions.md](calculation-assumptions.md); MVP considera somente lucro gerado no próprio ano-calendário de 2026, sem lucros acumulados de 2025 ou anteriores; medicina/odontologia restritas a atendimento profissional comum, fora da exceção de serviços hospitalares/diagnóstico do art. 15 §1º III "a" |
| Limitações do MVP | Sem cálculo de tributação mínima anual (art. 16-A) nem do redutor (art. 16-B) nesta fase — adotada Opção 3 (aviso quando a soma anual ultrapassar R$ 600.000,00, sem cálculo integral) — ver "Alternativas de escopo" em [pj-comparator-2026-research.md](pj-comparator-2026-research.md); sem capitalização de lucros; sem devolução de capital social; sem lucros de 2025 ou anteriores |
| Casos especiais | Distribuição exatamente R$ 50.000,00 (sem retenção); R$ 50.000,01 (retenção de 10% sobre o total); múltiplos pagamentos no mês somados para o cálculo do gatilho |
| Questões em aberto | Q-PJ-04 (liminar judicial concretamente identificada — MS 5002505-76.2026.4.03.6100, 26ª Vara Cível Federal de SP, 09/02/2026 — suspende a retenção apenas para a parte impetrante; RFB mantém posição oficial de aplicação ao Simples Nacional, adotada como base do MVP); Q-PJ-05/Q-PJ-06 (textos oficiais de Resolução CGSN art.145 e Solução Cosit 244/2025 obtidos via fonte secundária, pendências residuais). Detalhes em [pj-comparator-2026-research.md](pj-comparator-2026-research.md) |
| Status de pesquisa | PESQUISADA |
| Status de validação | VALIDADA |
| Status de implementação | PENDENTE |
| Status de testes | PENDENTE |
