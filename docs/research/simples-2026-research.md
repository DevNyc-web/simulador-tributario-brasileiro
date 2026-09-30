# Pesquisa Tributária — Simples Nacional (TR-005 a TR-009) — 2026

Status desta passagem: **PESQUISADA**. Validação: **PENDENTE**. Implementação: **PENDENTE**. Testes: **PENDENTE**.

Esta passagem cobre TR-005 (limite de permanência), TR-006 (Anexo III), TR-007 (Anexo V), TR-008 (alíquota efetiva) e TR-009 (Fator R). Segue a mesma metodologia de [pf-2026-research.md](pf-2026-research.md) e [mei-2026-research.md](mei-2026-research.md): fonte oficial primária como citação final; fonte secundária só para descoberta; toda afirmação numérica ou de fórmula remete a um ID de fonte (F-XX) em [fontes-tributarias.md](fontes-tributarias.md).

## Snapshot normativo do Simples Nacional em 2026

Para o ano-calendário de 2026, o regime aplicável é o "clássico" da LC 123/2006 (com as alterações da LC 155/2016, vigentes desde 01/01/2018) e da Resolução CGSN nº 140/2018, tal como consolidados no texto lido diretamente (F-23/F-34) e confirmados pelo Manual do PGDAS-D e DEFIS, versão de 17/06/2025 (F-32).

A Reforma Tributária do Consumo (IBS/CBS) já produziu alterações textuais na LC 123/2006 por meio da LC nº 214/2025 e da LC nº 227/2026, mas essas alterações aparecem no texto consolidado como remissões `(Vide Lei Complementar nº 214, de 16/1/2025)` — muitas delas também `alterada pela Lei Complementar nº 227, de 13/1/2026` — que **apontam para uma redação futura**, sem substituir a redação hoje operativa. Isso foi confirmado por leitura direta do texto integral da LC 123/2006 (F-34): dispositivos como art. 1º IV, art. 2º, art. 3º §1º/§4º V/XII, art. 12 §§1º-3º, art. 13 IX/X/XII-A/XII-B/XIII/XIV-A, art. 18 §1º/§1º-B I/§4º/§5º-E/§14/§16/§17/§22-A/§23/§24, art. 19 caput/§4º, art. 20 caput, art. 22 caput e incisos IV-VI, art. 23, art. 25, art. 26, art. 29 a 41 (diversos), art. 33, art. 38/38-A/38-B, art. 39 e art. 87-B trazem essa remissão.

Confirmação oficial (Receita Federal, notícia de agosto/2026 — F-35): "A Resolução CGSN nº 190 prevê que suas alterações produzirão efeitos, em regra, a partir de 1º de janeiro de 2027." As Resoluções CGSN nº 190 e nº 191/2026 tratam da incorporação do IBS/CBS ao Simples Nacional, de novos conceitos de início de atividade e receita bruta para fins de IBS/CBS, de procedimentos de emissão de documentos fiscais (em especial para o MEI) e da substituição do PIS/COFINS pela CBS. A única ação com efeito prático já em 2026 é o **prazo de opção** entre "Simples Nacional Puro" e "Simples Nacional Híbrido" (1º a 30/09/2026), mas essa opção só produz efeitos a partir de 2027.

**Achado central**: nenhum dos dispositivos centrais deste MVP — art. 3º II (limite geral de R$ 4.800.000,00), art. 13-A (sublimite de R$ 3.600.000,00), os Anexos III e V (tabelas de alíquotas) e o art. 18 §§5º-J/5º-M (corte de 28% do Fator R) — traz remissão a LC 214/2025 ou LC 227/2026. Esses dispositivos permanecem, para 2026, na redação dada pela LC 155/2016 (vigente desde 01/01/2018), sem alteração. Evidência adicional: o Perguntão do Simples Nacional geral (F-33) está com a nota "Este documento está em atualização para refletir as alterações decorrentes da Reforma Tributária" (datado de 18/09/2026) — mas essa observação recai sobre o Perguntão *geral*; o Perguntão do MEI (F-31, já usado em TR-003/TR-004) segue vigente e completo, sem essa ressalva, e o próprio Manual do PGDAS-D e DEFIS (F-32, versão de 17/06/2025) reproduz as mesmas tabelas e fórmulas clássicas, sem nenhuma tabela de transição IBS/CBS.

**Conclusão**: as regras documentadas abaixo (TR-005 a TR-009) são as vigentes para o cálculo do ano-calendário de 2026. As mudanças relacionadas à Reforma Tributária estão detalhadas na seção "Alterações 2027+ encontradas" e **não** foram aplicadas a nenhum valor ou fórmula deste documento.

## Escopo do MVP

Cenário suportado nesta fase (a ser registrado em [calculation-assumptions.md](calculation-assumptions.md)):

- Prestação de serviços no mercado interno, tributada pelo Anexo III ou Anexo V (conforme premissa 3 já aprovada).
- Sem exportação, sem substituição tributária, sem tributação monofásica, sem retenção de ISS na fonte, sem ISS devido a outro Município, sem ISS por valor fixo (art. 18 §22-A), sem múltiplos estabelecimentos.
- Regime de competência para RBT12 (não se implementa a opção por regime de caixa do art. 18 §3º).
- Fator R aplicado somente às atividades listadas no art. 25 §1º V da Resolução CGSN nº 140/2018 / art. 18 §§5º-B e 5º-I da LC 123/2006 (subconjunto fechado, ver TR-009).
- Pró-labore é considerado apenas como componente da folha de salários (FS12) do Fator R; o cálculo de INSS/IRPF do sócio sobre o pró-labore fica para TR-010/TR-011.

## TR-005 — Limite de receita para permanência no Simples Nacional

### Limite geral

R$ 4.800.000,00 por ano-calendário (LC 123/2006, art. 3º, II, redação dada pela LC 155/2016, com efeitos a partir de 1/1/2018) [F-23/F-34]. Texto literal: *"no caso de empresa de pequeno porte, aufira, em cada ano-calendário, receita bruta superior a R$ 360.000,00 ... e igual ou inferior a R$ 4.800.000,00"*.

### Limite proporcional (ano de início de atividade)

O art. 3º, § 2º, da LC 123/2006 dispõe: *"No caso de início de atividade no próprio ano-calendário, o limite a que se refere o caput deste artigo será proporcional ao número de meses em que a microempresa ou a empresa de pequeno porte houver exercido atividade, inclusive as frações de meses."* [F-23/F-34, leitura literal confirmada].

**Ressalva relevante**: ao contrário do que o valor "R$ 400.000,00 × meses" poderia sugerir, o texto literal do art. 3º § 2º **não fixa nenhum valor mensal explícito** — apenas estabelece o princípio da proporcionalidade sobre o teto de R$ 4.800.000,00. Isso contrasta com o MEI (art. 18-A, § 2º, que cita literalmente "R$ 6.750,00 ... multiplicados pelo número de meses") e com o MEI Caminhoneiro (art. 18-F, II, que cita literalmente "R$ 20.966,67"). O valor R$ 400.000,00 (= R$ 4.800.000,00 / 12) é **aritmética de conferência**, não uma citação literal da lei — registrado como Q-SN-01 (ver "Questões em aberto").

Nota metodológica adicional: essa proporcionalização do *limite de permanência* (art. 3º § 2º) é distinta da proporcionalização da *receita bruta acumulada para fins de alíquota* (RBT12p, Resolução CGSN nº 140/2018, art. 2º, IV/V — ver seção "Conceitos de RBT12 e PA"). Ambas usam o mesmo princípio de anualização, mas servem a propósitos diferentes.

### Sublimite ICMS/ISS

LC 123/2006, art. 13-A (acrescido pela LC 155/2016, efeitos desde 1/1/2018): *"Para efeito de recolhimento do ICMS e do ISS no Simples Nacional, o limite máximo de que trata o inciso II do caput do art. 3º será de R$ 3.600.000,00 (três milhões e seiscentos mil reais)"* [F-23/F-34, leitura literal].

Distinção explícita exigida pelo escopo desta pesquisa:

| | Limite de permanência no Simples Nacional | Sublimite para recolher ICMS/ISS pelo Simples Nacional |
|---|---|---|
| Valor | R$ 4.800.000,00 (art. 3º II) | R$ 3.600.000,00 nacional (art. 13-A), ou R$ 1.800.000,00 nos Estados que adotarem o sublimite opcional (art. 19) |
| Efeito ao ultrapassar | Exclusão do Simples Nacional inteiro (todos os tributos) | ICMS/ISS deixam de ser recolhidos pelo DAS a partir do mês seguinte (art. 20 § 1º); os demais tributos (IRPJ, CSLL, PIS, COFINS, CPP) continuam no Simples Nacional |

Art. 19, *caput* e § 4º: Estados cuja participação no PIB brasileiro seja de até 1% podem optar pelo sublimite de R$ 1.800.000,00; os demais Estados (e os que não exerceram a opção) ficam obrigatoriamente sujeitos ao sublimite de R$ 3.600.000,00 [F-34, leitura literal].

Mecânica de impedimento (art. 20, §§ 1º e 1º-A): o impedimento de recolher ICMS/ISS pelo Simples Nacional produz efeito a partir do mês subsequente ao excesso; se o excesso não superar 20% do sublimite, o efeito só ocorre no ano-calendário subsequente (não retroage).

Impacto no cálculo do Anexo III/V para receita acima de R$ 3.600.000,00: o art. 18, § 17, determina que a parcela de receita que exceder o sublimite fica sujeita, para os percentuais aplicáveis ao ICMS e ao ISS, às alíquotas máximas da 6ª faixa, proporcionalmente. Isso descreve a repartição *interna* enquanto a empresa ainda está no sublimite; uma vez configurado o impedimento efetivo (excesso real, mês seguinte), o ICMS/ISS passa a ser apurado fora do Simples Nacional, pela legislação estadual/municipal ordinária (art. 32 da LC 123/2006).

### Excesso de receita (documentado, não implementado nesta fase)

- Excesso do limite geral (art. 3º § 9º/§ 9º-A): exclusão a partir do mês subsequente à ocorrência; se o excesso não superar 20% do limite, os efeitos só ocorrem no ano-calendário subsequente.
- Excesso do limite proporcional no ano de abertura (art. 3º § 10/§ 12): exclusão com efeitos retroativos ao início das atividades; se o excesso não superar 20% do limite proporcional, sem retroação (efeitos apenas no ano seguinte).

### Questões em aberto

**Q-SN-01** (ABERTA, baixa relevância prática): confirmar se algum ato do CGSN expressa literalmente o valor de R$ 400.000,00/mês para o limite proporcional do art. 3º § 2º, ou se esse valor é sempre aritmética de conferência sem uso operacional direto — o PGDAS-D, na prática, trabalha com RBT12p (receita anualizada), não com uma comparação direta de "receita mensal × 12" contra o teto de R$ 4.800.000,00 para fins de permanência. O resultado numérico é idêntico em ambas as formas; a pendência é apenas sobre a existência (ou não) de uma citação literal.

## Conceitos de RBT12 e PA

- **PA** (período de apuração): o mês considerado como base para apuração da receita bruta [F-32].
- **RBT12**: receita bruta acumulada nos 12 (doze) meses anteriores ao do PA — não inclui o mês do próprio PA (LC 123/2006, art. 18, § 1º e § 1º-A, I) [F-23/F-34; F-32].
- **Regime de apuração**: a RBT12 (e a receita bruta acumulada no ano-calendário, para fins de limite) é sempre apurada pelo regime de competência. O art. 18, § 3º, permite que o contribuinte opte, apenas para a **base de cálculo mensal do DAS**, pelo regime de caixa (receita recebida no mês); essa opção não altera a apuração da RBT12 para fins de alíquota [F-23/F-34; F-32].
- **Empresas com menos de 13 meses (início de atividade)**: a RBT12 é substituída por uma RBT12 proporcionalizada (RBT12p):
  - No mês de abertura: RBT12p = receita do próprio mês (RPA) × 12.
  - Nos meses seguintes, até completar 12 meses de atividade: RBT12p = média aritmética das receitas brutas totais dos meses anteriores ao PA × 12.
  - Base legal da definição de "início de atividade" (período de 60 dias a partir da data de abertura constante do CNPJ): Resolução CGSN nº 140/2018, art. 2º, incisos IV e V [F-32].
  - Essa proporcionalização (para fins de alíquota) é distinta da proporcionalização do limite de permanência (art. 3º § 2º, ver TR-005.2) — ambas usam o mesmo princípio, mas servem propósitos diferentes: uma determina a faixa/alíquota aplicável, a outra determina se a empresa excedeu o teto para continuar no regime.
- **Receita do PA (RPA)**: a receita bruta do próprio mês de apuração, usada como base de cálculo do DAS mensal (LC 123/2006, art. 18, caput e § 3º) — distinta da RBT12, que serve apenas para determinar a faixa/alíquota nominal e a parcela a deduzir [F-23/F-34; F-32].
- **Regra de RBT12 = 0**: para fins de determinação da alíquota efetiva, quando RBT12 = 0, considera-se RBT12 = 1 (regra operacional documentada no Manual do PGDAS-D — F-32; não localizada como texto literal na LC 123/2006).

## TR-006 — Tabela do Anexo III

Tabela confirmada idêntica à indicada no pedido de pesquisa e ao texto oficial da LC 123/2006 (Anexo III, redação dada pela LC 155/2016, vigência 01/01/2018) [F-23/F-34], cross-validada pelo Manual do PGDAS-D e DEFIS (F-32). **Nenhuma divergência encontrada.**

| Faixa | Receita Bruta em 12 Meses (RBT12) | Alíquota nominal | Parcela a Deduzir (PD) |
|---|---|---|---|
| 1ª | Até 180.000,00 | 6,00% | – |
| 2ª | De 180.000,01 a 360.000,00 | 11,20% | 9.360,00 |
| 3ª | De 360.000,01 a 720.000,00 | 13,50% | 17.640,00 |
| 4ª | De 720.000,01 a 1.800.000,00 | 16,00% | 35.640,00 |
| 5ª | De 1.800.000,01 a 3.600.000,00 | 21,00% | 125.640,00 |
| 6ª | De 3.600.000,01 a 4.800.000,00 | 33,00% | 648.000,00 |

Percentual de repartição por faixa (IRPJ / CSLL / COFINS / PIS-Pasep / CPP / ISS): 1ª 4,00/3,50/12,82/2,78/43,40/33,50; 2ª 4,00/3,50/14,05/3,05/43,40/32,00; 3ª 4,00/3,50/13,64/2,96/43,40/32,50; 4ª 4,00/3,50/13,64/2,96/43,40/32,50; 5ª 4,00/3,50/12,82/2,78/43,40/33,50; 6ª 35,00/15,00/16,03/3,47/30,50/–.

Regra do teto de 5% do ISS (LC 123/2006, art. 18 § 1º-B, I): o percentual efetivo máximo destinado ao ISS é 5%; a diferença é transferida proporcionalmente aos tributos federais da mesma faixa. Na 5ª faixa, quando a alíquota efetiva for superior a 14,92537%, aplica-se a redistribuição prevista no próprio Anexo III (fórmulas por tributo, ver LC 123/2006, Anexo III, nota de rodapé).

Casos de faixa (fronteiras, para casos de teste futuros): 180.000,00/180.000,01; 360.000,00/360.000,01; 720.000,00/720.000,01; 1.800.000,00/1.800.000,01; 3.600.000,00/3.600.000,01; 4.800.000,00 (teto).

## TR-007 — Tabela do Anexo V

Tabela confirmada idêntica à indicada no pedido de pesquisa e ao texto oficial da LC 123/2006 (Anexo V, redação dada pela LC 155/2016, vigência 01/01/2018) [F-23/F-34], cross-validada pelo Manual do PGDAS-D e DEFIS (F-32). **Nenhuma divergência encontrada.**

| Faixa | Receita Bruta em 12 Meses (RBT12) | Alíquota nominal | Parcela a Deduzir (PD) |
|---|---|---|---|
| 1ª | Até 180.000,00 | 15,50% | – |
| 2ª | De 180.000,01 a 360.000,00 | 18,00% | 4.500,00 |
| 3ª | De 360.000,01 a 720.000,00 | 19,50% | 9.900,00 |
| 4ª | De 720.000,01 a 1.800.000,00 | 20,50% | 17.100,00 |
| 5ª | De 1.800.000,01 a 3.600.000,00 | 23,00% | 62.100,00 |
| 6ª | De 3.600.000,01 a 4.800.000,00 | 30,50% | 540.000,00 |

Percentual de repartição por faixa (IRPJ / CSLL / COFINS / PIS-Pasep / CPP / ISS): 1ª 25,00/15,00/14,10/3,05/28,85/14,00; 2ª 23,00/15,00/14,10/3,05/27,85/17,00; 3ª 24,00/15,00/14,92/3,23/23,85/19,00; 4ª 21,00/15,00/15,74/3,41/23,85/21,00; 5ª 23,00/12,50/14,10/3,05/23,85/23,50; 6ª 35,00/15,50/16,44/3,56/29,50/–.

Mesma regra do teto de 5% do ISS aplicável (art. 18 § 1º-B, I), com redistribuição na 5ª faixa quando a alíquota efetiva superar 12,5%.

Casos de faixa (mesmos limites do Anexo III): 180.000,00/180.000,01; 360.000,00/360.000,01; 720.000,00/720.000,01; 1.800.000,00/1.800.000,01; 3.600.000,00/3.600.000,01; 4.800.000,00 (teto).

## TR-008 — Fórmula da alíquota efetiva

### Fórmula

Alíquota efetiva = [(RBT12 × alíquota nominal da faixa) − parcela a deduzir da faixa] / RBT12 (LC 123/2006, art. 18, § 1º-A) [F-23/F-34; confirmado pelo Manual do PGDAS-D, F-32, com exemplo numérico]. Quando RBT12 = 0, considera-se RBT12 = 1 [F-32].

### DAS mensal

DAS mensal = receita bruta do PA (RPA) × alíquota efetiva (LC 123/2006, art. 18, caput e § 3º) [F-23/F-34; F-32].

### Premissas de segregação (fora do MVP)

O art. 18, §§ 4º-A e 12 a 17, exige a segregação destacada de receitas sujeitas a: substituição tributária e tributação monofásica; retenção de ISS na fonte ou ISS devido a Município diverso do estabelecimento; ISS por valor fixo, isenção ou redução; exportação para o exterior. Cada uma dessas hipóteses altera o cálculo do DAS (redução de tributos já recolhidos por outra via, tratamento de ICMS/ISS por fora, etc.) e **não é suportada nesta versão do MVP** — o cenário coberto é o de prestação de serviços simples no mercado interno, sem nenhuma dessas segregações.

### Casos fora do MVP

Qualquer receita sujeita aos regimes do parágrafo anterior; atividades do Anexo I, II ou IV; múltiplos estabelecimentos; opção pelo regime de caixa (art. 18 § 3º).

## TR-009 — Fator R

### Fórmula

Fator "r" = FS12 / RBT12 (Resolução CGSN nº 140/2018, art. 26, citado no Manual do PGDAS-D — F-32). O corte de 28% que determina o enquadramento no Anexo III ou V tem base na própria LC 123/2006, art. 18, §§ 5º-J e 5º-M [F-23/F-34, leitura literal confirmada]: "As atividades de prestação de serviços a que se refere o § 5º-I serão tributadas na forma do Anexo III ... caso a razão entre a folha de salários e a receita bruta ... seja igual ou superior a 28%" (§ 5º-J); "Quando a relação ... for inferior a 28% ... serão tributadas na forma do Anexo V" (§ 5º-M).

### FS12 (folha de salários, 12 meses)

Definição literal (LC 123/2006, art. 18, § 24, confirmada por leitura direta e idêntica ao texto do Manual — F-32, que cita o mesmo conteúdo com base no art. 26 da Resolução CGSN nº 140/2018): *"considera-se folha de salários, incluídos encargos, o montante pago, nos doze meses anteriores ao período de apuração, a título de remunerações a pessoas físicas decorrentes do trabalho, acrescido do montante efetivamente recolhido a título de contribuição patronal previdenciária e FGTS, incluídas as retiradas de pró-labore."*

- **Entra**: salários e encargos, 13º salário, retiradas de pró-labore, CPP efetivamente recolhida, FGTS efetivamente recolhido.
- **Não entra** (art. 18, § 26): valores pagos a título de aluguéis e de distribuição de lucros.
- Só entram no cálculo as remunerações informadas na forma do art. 32, IV, da Lei nº 8.212/1991 (GFIP/eSocial) — art. 18, § 25.

### RBT12r (para fins do Fator R)

É o mesmo RBT12 definido na seção "Conceitos de RBT12 e PA" (receita bruta acumulada nos 12 meses anteriores ao PA).

### Corte de 28%

Fator r ≥ 0,28 → Anexo III; fator r < 0,28 → Anexo V (LC 123/2006, art. 18, §§ 5º-J e 5º-M). Aplica-se apenas às atividades listadas no § 5º-I (ver "Atividades suportadas no MVP").

### Pró-labore

O pró-labore integra a folha de salários (FS12) e, portanto, entra no numerador do Fator R. Esta pesquisa **registra** esse fato, mas **não calcula** nesta fase o INSS/IRPF devido pelo sócio sobre o pró-labore — isso é reservado para TR-010/TR-011, conforme já decidido no escopo do projeto.

### Exclusões

Aluguéis e distribuição de lucros não entram na FS12 (art. 18, § 26).

### Empresas novas

- Mês de abertura: fator r = FSPA/RPA (usa os valores do próprio PA, não os 12 meses acumulados). Casos-limite: FSPA>0 e RPA=0 → fator r = 0,28; FSPA=0 e RPA>0 → fator r = 0,01 [F-32].
- Empresas com menos de 13 meses desde a abertura: fator r = (soma da folha de salários desde o mês de abertura até o mês anterior ao PA) / (soma das receitas desde o mês de abertura até o mês anterior ao PA) [F-32].

### Casos especiais (valores de FS12/RBT12 iguais a zero)

- FS12 = 0 e RBT12 = 0 → fator r = 0,01.
- FS12 = 0 e RBT12 > 0 → fator r = 0,01.
- FS12 > 0 e RBT12 = 0 → fator r = 0,28.
- Truncamento: desde 04/2018, o sistema trunca o resultado do fator r em duas casas decimais, sem arredondar (ex.: 0,2774 vira 0,27, não 0,28). Antes disso (01 a 03/2018) havia arredondamento — irrelevante para 2026, registrado apenas por precisão histórica [F-32].

### Atividades suportadas no MVP

Atividades sujeitas ao Fator R (Resolução CGSN nº 140/2018, art. 25, § 1º, V; equivalentes na LC 123/2006 art. 18 §§ 5º-B e 5º-I) — lista fechada confirmada em F-32 e cruzada com o texto literal da LC 123/2006 (F-34):

Administração e locação de imóveis de terceiros; academias de dança/capoeira/ioga/artes marciais; academias de atividades físicas/desportivas/natação/escolas de esportes; elaboração de programas de computador (inclusive jogos eletrônicos) desenvolvidos no estabelecimento do optante; licenciamento/cessão de uso de programas de computação; planejamento/confecção/manutenção/atualização de páginas eletrônicas (no estabelecimento do optante); empresas montadoras de estandes para feiras; laboratórios de análises clínicas/patologia clínica; serviços de tomografia/diagnósticos por imagem/ressonância magnética; serviços de prótese em geral; fisioterapia; medicina (inclusive laboratorial) e enfermagem; medicina veterinária; odontologia e prótese dentária; psicologia/psicanálise/terapia ocupacional/acupuntura/podologia/fonoaudiologia/clínicas de nutrição e vacinação/bancos de leite; serviços de comissaria/despachantes/tradução/interpretação; engenharia/medição/cartografia/topografia/geologia/geodésia/testes/suporte e análises técnicas e tecnológicas/pesquisa/design/desenho/agronomia; representação comercial e demais atividades de intermediação de negócios e serviços de terceiros; perícia/leilão/avaliação; auditoria/economia/consultoria/gestão/organização/controle/administração; jornalismo e publicidade; agenciamento (exceto de mão de obra); arquitetura e urbanismo; outras atividades intelectuais de natureza técnica/científica/desportiva/artística/cultural não relacionadas nos Anexos III (sem Fator R), IV ou V de forma diversa.

Tabela didática do MVP (subconjunto do prompt do usuário, verificado individualmente contra a lista acima — todas as 9 atividades confirmadas como sujeitas ao Fator R):

| Atividade | Base legal | Sujeita ao Fator R? | Suportada no MVP? |
|---|---|---|---|
| Desenvolvimento de software | LC 123/2006, art. 18 § 5º-D, IV | Sim | Sim |
| Consultoria | LC 123/2006, art. 18 § 5º-I, IX | Sim | Sim |
| Engenharia | LC 123/2006, art. 18 § 5º-I, VI | Sim | Sim |
| Arquitetura | LC 123/2006, art. 18 § 5º-B, XVIII | Sim | Sim |
| Medicina | LC 123/2006, art. 18 § 5º-B, XIX | Sim | Sim |
| Odontologia | LC 123/2006, art. 18 § 5º-B, XX | Sim | Sim |
| Psicologia | LC 123/2006, art. 18 § 5º-B, XXI | Sim | Sim |
| Fisioterapia | LC 123/2006, art. 18 § 5º-B, XVI | Sim | Sim |
| Academias | LC 123/2006, art. 18 § 5º-D, II/III | Sim | Sim |

Atividades do Anexo III **não** sujeitas ao Fator R, tributadas diretamente pelo Anexo III (Resolução CGSN 140/2018, art. 25, § 1º, III / § 2º, I / § 11; LC 123/2006 art. 18 § 5º-B I-XV/XVII, exceto as listadas acima): creche/pré-escola/ensino fundamental/escolas técnicas/línguas/artes/pilotagem/preparatórios para concursos/gerenciais/escolas livres; agência terceirizada de correios; agência de viagem e turismo; centro de formação de condutores; agência lotérica; serviços de instalação/reparo/manutenção/usinagem/solda/tratamento/revestimento em metais; transporte municipal de passageiros; escritórios de serviços contábeis; produções cinematográficas/audiovisuais/artísticas/culturais; corretagem de seguros — **fora do MVP** (não fazem parte do subconjunto de atividades suportadas).

Atividades do Anexo IV (art. 18 § 5º-C — não sujeitas ao Fator R, sem CPP no Simples): construção de imóveis e obras de engenharia; execução de projetos e serviços de paisagismo; decoração de interiores; serviço de vigilância/limpeza/conservação; serviços advocatícios — **fora do MVP**.

## Alterações 2027+ encontradas durante a pesquisa

- Resoluções CGSN nº 190 e nº 191/2026 (F-35, notícia oficial da Receita Federal, agosto/2026): incorporam IBS/CBS ao Simples Nacional; ajustam conceitos de início de atividade e receita bruta para fins de IBS/CBS; alteram procedimentos de emissão de documentos fiscais (especialmente para o MEI); disciplinam a substituição do PIS/Cofins pela CBS. Produzem efeitos, em regra, a partir de 1º/1/2027. O único efeito prático em 2026 é o prazo de opção pelo regime (Simples Nacional Puro ou Híbrido), em setembro/2026, para vigência em 2027.
- LC nº 214/2025 e LC nº 227/2026: inseriram dezenas de remissões `(Vide Lei Complementar nº 214/227)` na LC 123/2006 (arts. 1º, 2º, 3º, 12, 13, 18, 19, 20, 22, 23, 25, 25-A, 25-B, 26, 29-41, 87-B, entre outros), todas apontando para uma redação futura, sem substituir a redação hoje operativa.
- **Nenhuma** dessas remissões atinge o art. 3º II (limite geral), o art. 13-A (sublimite), os Anexos III e V (tabelas de alíquotas) ou o art. 18 §§ 5º-J/5º-M (corte de 28% do Fator R) — os dispositivos centrais deste MVP permanecem, para 2026, na redação vigente desde 2018 (LC 155/2016).
- **Nota**: alterações publicadas em 2025/2026 com efeitos a partir de 2027 — **não aplicadas** ao cálculo de 2026 deste MVP.

## Questões em aberto

- **Q-SN-01** (ver TR-005.2): confirmar se algum ato do CGSN expressa literalmente o valor de R$ 400.000,00/mês para o limite proporcional do art. 3º § 2º, ou se é sempre aritmética de conferência. Baixa relevância prática (resultado numérico idêntico); pendência apenas de precisão de citação.

## Casos de teste futuros (propostos, não implementados)

RBT12 nos valores de fronteira, para Anexo III e Anexo V (12 casos): 180.000,00 / 180.000,01; 360.000,00 / 360.000,01; 720.000,00 / 720.000,01; 1.800.000,00 / 1.800.000,01; 3.600.000,00 / 3.600.000,01; 4.800.000,00 / 4.800.000,01 (acima do teto, fora do Simples).

Casos de Fator R: fator r = 0,27 (Anexo V); fator r = 0,28 (Anexo III, fronteira exata); fator r = 0,29 (Anexo III); RBT12 = 0 (regra especial); FS12 = 0 e RBT12 = 0; empresa em início de atividade no mês 1 (fator r = FSPA/RPA), no mês 6 (fator r acumulado <13 meses) e no mês 12.

Caso de sublimite: RBT12 = 3.600.000,01 (transição — ICMS/ISS apurados fora do Simples Nacional a partir do mês seguinte, demais tributos permanecem no DAS).
