# Simulador Tributário Brasileiro 2026–2033
<!-- Nota interna (não aparece na versão renderizada): preencher [Inserir integrantes] e [Inserir orientador(a)] antes de gerar o artefato final. -->

**Sistema web educacional para simulação e comparação tributária**

Relatório final do projeto — documentação acadêmica

---

## 1. Identificação do projeto

| Campo | Informação |
|---|---|
| Título | Simulador Tributário Brasileiro 2026–2033 |
| Subtítulo | Sistema web educacional para simulação e comparação tributária |
| Natureza | Projeto acadêmico (trabalho de disciplina); ferramenta educacional, não comercial |
| Versão entregue | 1.0 — MVP com motor tributário real para o ano-calendário de 2026 (base: commit `1f28c60`, merge do PR #2 na `main`) |
| Ano | 2026 |
| Integrantes | [Inserir integrantes] |
| Orientação acadêmica | [Inserir orientador(a)] |
| Repositório | `DevNyc-web/simulador-tributario-brasileiro` (identificador da conta no GitHub; não é nome de integrante) |
| Tecnologias principais | Python 3.12; Flask (≥ 3.0); HTML5, CSS3 e JavaScript puros; JSON versionado por ano; `decimal.Decimal`; pytest (≥ 8); coverage 7.16.2 (apenas desenvolvimento); Git/GitHub |
| Métricas de entrega | 432 testes automatizados; 98% de cobertura de linhas (`src` + `app.py`); ≈ 2.000 linhas de código-fonte e ≈ 2.100 linhas de testes |

> **Nota metodológica.** Ferramentas de assistência por inteligência artificial foram utilizadas como apoio ao desenvolvimento, revisão e documentação. As decisões de escopo, validação e entrega permaneceram sob responsabilidade da equipe do projeto.

---

## 2. Resumo executivo

A legislação tributária brasileira para pessoas físicas, autônomos, microempreendedores individuais (MEI) e prestadores de serviços optantes pelo Simples Nacional é extensa e mutável, o que dificulta a compreensão do impacto aproximado de cada estrutura. Este projeto entrega um simulador web educacional que calcula, de forma rastreável e explicada, tributos de cenários do ano-calendário de 2026 e apresenta diferenças numéricas entre a atuação como pessoa física e como pessoa jurídica.

O público-alvo são estudantes, profissionais autônomos, MEIs e prestadores de serviços que desejam entender ordens de grandeza e premissas, bem como docentes e profissionais que queiram usar a ferramenta como material didático. O sistema **não** substitui contador nem orientação jurídica e **não** recomenda regime tributário.

Os módulos implementados são: Pessoa Física/autônomo (IRPF mensal e INSS do contribuinte individual), MEI (limite de receita e DAS-MEI), Simples Nacional para serviços (Anexos III e V, RBT12/RBT12p, Fator R), pró-labore do sócio, distribuição de lucros (IRRF mensal e limite sem escrituração) e o comparador PF × PJ. Cada módulo apoia-se em regras tributárias catalogadas (TR-001 a TR-011), pesquisadas, validadas contra fontes oficiais, implementadas e testadas. Uma linha do tempo educacional da Reforma Tributária (2026–2033) existe como **estrutura de navegação**; seu conteúdo por ano ainda está marcado como pendente de validação.

A arquitetura é uma aplicação web monolítica modular em camadas (interface → rotas Flask → serviços/adaptadores → motor tributário → carga de regras → JSON por ano), sem banco de dados, sem autenticação e sem dependência externa em tempo de execução para o cálculo. Todo parâmetro fiscal vive em `data/tax_rules/<ano>/rules.json`; o código contém apenas fórmulas. O resultado técnico é medido: **432 testes automatizados, todos aprovados, com 98% de cobertura de linhas** (meta acadêmica: ≥ 80%; a cobertura não é, nem se afirma ser, de 100%).

**Estado por ano:** 2026 possui motor tributário real. 2027–2033 possuem apenas arquivos de regras vazios e a linha do tempo educacional; **não há cálculo fiscal para esses anos**.

---

## 3. Contexto, problema e oportunidade

### 3.1 Contexto

A partir de 2026 iniciou-se a transição da Reforma Tributária do consumo, e a Lei nº 15.270/2025 alterou a tributação da renda da pessoa física (redução mensal do IRPF e tributação de lucros e dividendos). Ao mesmo tempo, as regras do Simples Nacional, do MEI e da previdência do contribuinte individual continuam a depender de tabelas, limites e fórmulas atualizados anualmente.

### 3.2 Problema

A complexidade do sistema tributário brasileiro torna difícil para pessoas físicas, autônomos, MEIs e prestadores de serviços compreenderem o impacto aproximado de diferentes estruturas tributárias. Ferramentas existentes costumam ocultar premissas, misturar regras de anos distintos ou apresentar resultados sem rastro de origem, o que dificulta o uso didático.

O sistema procura tornar esse cálculo:

- **rastreável** — cada regra remete a fontes oficiais registradas;
- **educacional** — resultados acompanham explicações e avisos;
- **estruturado** — modelos imutáveis, enums e camadas separadas;
- **baseado em regras versionadas** — parâmetros por ano em arquivos de dados.

O sistema não afirma substituir o trabalho do contador.

### 3.3 Oportunidade

- Centralizar simulações de perfis distintos em um só lugar.
- Melhorar a compreensão tributária por meio de explicações passo a passo.
- Comparar cenários sob premissas explícitas e equivalentes.
- Apresentar premissas, limitações e avisos junto a cada resultado.
- Versionar regras fiscais para auditoria e atualização sem alterar a interface.
- Preparar a arquitetura para alterações legislativas futuras.

Distingue-se a **oportunidade acadêmica** (objeto deste trabalho: construir e demonstrar um sistema rastreável, testado e documentado) de um eventual **produto comercial futuro** (que exigiria hospedagem, manutenção legislativa contínua, revisão profissional e modelo de sustentação — discutido apenas como hipótese na seção 13.4).

---

## 4. Proposta de valor

> Permitir que o usuário simule cenários tributários de 2026 de maneira transparente, apresentando cálculo, premissas, avisos e diferenças entre cenários, sem substituir orientação profissional.

O sistema não promete economia tributária, não escolhe regime e não recomenda estrutura ideal. O comparador apresenta diferenças aritméticas, sem juízo de valor.

---

## 5. Objetivos

### 5.1 Objetivo geral

Desenvolver e documentar um sistema web educacional capaz de simular, com regras tributárias de 2026 rastreáveis e testadas, cenários de pessoa física autônoma, MEI e Simples Nacional, e de compará-los numericamente, acompanhado de uma estrutura educacional para a transição 2026–2033.

### 5.2 Objetivos específicos

1. Calcular o IRPF mensal e o INSS do contribuinte individual para PF/autônomo (TR-001, TR-002).
2. Verificar o limite de receita do MEI e calcular o DAS-MEI (TR-003, TR-004).
3. Calcular o DAS do Simples Nacional para serviços, com RBT12/RBT12p e limites de permanência (TR-005, TR-008).
4. Aplicar as tabelas dos Anexos III e V (TR-006, TR-007).
5. Calcular o Fator R e escolher entre os Anexos III e V (TR-009).
6. Calcular INSS e IRPF do pró-labore do sócio (TR-010).
7. Calcular o IRRF sobre dividendos, o limite de distribuição sem escrituração e sinalizar altas rendas (TR-011).
8. Comparar PF × PJ para a mesma receita, sem recomendar opção.
9. Oferecer uma linha do tempo educacional da Reforma 2026–2033 (estrutura; conteúdo pendente).
10. Manter rastreabilidade entre regra, fonte, implementação e teste.
11. Garantir qualidade por testes automatizados, com cobertura mínima de 80%.

---

## 6. Ciclo de vida do desenvolvimento (SDLC)

A **gestão documental** do projeto segue uma decomposição tradicional (iniciação, requisitos, análise, projeto, implementação, testes, entrega, evolução). A **implementação**, por sua vez, ocorreu de forma **incremental, em fases curtas** com revisão e aprovação ao final de cada uma e integração por *pull requests*. Não há registro no projeto da adoção de Scrum (sem *sprints* formais, *backlog* com estimativas ou cerimônias); por isso o projeto não é descrito como Scrum.

| Fase clássica | Como ocorreu no projeto | Evidência |
|---|---|---|
| 1. Iniciação | Definição do problema, objetivo e estrutura inicial | `README.md`; commit `4bba18f` |
| 2. Requisitos | Escopo, requisitos, MoSCoW, fluxo do usuário | `docs/project/*`; commit `939db10` |
| 3. Análise | Pesquisa tributária: catálogo de regras TR-001 a TR-011, fontes oficiais, premissas, validação independente | `docs/research/*`; PR #1 (`03f9748`) |
| 4. Projeto/design | Esqueleto da interface; arquitetura de camadas e contrato de regras (schema, status, `Decimal`) | `5fc4bf9`; `docs/project/tax-engine-architecture.md`; `dbfe3a7` |
| 5. Implementação | Motores PF, MEI, Simples, pró-labore/dividendos, comparador; integração web | `28f8867`, `51f206e`, `72354d2`, `eec8aa3`, `6d55116` |
| 6. Testes | Testes por módulo, integração HTTP, entradas hostis, cobertura | `1ff048b`; `docs/project/testing-and-quality.md` |
| 7. Implantação/entrega | Merge do PR #2 na `main`; branch de entrega final; este relatório | `1f28c60`; branch `feat/final-delivery` |
| 8. Manutenção/evolução | Atualização anual das regras; roadmap (seção 35) | Planejada; não iniciada |

Princípio condutor do desenvolvimento: **nenhuma regra é implementada sem pesquisa e validação prévias**, e uma regra só passa a produzir número quando está implementada no código (ciclo `PENDENTE → PESQUISADA → VALIDADA → IMPLEMENTADA → TESTADA`).

---

## 7. Equipe e responsabilidades

Não há, na documentação do repositório, identificação inequívoca de integrantes além do identificador de conta do GitHub. Por isso os nomes permanecem como placeholder. A tabela distingue **papel** (função do projeto) de **pessoa**.

| Pessoa | Papel | Responsabilidades |
|---|---|---|
| [Inserir integrantes] | Gestão do projeto | Escopo, cronograma, riscos, comunicação, aprovação de fases |
| [Inserir integrantes] | Análise tributária | Pesquisa em fontes oficiais, catálogo de regras, premissas, validação |
| [Inserir integrantes] | Desenvolvimento | Arquitetura, motor tributário, interface, integração |
| [Inserir integrantes] | Testes e qualidade (QA) | Estratégia de testes, cobertura, revisão adversarial |
| [Inserir orientador(a)] | Orientação acadêmica | Avaliação, validação de premissas e de escopo |

Uma mesma pessoa pode acumular mais de um papel (caso típico de projeto acadêmico de pequena equipe). Nenhuma participação de contador externo é afirmada.

---

## 8. Stakeholders

| Stakeholder | Interesse | Influência | Necessidade | Estratégia de comunicação |
|---|---|---|---|---|
| Equipe acadêmica (integrantes) | Concluir o trabalho com qualidade | Alta | Escopo claro, prazo viável, requisitos rastreáveis | Acompanhamento de fases e revisão contínua |
| Professor/orientador | Avaliar rigor técnico e metodológico | Alta | Documentação completa, evidências de qualidade | Relatórios de fase, entrega final com evidências |
| Usuários do simulador (estudantes, autônomos, MEIs) | Entender impacto tributário aproximado | Média | Interface simples, resultados explicados, avisos claros | Textos na própria interface e página *Sobre* |
| Profissionais contábeis (externos, potenciais) | Usar como apoio didático; preservar correção técnica | Média (potencial) | Fontes rastreáveis, premissas explícitas | Catálogo de regras e documentação pública no repositório |
| Mantenedores futuros | Evoluir o sistema | Média | Código modular, testes, regras versionadas | `README`, documentação técnica, suíte de testes |
| Órgãos normativos (fontes oficiais) | — (fornecem a base normativa, sem envolvimento direto) | Alta sobre as regras | Consulta às fontes oficiais | Registro de fontes em `docs/research/fontes-tributarias.md` |

---

## 9. Levantamento de requisitos

Os requisitos abaixo consolidam, para este relatório, o que o sistema **efetivamente implementa**. A especificação original das fases iniciais está em `docs/project/requirements.md` (RF-001 a RF-030), com granularidade maior; a coluna "Ref." indica a correspondência aproximada.

### 9.1 Requisitos funcionais

| ID | Requisito | Situação | Ref. (`requirements.md`) |
|---|---|---|---|
| RF-01 | Simular Pessoa Física/autônomo: INSS do contribuinte individual (planos normal e simplificado) e IRPF mensal (TR-001, TR-002) | Implementado | RF-001..005 |
| RF-02 | Simular MEI: limite anual/proporcional, classificação do excesso e DAS fixo (TR-003, TR-004) | Implementado | RF-006, RF-007 |
| RF-03 | Simular Simples Nacional (serviços): RBT12/RBT12p, limites, alíquota efetiva e DAS (TR-005, TR-008) | Implementado | RF-009..013 |
| RF-04 | Calcular o Fator R (primeiro mês, meses 2–12 e 13+ meses; truncamento em duas casas) (TR-009) | Implementado | RF-010 |
| RF-05 | Selecionar Anexo III ou V e a faixa correspondente (TR-006, TR-007) | Implementado | RF-010, RF-011 |
| RF-06 | Calcular INSS e IRPF do pró-labore do sócio (TR-010) | Implementado | RF-012, RF-017 |
| RF-07 | Calcular dividendos: IRRF mensal, limite sem escrituração, modo com escrituração, aviso de altas rendas (TR-011) | Implementado | RF-017 (parcial) |
| RF-08 | Comparar PF × PJ para a mesma receita, com diferenças numéricas e sem recomendação | Implementado | RF-015..019 |
| RF-09 | Exibir explicações, avisos e identificadores de regra (TR-xxx) em cada resultado | Implementado | RF-005, RF-013, RF-027 |
| RF-10 | Exibir a linha do tempo da Reforma 2026–2033 | **Parcial**: navegação por ano implementada; conteúdo educacional por ano ainda marcado "pendente de validação" | RF-021..023 |
| RF-11 | Validar entradas no servidor (formato, faixa, enums, histórico) com mensagem por campo | Implementado | RF-029 |
| RF-12 | Apresentar formulários e resultados no navegador (`POST /resultado`) | Implementado | RF-024..026 |
| RF-13 | Carregar regras versionadas por ano e recusar cálculo de regra não implementada/testada | Implementado | RF-027, RF-028 |
| RF-14 | Informar cenário não suportado ou incompatível sem exibir resultado parcial | Implementado | RF-014 |

Itens da especificação original **não** implementados (ver seção 34): gráficos comparativos, diferença anual no comparador, botão "Simular no Simples" a partir do MEI, preservação de dados entre telas (RF-008, RF-018, RF-020, RF-030 do documento original).

### 9.2 Requisitos não funcionais

| ID | Requisito | Verificação |
|---|---|---|
| RNF-01 | Valores monetários e fiscais em `Decimal`; nunca `float` | Modelos validam tipo; testes de ausência de `float` |
| RNF-02 | Nenhuma constante fiscal no código Python de cálculo; parâmetros em `rules.json` | Varredura de valores fiscais no código; testes de contrato do JSON |
| RNF-03 | Nenhuma lógica fiscal em `app.py`, templates e JavaScript | Teste automatizado de auditoria de camadas |
| RNF-04 | Rastreabilidade: cada regra com ID (TR-xxx), fontes e status | `rules.json`, `tax-rule-catalog.md`, matriz |
| RNF-05 | Regras versionadas por ano (`data/tax_rules/<ano>/rules.json`) | Testes do *loader* para 2026–2033 |
| RNF-06 | Separação em camadas (interface → serviços → motor → regras → dados) | Estrutura de pacotes; testes do motor sem Flask |
| RNF-07 | Interface responsiva, sem rolagem horizontal em 360 px | Medição programática em 15 páginas; revisão visual manual pendente |
| RNF-08 | Acessibilidade básica (rótulos, `fieldset/legend`, `aria-invalid`, `aria-describedby`, foco) | Testes de rótulos e de âncoras de erro; revisão estática |
| RNF-09 | Segurança de saída: *autoescaping* ativo, sem `|safe`, entrada escapada | Testes específicos |
| RNF-10 | Cobertura de testes ≥ 80% | 98% medidos (`coverage`) |
| RNF-11 | Entrada inválida ou hostil nunca gera erro 500 | Varredura de entradas extremas nos quatro formulários |
| RNF-12 | Manutenção e extensibilidade: adicionar ano/regra sem alterar a interface | Arquitetura de regras por ano; modelos por módulo |
| RNF-13 | Sem persistência de dados pessoais; sem sessão, banco ou login | Inspeção do código; ausência de dependências de persistência |
| RNF-14 | Tempo de resposta local imediato, sem I/O externo no cálculo | Inspeção: apenas leitura do JSON local; sem chamadas HTTP |

---

## 10. Priorização MoSCoW

Critério: **Must** = núcleo indispensável a um MVP executável em horizonte acadêmico de aproximadamente 4–6 semanas; **Should** = importante, mas não bloqueante; **Could** = desejável futuro; **Won't** = explicitamente fora desta entrega.

| ID | Requisito | Prioridade | Justificativa | Situação |
|---|---|---|---|---|
| RF-01 | PF/autônomo | Must | Base do comparador e caso de uso mais simples | Entregue |
| RF-02 | MEI | Must | Perfil-alvo do público; porta de entrada ao Simples | Entregue |
| RF-03 | Simples Nacional | Must | Principal módulo da proposta | Entregue |
| RF-04 | Fator R | Must | Determina o anexo; sem ele o Simples fica incorreto | Entregue |
| RF-05 | Anexos III/V | Must | Tabelas de cálculo do DAS | Entregue |
| RF-06 | Pró-labore (INSS/IRPF) | Must | Necessário ao cenário PJ e ao comparador | Entregue |
| RF-08 | Comparador PF × PJ | Must | Funcionalidade central da apresentação | Entregue |
| RF-09 | Explicações e avisos | Must | Finalidade educacional | Entregue |
| RF-11 | Validação de entradas | Must | Evita cálculo com dado inválido | Entregue |
| RF-12 | Resultados no navegador | Must | Uso pelo público | Entregue |
| RF-13 | Regras versionadas e rastreáveis | Must | "Sem fonte, sem regra" | Entregue |
| RF-14 | Cenário não suportado sem resultado parcial | Must | Evita números enganosos | Entregue |
| RNF-01, 02, 03 | `Decimal`, parâmetros em JSON, sem lógica fiscal na interface | Must | Correção e auditabilidade | Entregue |
| RNF-10 | Cobertura ≥ 80% | Must | Meta acadêmica | Entregue (98%) |
| RF-07 | Dividendos (IRRF, limite sem escrituração) | Should | Refina o cenário PJ; depende de pesquisa adicional | Entregue |
| RF-10 | Linha do tempo da Reforma (estrutura e conteúdo) | Should | Objetivo educacional do projeto; conteúdo exige nova pesquisa | Estrutura entregue; conteúdo pendente |
| RNF-07, 08 | Responsividade e acessibilidade básica | Should | Qualidade de uso | Entregues (revisão visual manual pendente) |
| — | Atalhos entre simulações (ex.: MEI → Simples) | Should | Melhora de fluxo | Não entregue |
| — | Diferença anual no comparador | Should | Complementa a diferença mensal | Não entregue |
| — | Gráficos comparativos | Could | Apoio visual | Não entregue |
| — | Exportação (impressão/PDF/CSV) | Could | Conveniência | Não entregue |
| — | Histórico temporário de simulações | Could | Conveniência | Não entregue |
| — | Lucro Presumido simplificado | Could | Ampliação de cobertura | Não entregue |
| — | Lucro Real / Lucro Presumido completos | Won't | Complexidade fora do horizonte | Fora do escopo |
| — | Cálculo completo 2027–2033; IBS/CBS detalhado | Won't | Regras ainda em transição; requer nova pesquisa | Fora do escopo |
| — | Banco de dados, login, histórico persistente | Won't | Não necessários ao MVP; implicações de LGPD | Fora do escopo |
| — | APIs governamentais; atualização legal automática | Won't | Dependência externa e risco normativo | Fora do escopo |
| — | IA; aplicativo mobile; consultoria personalizada | Won't | Fora da proposta | Fora do escopo |

**Distribuição:** Must = 14 itens (12 RF + 2 grupos de RNF, contando RNF-01/02/03 como um grupo e RNF-10 como outro); Should = 5; Could = 4; Won't = 5 grupos.

---

## 11. Escopo

### 11.1 Dentro do escopo

- Ano fiscal de 2026 (cálculo real).
- Pessoa Física/autônomo: IRPF mensal e INSS (planos normal e simplificado); deduções suportadas: contribuição previdenciária e desconto simplificado.
- MEI comum: três categorias tributárias (Comércio/Indústria, Serviços, Comércio e Serviços).
- Simples Nacional para prestação de serviços, Anexos III e V, com as nove atividades validadas sujeitas ao Fator R: desenvolvimento de software, consultoria, engenharia, arquitetura, medicina, odontologia, psicologia, fisioterapia e academias.
- Fator R e RBT12/RBT12p (empresa nova e madura).
- Pró-labore de sócio único.
- Dividendos no escopo validado: IRRF mensal, limite sem escrituração, modo com escrituração contábil informada pelo usuário.
- Comparador PF × PJ.
- Interface web com formulários, validação e resultados.
- Linha do tempo educacional da Reforma 2026–2033 (estrutura).

### 11.2 Fora do escopo

- Lucro Presumido e Lucro Real.
- Cálculo completo de 2027–2033 e IBS/CBS detalhado.
- Banco de dados e histórico de simulações.
- Autenticação/login.
- Exportação para PDF.
- APIs governamentais.
- Atualização legal automática.
- Inteligência artificial no produto.
- Aplicativo mobile.
- Consultoria personalizada.
- Casos tributários específicos registrados como fora do MVP (dependentes, pensão alimentícia, Livro Caixa, rendimentos do exterior, MEI Caminhoneiro, Simples Anexos I/II/IV, tributação anual integral de altas rendas, entre outros — ver seção 34).

---

## 12. Termo de Abertura do Projeto (TAP)

| Item | Conteúdo |
|---|---|
| Nome do projeto | Simulador Tributário Brasileiro 2026–2033 |
| Justificativa | A complexidade e a mutabilidade das regras tributárias dificultam a compreensão, por não especialistas, do impacto aproximado de cada estrutura (PF, MEI, Simples). Um simulador educacional rastreável contribui para o ensino e a alfabetização tributária. |
| Objetivo | Entregar um sistema web educacional com motor tributário real para 2026, comparador PF × PJ e estrutura educacional da Reforma 2026–2033 (seção 5). |
| Entregáveis | (1) Sistema web funcional; (2) catálogo de regras e pesquisa tributária validada; (3) `rules.json` versionado; (4) suíte de testes e relatório de cobertura; (5) documentação técnica e de qualidade; (6) este relatório acadêmico. |
| Escopo de alto nível | Conforme seção 11. |
| Restrições | Prazo acadêmico (horizonte de 4–6 semanas); apenas fontes oficiais como base normativa; sem orçamento financeiro dedicado; sem banco de dados, login ou APIs externas; ferramenta estritamente educacional. |
| Premissas | Disponibilidade das fontes oficiais; estabilidade das regras de 2026 durante o projeto; usuário informa dados corretos; escopo de cenários limitado ao que foi validado. |
| Riscos iniciais | Mudança normativa; interpretação incompleta de regras; combinação de casos do Simples; expectativa de que o sistema cubra Lucro Presumido/Real; prazo curto (registro completo na seção 28). |
| Critérios de sucesso | TR-001 a TR-011 implementadas e testadas; quatro módulos funcionais no navegador; cobertura ≥ 80%; nenhuma lógica fiscal na interface; nenhuma recomendação de regime; documentação completa entregue. |
| Responsável | Gestão do projeto — [Inserir integrantes] |
| Aprovação | Conforme processo acadêmico da disciplina |

---

## 13. Estudo de viabilidade

### 13.1 Viabilidade técnica

O projeto é tecnicamente viável com tecnologias maduras, gratuitas e de baixo acoplamento, o que a implementação comprovou:

- **Python e Flask:** aplicação web monolítica simples; apenas Flask como dependência de execução (`requirements.txt` contém Flask e pytest).
- **HTML/CSS/JavaScript puros:** sem *framework* de front-end; o JavaScript limita-se a comportamento de interface.
- **`Decimal`:** aritmética decimal exata nos valores monetários e fiscais, sem `float`.
- **JSON versionado:** parâmetros fiscais por ano, separados do código e carregados com conversão explícita e estrita.
- **Testes automatizados:** 432 testes e 98% de cobertura sustentam a correção e a manutenção.
- **Arquitetura modular:** motor independente de Flask, modelos imutáveis e enums fechados.
- **Sem dependência externa em tempo de execução para o cálculo:** o motor só lê arquivos JSON locais.

### 13.2 Viabilidade operacional

- **Uso via navegador**, sem instalação para o usuário final.
- **Formulários guiados** com rótulos, dicas e mensagens de erro por campo; aceitam valores em formato brasileiro (ex.: `8.000,50`).
- **Resultados imediatos**, com explicações e avisos.
- **Sem necessidade de treinamento técnico avançado**: a interface não expõe tabelas nem alíquotas; usa rótulos amigáveis.
- **Limitações e aviso educacional** presentes em todas as páginas ("Ferramenta educacional. Não substitui orientação contábil ou jurídica.") e reforçados na tela de resultado.
- **Limitação operacional:** a operação de uma versão pública exigiria hospedagem e rotina de atualização anual das regras (seções 13.4, 29 e 30).

### 13.3 Viabilidade legal

Esta seção **não constitui parecer jurídico**.

- **Natureza educacional:** o sistema apresenta estimativas e não presta consultoria tributária.
- **Fontes normativas:** a correção depende de manter as regras vinculadas a fontes oficiais registradas (`docs/research/fontes-tributarias.md`). Há pendências documentais residuais, registradas e não bloqueantes (por exemplo, a releitura integral do art. 145 da Resolução CGSN nº 140/2018).
- **Risco de desatualização legal:** a legislação muda; um resultado calculado com regras de um ano não vale para outro sem nova validação.
- **Não substituição de profissional:** cada resultado traz aviso nesse sentido.
- **Privacidade/LGPD:** o MVP não possui conta, banco nem histórico, e processa os dados informados apenas durante a requisição; ver seção 31.

### 13.4 Viabilidade econômica

**Verificação prévia:** a documentação existente do projeto **não** contém custos, benefícios, taxa de desconto ou qualquer estimativa econômica. Portanto, o que segue é um **CENÁRIO ACADÊMICO ESTIMATIVO — hipótese de viabilidade —, e não custo real já incorrido, receita real ou previsão comercial**. Os mesmos números são usados em VPL, TIR, payback, custos e reservas (seções 13.4, 21 e 22).

**Hipóteses do cenário**

| Parâmetro | Valor | Observação |
|---|---|---|
| Investimento inicial (I₀) | R$ 18.400,00 | Esforço de 240 h a R$ 60,00/h (R$ 14.400,00) + custos indiretos (R$ 1.600,00) + reserva de contingência de 10% (R$ 1.600,00) + reserva gerencial de 5% (R$ 800,00) — detalhado na seção 21 |
| Custo operacional anual | R$ 3.060,00 | Hospedagem R$ 600,00 + domínio R$ 60,00 + manutenção/atualização anual das regras (40 h × R$ 60,00 = R$ 2.400,00) |
| Benefício anual hipotético | R$ 9.600,00 | 40 assinantes institucionais/individuais × R$ 20,00/mês × 12; **hipótese de adoção**, sem pesquisa de mercado |
| Fluxo de caixa líquido anual | R$ 6.540,00 | R$ 9.600,00 − R$ 3.060,00 |
| Horizonte | 5 anos | Vida útil hipotética sob manutenção anual das regras |
| Taxa mínima de atratividade (TMA) | 12% ao ano | Hipótese de planejamento |

**Fórmulas**

- VPL = −I₀ + Σₜ₌₁ⁿ [ FCₜ / (1 + i)ᵗ ]
- TIR: taxa *r* tal que VPL(*r*) = 0
- Payback simples = I₀ / FC (fluxo constante)
- Payback descontado: primeiro instante em que o fluxo descontado acumulado se torna não negativo

**Resultados** (FC = R$ 6.540,00; n = 5; i = 12%; fator de valor presente da anuidade = 3,604776)

| Ano | Fluxo descontado (R$) | Acumulado (R$) |
|---|---|---|
| 0 | −18.400,00 | −18.400,00 |
| 1 | 5.839,29 | −12.560,71 |
| 2 | 5.213,65 | −7.347,07 |
| 3 | 4.655,04 | −2.692,02 |
| 4 | 4.156,29 | 1.464,26 |
| 5 | 3.710,97 | 5.175,24 |

| Indicador | Resultado |
|---|---|
| **VPL** | **R$ 5.175,24** (positivo) |
| **TIR** | **≈ 22,8% ao ano** (> TMA de 12%) |
| **Payback simples** | ≈ 2,81 anos |
| **Payback descontado** | ≈ 3,65 anos |

**Sensibilidade.** O VPL é sensível à hipótese de benefício: com benefício anual de R$ 7.000,00 o VPL seria ≈ −R$ 4.197,00; o ponto de equilíbrio (VPL = 0) ocorre com benefício anual de ≈ R$ 8.164,00 (cerca de 34 assinantes a R$ 20,00/mês). Isso mostra que o resultado positivo não é garantido e depende da adoção.

**Limitações da estimativa.** (i) O valor-hora, as horas e o preço da assinatura são hipóteses de planejamento; (ii) o projeto acadêmico não tem orçamento nem receita; (iii) não há pesquisa de mercado, tributação sobre a receita hipotética nem custo de captação de usuários; (iv) o custo de manutenção legislativa pode ser subestimado, dada a frequência de mudanças normativas; (v) o objetivo declarado do trabalho é educacional, não lucrativo. O cálculo serve para exercitar a análise de viabilidade, não para prever resultado financeiro.

---

## 14. Arquitetura da solução

### 14.1 Visão geral

Aplicação web **monolítica modular** (não há microserviços), executada em um único processo Flask, organizada em camadas com dependência apenas no sentido descendente:

```
Navegador (HTML / CSS / JavaScript)
        ↓  GET /simulacao/... , POST /resultado
Rotas Flask (app.py)
        ↓
Serviços e adaptadores (src/services)
        ↓
Motor tributário (src/tax_engine)
        ↓
Carga de regras (src/tax_rules)
        ↓
Dados por ano (data/tax_rules/<ano>/rules.json)
```

### 14.2 Responsabilidades

| Camada | Arquivos principais | Responsabilidade |
|---|---|---|
| Interface | `templates/`, `static/css/style.css`, `static/js/app.js` | Formulários e resultados; o JavaScript apenas mostra/oculta campos, valida formato e gerencia o menu e a linha do tempo. Nenhuma regra fiscal. |
| Rotas | `app.py` | Define as rotas, filtros de apresentação e o `POST /resultado`; devolve erros de formulário (422) sem expor falhas. |
| Serviços/adaptadores | `src/services/simulation_input_adapter.py`, `simulation_service.py`, `presentation.py` | Converte strings de formulário em modelos (`parse_brl_input`, `Decimal`); orquestra o motor; formata moeda/percentuais e rótulos. Não contém fórmula. |
| Modelos | `src/models/tax.py` | Dataclasses imutáveis de entrada e resultado, enums (planos, categorias, atividades, anexos, status) e validações. |
| Motor tributário | `src/tax_engine/` (`pf_2026.py`, `mei_2026.py`, `simples_2026.py`, `prolabore_2026.py`, `dividendos_2026.py`, `comparator_2026.py`, `calculator.py`) | Fórmulas dos módulos, independentes de Flask; leem parâmetros do JSON via `get_rule`. |
| Regras | `src/tax_rules/` (`rule_loader.py`, `decimal_utils.py`, `exceptions.py`) | Carrega e valida o arquivo de regras por ano; obtém regra por ID; converte decimais de forma estrita; recusa regra cujo status não autoriza cálculo. |
| Dados | `data/tax_rules/2026…2033/rules.json` | Parâmetros fiscais, fontes e status por regra. 2026 contém TR-001 a TR-011; 2027–2033 estão vazios. |

### 14.3 Versionamento de regras

Cada `rules.json` tem `schema_version`, `ano` e uma lista `regras`; cada regra tem `id` (TR-xxx), `nome`, `ano`, `status`, vigência, `fontes` e `parametros` (números decimais como *strings*). O ciclo de status é `PENDENTE → PESQUISADA → VALIDADA → IMPLEMENTADA → TESTADA`: somente regras implementadas e testadas produzem resultado fiscal. Um ano sem regras (2027–2033) resulta em estado pendente, sem número algum.

### 14.4 Fluxo de uma simulação

1. O navegador envia `POST /resultado` com `tipo_simulacao` (pf, mei, simples ou comparar).
2. O adaptador valida formato, converte para `Decimal`/`int`/enum e monta o modelo de entrada (erros por campo devolvem o formulário com a mensagem).
3. O serviço chama o motor, que consulta as regras (TR-xxx) no JSON do ano.
4. O resultado (`SimulationResult` ou `ComparatorResult`) é renderizado com formatação apenas visual; estados não suportados ou incompatíveis mostram mensagem e nenhum valor.

### 14.5 Decisões de projeto relevantes

- **Sem banco, sessão ou login**: o resultado é calculado e exibido na própria requisição.
- **Valores pendentes são `None`, nunca zero.**
- **Política de arredondamento fiscal em aberto** (pendência técnica documentada): o motor preserva `Decimal` exato; a tela arredonda só a exibição.
- **Comparador por composição**: reutiliza os motores PF, Simples, pró-labore e dividendos, sem duplicar cálculo.

---

## 15. Estrutura Analítica do Projeto — EAP/WBS

| Nível 1 | Nível 2 | Entregável / evidência |
|---|---|---|
| **1. Gestão e iniciação** | 1.1 Termo de abertura e escopo | TAP; `moscow.md` |
| | 1.2 Requisitos e fluxo do usuário | `requirements.md`, `user-flow.md` |
| | 1.3 Planos (riscos, comunicação, qualidade) | Seções 23–30 deste relatório |
| | 1.4 Controle por fases e *pull requests* | PR #1 e PR #2 |
| **2. Pesquisa tributária** | 2.1 Catálogo, matriz e fontes | `tax-rule-catalog.md`, `tax-rule-matrix.md`, `fontes-tributarias.md` |
| | 2.2 PF/autônomo (TR-001, TR-002) | `pf-2026-research.md` |
| | 2.3 MEI (TR-003, TR-004) | `mei-2026-research.md` |
| | 2.4 Simples e Fator R (TR-005 a TR-009) | `simples-2026-research.md` |
| | 2.5 Pró-labore e dividendos (TR-010, TR-011) | `pj-comparator-2026-research.md` |
| | 2.6 Validação independente | Seções de revisão nos documentos de pesquisa |
| **3. Arquitetura** | 3.1 Camadas e contratos | `tax-engine-architecture.md` |
| | 3.2 Modelos imutáveis e enums | `src/models/tax.py` |
| | 3.3 Carga de regras e `Decimal` estrito | `src/tax_rules/` |
| | 3.4 Esquema de regras por ano | `data/tax_rules/` |
| **4. Motor tributário 2026** | 4.1 PF (TR-001/002) | `pf_2026.py` |
| | 4.2 MEI (TR-003/004) | `mei_2026.py` |
| | 4.3 Simples: RBT12/RBT12p, limites, Fator R, anexos (TR-005..009) | `simples_2026.py` |
| | 4.4 Pró-labore (TR-010) | `prolabore_2026.py` |
| | 4.5 Dividendos (TR-011) | `dividendos_2026.py` |
| | 4.6 Comparador PF × PJ | `comparator_2026.py` |
| | 4.7 Despacho de cenários | `calculator.py` |
| **5. Interface web** | 5.1 Esqueleto da interface | Fase inicial (`5fc4bf9`) |
| | 5.2 Adaptador de entrada e parser BRL | `simulation_input_adapter.py` |
| | 5.3 Formulários e macros | `templates/` |
| | 5.4 Resultados e apresentação | `result.html`, `presentation.py` |
| | 5.5 Linha do tempo da Reforma (estrutura) | `reform.html`, `app.js` |
| **6. Qualidade** | 6.1 Testes por módulo | `tests/test_*_2026.py` |
| | 6.2 Integração frontend/backend | `test_frontend_integration.py` |
| | 6.3 *Hardening* e entradas hostis | Fase final de testes |
| | 6.4 Cobertura | `testing-and-quality.md` |
| | 6.5 Revisão de acessibilidade e responsividade | Seção 23 |
| **7. Documentação** | 7.1 Documentação de pesquisa | `docs/research/` |
| | 7.2 Documentação de projeto e qualidade | `docs/project/` |
| | 7.3 Relatório acadêmico | Este documento |
| **8. Entrega** | 8.1 Integração na `main` | Merge do PR #2 |
| | 8.2 Branch de entrega final | `feat/final-delivery` |
| | 8.3 Revisão final | Conferência do relatório e da inspeção visual manual |

---

## 16. Sequenciamento das atividades

As durações abaixo constituem a **baseline acadêmica de planejamento** (em semanas, horizonte de 6 semanas). **Não** são a duração real comprovada pelo Git: os commits disponíveis estão concentrados em 29 e 30/09/2026 (ver seção 17), e nenhum esforço real foi medido.

| ID | Atividade | Duração planejada |
|---|---|---|
| A1 | Iniciação e escopo (TAP, MoSCoW) | 0,5 sem. |
| A2 | Levantamento de requisitos e fluxo do usuário | 0,5 sem. |
| A3 | Pesquisa tributária e validação (TR-001..TR-011) | 1,5 sem. |
| A4 | Arquitetura e fundação do motor | 0,5 sem. |
| A5 | Motor tributário 2026 (PF, MEI, Simples, pró-labore/dividendos, comparador) | 1,5 sem. |
| A6 | Interface web integrada | 1,0 sem. |
| A7 | Testes finais e *hardening* | 0,5 sem. |
| A8 | Documentação acadêmica final | 0,5 sem. |
| A9 | Entrega final (integração e revisão) | marco (0 sem.) |

Os testes por módulo são escritos junto com cada implementação (A5, A6); A7 concentra a revisão adversarial, a cobertura e a medição final.

---

## 17. Marcos do projeto

As datas vêm do `git log` (data do commit); onde o marco agrupa várias etapas, cita-se o intervalo.

| Marco | Descrição | Data (git) | Evidência |
|---|---|---|---|
| M1 | Escopo definido | 2026-09-29 | `939db10` docs: define MVP scope and requirements |
| M2 | Pesquisa tributária validada (TR-001..TR-011) | 2026-09-29 a 2026-09-30 | `1c38f4d`, `3af4fad` (PF, MEI); `04a1f8b`, `7a8130e` (Simples, pró-labore/dividendos); PR #1 `03f9748` |
| M3 | Fundação do motor | 2026-09-30 | `dbfe3a7` |
| M4 | PF (TR-001/002) | 2026-09-30 | `28f8867` |
| M5 | MEI (TR-003/004) | 2026-09-30 | `51f206e` |
| M6 | Simples Nacional (TR-005..009) | 2026-09-30 | `72354d2` |
| M7 | Pró-labore, dividendos e comparador (TR-010/011) | 2026-09-30 | `eec8aa3` |
| M8 | Interface integrada ao motor | 2026-09-30 | `6d55116` |
| M9 | *Hardening* concluído e PR #2 integrado | 2026-09-30 | `1ff048b`; merge `1f28c60` |
| M10 | Entrega final (relatório acadêmico e revisão final) | em elaboração nesta fase | Branch `feat/final-delivery` |

Observação: os commits disponíveis no repositório estão concentrados em 29 e 30/09/2026 (22 commits). O cronograma da seção 19 é a **baseline acadêmica de planejamento** de 6 semanas, e não a medição do tempo real gasto.

---

## 18. PDM — diagrama de precedências

Relações *Finish-to-Start* (FS), salvo indicação de *Start-to-Start* (SS).

| ID | Atividade | Predecessora | Relação | Justificativa |
|---|---|---|---|---|
| A1 | Iniciação e escopo | — | — | Ponto de partida |
| A2 | Requisitos | A1 | FS | Requisitos dependem do escopo aprovado |
| A3 | Pesquisa tributária | A2 | FS | A pesquisa é guiada pelos requisitos e módulos definidos |
| A4 | Arquitetura e fundação | A3 | FS | O contrato de regras (status, parâmetros, fontes) deriva do catálogo pesquisado |
| A5 | Motor tributário 2026 | A4 | FS | O motor usa o contrato de regras e as regras validadas (A3) |
| A6 | Interface integrada | A5 | FS | A interface exibe resultados dos motores |
| A7 | Testes finais e *hardening* | A6 | FS | Revisão adversarial exige o fluxo completo |
| A8 | Documentação acadêmica | A6 | SS (com A7) | Pode iniciar quando o sistema está funcional, em paralelo à revisão final |
| A9 | Entrega final | A7, A8 | FS | Só se entrega com testes e documentação concluídos |

```
A1 → A2 → A3 → A4 → A5 → A6 ─┬→ A7 ─┬→ A9
                              └→ A8 ─┘
```

---

## 19. Cronograma / Gantt (baseline acadêmica de planejamento — 6 semanas)

Baseline de planejamento; não representa a duração real comprovada pelo Git (ver seção 17).

■ = semana com atividade.

| Atividade | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| A1 Iniciação e escopo | ■ | | | | | |
| A2 Requisitos | ■ | | | | | |
| A3 Pesquisa tributária e validação | | ■ | ■ | | | |
| A4 Arquitetura e fundação | | | ■ | | | |
| A5 Motor tributário 2026 | | | | ■ | ■ | |
| A6 Interface web integrada | | | | | ■ | ■ |
| A7 Testes finais e *hardening* | | | | | | ■ |
| A8 Documentação acadêmica | | | | | | ■ |
| A9 Entrega final | | | | | | ■ |
| Testes por módulo (contínuo) | | | | ■ | ■ | ■ |
| Documentação de pesquisa (contínua) | | ■ | ■ | | | |

Marcos planejados: M1–M2 (fim de S1–S3), M3 (fim de S3), M4–M7 (S4–S5), M8 (S5–S6), M9 (S6), M10 (fim de S6).

---

## 20. Caminho crítico

**Caminho crítico (duração planejada de 6,0 semanas):**

A1 (0,5) → A2 (0,5) → A3 (1,5) → A4 (0,5) → A5 (1,5) → A6 (1,0) → A7 (0,5) → A9

- **A8 (documentação)** corre em paralelo a A7 e tem a mesma duração, portanto folga zero: também é crítica para o marco final.
- Não há folga nas demais atividades, pois formam uma cadeia sequencial (um mesmo grupo executa as atividades em série).

**Impacto de atrasos.** Um atraso em qualquer atividade da cadeia desloca diretamente a data final:

- **A3 (pesquisa)** é a mais sensível: sem regra validada, o motor não pode produzir número (princípio "sem fonte, sem regra"). Foi o risco R1 já identificado na especificação do MVP.
- **A5 (motor)** é a atividade de maior esforço; o Simples/Fator R concentra a complexidade.
- **A6 e A7** dependem de A5; um atraso reduz o tempo de testes e de *hardening*.
- Mitigação planejada: cortar itens Should/Could primeiro (ordem já prevista na especificação), preservando o núcleo Must.

---

## 21. Estimativa de custos

**Cenário acadêmico estimativo (hipótese).** Não há custo real registrado; os valores abaixo reaproveitam exatamente o cenário da seção 13.4 e **não representam despesa efetivamente realizada**.

### 21.1 Investimento inicial

| Recurso | Tipo | Quantidade | Valor unitário (R$) | Custo (R$) |
|---|---|---|---|---|
| Gestão e documentação | Direto (mão de obra) | 40 h | 60,00 | 2.400,00 |
| Pesquisa e análise tributária | Direto (mão de obra) | 60 h | 60,00 | 3.600,00 |
| Desenvolvimento | Direto (mão de obra) | 100 h | 60,00 | 6.000,00 |
| Testes e qualidade (QA) | Direto (mão de obra) | 40 h | 60,00 | 2.400,00 |
| Software (Python, Flask, pytest, coverage, Git/GitHub — código aberto/gratuito) | Direto | 1 | 0,00 | 0,00 |
| **Subtotal custos diretos** | | | | **14.400,00** |
| Estação de trabalho (depreciação no período) | Indireto | 1 | 1.000,00 | 1.000,00 |
| Internet e energia (≈ 1,5 mês) | Indireto | 1,5 mês | 400,00 | 600,00 |
| **Subtotal custos indiretos** | | | | **1.600,00** |
| **Custos diretos + indiretos** | | | | **16.000,00** |
| Reserva de contingência (10% de 16.000) | Reserva | — | — | 1.600,00 |
| Reserva gerencial (5% de 16.000) | Reserva | — | — | 800,00 |
| **Investimento inicial total (I₀)** | | | | **18.400,00** |

### 21.2 Custo operacional anual (implantação futura hipotética)

| Item | Tipo | Quantidade | Valor unitário (R$) | Custo anual (R$) |
|---|---|---|---|---|
| Hospedagem | Direto | 12 meses | 50,00 | 600,00 |
| Domínio | Direto | 1 ano | 60,00 | 60,00 |
| Manutenção e atualização anual das regras | Direto (mão de obra) | 40 h | 60,00 | 2.400,00 |
| **Total anual** | | | | **3.060,00** |

---

## 22. Reservas

- **Reserva de contingência (10% — R$ 1.600,00):** destinada a **riscos conhecidos e identificados** no registro de riscos (seção 28), como retrabalho de regra por interpretação normativa, ajustes de interface e correção de defeitos. É acionada quando um risco do registro se materializa.
- **Reserva gerencial (5% — R$ 800,00):** destinada a **incertezas não previstas** ("desconhecidos desconhecidos"), sob decisão da gestão do projeto.

Os percentuais são **hipóteses de planejamento** (práticas usuais de gestão de projetos), adotadas para o cenário acadêmico e sem pretensão de serem valores reais.

---

## 23. Gestão da qualidade

**Política de qualidade:** o sistema só produz número quando a regra tributária correspondente foi pesquisada, validada contra fonte oficial, implementada e testada; nenhum resultado é exibido em cenário não suportado.

**Evidências reais (Fase final de testes):**

- **432 testes automatizados**, todos aprovados;
- **98% de cobertura de linhas** (`src` + `app.py`), contra a meta exigida de **≥ 80%**. A cobertura mede linhas, não ramos, e não é de 100%.

| Grupo | Cobertura |
|---|---|
| Motor tributário (`src/tax_engine`) | ≈ 99,5% |
| Regras (`src/tax_rules`) | ≈ 93% |
| Serviços (`src/services`) | ≈ 99% |
| Modelos (`src/models`) | 98% |
| `app.py` | 97% |
| **Total** | **98%** |

**Tipos de verificação:** testes unitários dos motores; testes de integração do fluxo HTTP; testes de fronteira; entradas hostis/extremas; regressão; auditoria de camadas; segurança de saída; verificação de responsividade e acessibilidade básica. O detalhamento está em `docs/project/testing-and-quality.md`.

**Verificação de layout a 360 px:** medição programática, sem *framework* de automação, em 15 páginas (GET e respostas de POST); nenhuma apresentou rolagem horizontal. **Essa medição não avalia estética; a inspeção visual manual em 360 px permanece pendente para a revisão final.**

---

## 24. Garantia da Qualidade (QA) e Controle da Qualidade (QC)

**QA — Garantia da Qualidade (processo preventivo):**

- desenvolvimento em fases curtas, com revisão e aprovação ao final de cada fase;
- integração por *pull requests* com histórico de commits legível;
- **pesquisa e validação normativa antes da implementação** (catálogo de regras e matriz de status);
- rastreabilidade entre regra, fonte, código e teste (seção 32);
- **separação de camadas**, com auditoria automática de que a interface não contém regra fiscal;
- decisões de escopo registradas (premissas de cálculo, limitações do MVP);
- revisão de código/diffs a cada fase.

**QC — Controle da Qualidade (verificação do produto):**

- execução da suíte com `pytest` (432 testes);
- medição de cobertura com `coverage` (98%);
- testes de fronteira (limites de faixas, MEI, Fator R, sublimites, R$ 50 mil, altas rendas);
- integração HTTP (`POST /resultado` nos quatro módulos);
- entradas adversariais (vazio, `NaN`, `Infinity`, negativos, números enormes, HTML, enums inválidos, histórico faltante/extra);
- revisão de interface (rótulos, mensagens de erro, rolagem horizontal em 360 px).

---

## 25. Estratégia de testes

| Nível | Conteúdo | Arquivos |
|---|---|---|
| Infraestrutura | Esquema do `rules.json`, carga por ano, `Decimal` estrito, modelos imutáveis, IDs únicos e status | `test_rule_loader.py`, `test_tax_models.py` |
| Unitário dos motores | PF, MEI, Simples, pró-labore, dividendos; exemplos oficiais da Receita em testes `test_irpf_official_example_*` | `test_pf_2026.py`, `test_mei_2026.py`, `test_simples_2026.py`, `test_prolabore_dividendos_2026.py` |
| Composição | Comparador PF × PJ reaproveitando os motores; ausência de veredito | `test_comparator_2026.py` |
| Integração | Rotas, formulários, `POST /resultado`, parser de moeda, histórico do Simples | `test_routes.py`, `test_frontend_integration.py` |
| Fronteiras | Limites de faixa e de corte de cada regra | Nos arquivos de cada motor |
| Robustez | Entradas hostis em todos os campos dos quatro formulários, sem erro 500 | `test_frontend_integration.py` |
| Camadas e segurança | Ausência de parâmetros fiscais na interface; *autoescaping*; sem `|safe` | `test_frontend_integration.py` |
| Regressão | Execução integral a cada fase; invariantes (total = soma; líquido = bruto − tributos) | Suíte completa |

Fronteiras cobertas (exemplos): IRPF R$ 5.000,00 / 5.000,01 e 7.350,00 / 7.350,01; MEI R$ 81.000,00 / 81.000,01 e 97.200,00 / 97.200,01; Fator R 0,27 / 0,28 / 0,29; Simples R$ 3.600.000,00 / 3.600.000,01 e 4.800.000,00 / 4.800.000,01; dividendos R$ 50.000,00 / 50.000,01; altas rendas R$ 600.000,00 / 600.000,01.

---

## 26. Matriz RACI

R = Responsável (executa); A = Aprovador (presta contas; um por atividade); C = Consultado; I = Informado. Os papéis são funções do projeto; uma mesma pessoa pode acumular mais de um papel.

| Atividade | Gestão | Análise tributária | Desenvolvimento | QA | Orientação acadêmica |
|---|---|---|---|---|---|
| A1 Iniciação e escopo (TAP) | R | C | C | I | A |
| A2 Requisitos | A/R | C | C | C | I |
| A3 Pesquisa tributária e validação | I | A/R | C | C | C |
| A4 Arquitetura e fundação | C | C | A/R | C | I |
| A5 Motor tributário 2026 | I | C | A/R | C | I |
| A6 Interface web | I | C | A/R | C | I |
| A7 Testes e *hardening* | I | C | R | A/R | I |
| A8 Documentação acadêmica | A/R | C | C | C | I |
| A9 Entrega final | R | I | R | R | A |

---

## 27. Plano de comunicação

Plano **proposto** (não registra reuniões efetivamente realizadas).

| Informação | Destinatário | Canal | Periodicidade | Responsável |
|---|---|---|---|---|
| Status do projeto (fases concluídas, próximos passos) | Orientação acadêmica e equipe | Relatório curto/reunião | Semanal | Gestão |
| Riscos novos ou alterados | Equipe e orientação | Registro de riscos atualizado | Quinzenal ou sob evento | Gestão |
| Mudanças de escopo | Equipe e orientação | Solicitação de mudança registrada em documento e PR | Sob demanda | Gestão |
| Resultados dos testes e da cobertura | Equipe e orientação | Saída do `pytest`/`coverage` e `testing-and-quality.md` | A cada fase | QA |
| Decisões e premissas tributárias | Equipe e orientação | Documentos de pesquisa e catálogo | A cada validação | Análise tributária |
| Entrega final | Orientação acadêmica | Repositório, relatório e apresentação | Única (fim do projeto) | Gestão |

---

## 28. Gestão de riscos

Escala: Probabilidade (P) e Impacto (I) de 1 (muito baixo) a 5 (muito alto); **Exposição = P × I**. Trata-se de **avaliação qualitativa de planejamento**, e não de probabilidade estatística.

| ID | Categoria | Descrição | P | I | P×I | Resposta | Mitigação | Contingência | Responsável |
|---|---|---|---|---|---|---|---|---|---|
| R01 | LEGISLAÇÃO/REGRA FISCAL | Mudança normativa ou interpretação diferente após a validação, tornando uma regra desatualizada ou incorreta | 4 | 5 | 20 | Mitigar | Fontes oficiais registradas; regras versionadas por ano; revisão anual do catálogo | Reabrir a regra (status volta a `PESQUISADA`) e corrigir `rules.json`/motor | Análise tributária |
| R02 | LEGISLAÇÃO/REGRA FISCAL | Pendências documentais residuais (ex.: releitura integral de artigo de resolução do CGSN) | 3 | 3 | 9 | Aceitar/Mitigar | Pendências registradas e não bloqueantes; revisão na auditoria documental final | Ajustar a documentação, sem mudança de valor | Análise tributária |
| R03 | ARQUITETURA | Acoplamento entre interface e regra fiscal, gerando inconsistência | 2 | 4 | 8 | Evitar | Camadas separadas; auditoria automática da interface; parâmetros só em JSON | Refatorar para a camada correta | Desenvolvimento |
| R04 | ARQUITETURA | Política de arredondamento do DAS/IRPF em aberto pode gerar diferenças de centavos em relação a ferramentas oficiais | 3 | 2 | 6 | Aceitar | Cálculo em `Decimal` exato; arredondamento só visual, documentado | Definir política com base em orientação oficial e ajustar testes | Desenvolvimento |
| R05 | API/INTEGRAÇÃO | **O MVP não depende de API externa em tempo de execução.** O risco refere-se a uma **futura** integração com APIs/fontes governamentais, que pode sofrer indisponibilidade, alteração contratual ou mudança de formato | 3 | 3 | 9 | Evitar (no MVP) / Mitigar (no futuro) | Manter o cálculo local; se houver integração futura, isolar em camada própria com *fallback* local | Desativar a integração e usar os dados versionados | Desenvolvimento |
| R06 | HUMANO | Dependência de poucas pessoas (conhecimento concentrado; indisponibilidade) | 3 | 4 | 12 | Mitigar | Documentação detalhada, catálogo de regras, testes, repositório versionado | Redistribuir atividades; reduzir escopo Should/Could | Gestão |
| R07 | HUMANO | Erro de interpretação tributária por não especialista | 3 | 4 | 12 | Mitigar | Validação independente; premissas explícitas; revisão da orientação acadêmica | Reabrir a regra e corrigir | Análise tributária |
| R08 | HUMANO | Uso do simulador como aconselhamento profissional pelo usuário | 3 | 4 | 12 | Mitigar | Aviso em todas as páginas e na tela de resultado; nenhuma recomendação de regime | Reforçar avisos; restringir uso a contexto educacional | Gestão |
| R09 | INFRAESTRUTURA | Indisponibilidade da hospedagem em uma implantação futura | 2 | 3 | 6 | Transferir/Mitigar | Escolha de provedor com SLA adequado; aplicação *stateless* e portável | Reimplantar em outro provedor a partir do repositório | Desenvolvimento |
| R10 | INFRAESTRUTURA | Incompatibilidade de ambiente (versão do Python ou de dependências) | 2 | 3 | 6 | Mitigar | `requirements.txt` com versões mínimas; suíte de testes reprodutível | Fixar versões e recriar o ambiente virtual | Desenvolvimento |
| R11 | QUALIDADE | Defeito não detectado em combinação rara de entrada | 3 | 4 | 12 | Mitigar | 432 testes, fronteiras e entradas hostis; cobertura de 98% | Correção priorizada; novo teste de regressão | QA |
| R12 | QUALIDADE | Sensação de conformidade total a partir da cobertura alta (cobertura mede linhas, não correção normativa) | 2 | 3 | 6 | Mitigar | Testes derivados de valores das fontes oficiais; validação normativa separada | Revisão por profissional da área | QA |
| R13 | PRAZO | Complexidade do Simples/Fator R superior ao planejado | 3 | 4 | 12 | Mitigar | Escopo restrito a serviços, Anexos III/V e nove atividades; corte de Should/Could | Acionar a reserva de contingência; reduzir escopo | Gestão |
| R14 | PRAZO | Expectativa de cobertura de Lucro Presumido/Real ou de 2027+ | 2 | 3 | 6 | Evitar | Escopo explícito; itens rotulados como "em breve"/fora do escopo | Comunicar limitações na interface e no relatório | Gestão |

---

## 29. Aquisições (procurement)

**Cenário real do MVP:** o sistema usa majoritariamente software de código aberto ou gratuito (Python, Flask, pytest, coverage, Git/GitHub). Não há aquisição externa obrigatória para o motor local, e nenhum contrato foi firmado.

**Possíveis aquisições em uma implantação futura (hipotéticas):**

| Item | Finalidade |
|---|---|
| Hospedagem | Disponibilizar o sistema na internet |
| Domínio | Endereço público |
| Serviços de monitoramento | Acompanhar disponibilidade e erros |
| Fonte de dados/API (eventual) | Apoio à atualização normativa, se vier a ser adotada |

**Critérios de seleção:**

| Critério | Consideração |
|---|---|
| Custo | Compatível com o orçamento hipotético (seção 21) |
| Disponibilidade | Histórico e garantia de funcionamento do provedor |
| Suporte | Canais e prazos de atendimento |
| Segurança | Criptografia em trânsito (HTTPS), atualizações de segurança |
| SLA | Compromissos formais de disponibilidade |
| Portabilidade | Evitar dependência exclusiva (aplicação simples, sem banco) |

---

## 30. SLA e operação

**Não existe SLA contratual hoje**: o sistema é um projeto acadêmico executado localmente. A tabela a seguir é um **SLA-alvo** de planejamento para uma eventual operação em produção, com valores moderados e justificados.

| Item | Alvo proposto | Justificativa |
|---|---|---|
| Disponibilidade | 99,0% ao mês (≈ 7 h de indisponibilidade/mês) | Hospedagem simples e aplicação sem estado; ferramenta educacional, não crítica |
| Tempo de resposta | p95 < 1 s por simulação | Compatível com o RNF-14: cálculo local, sem I/O externo |
| Recuperação (RTO) | ≤ 4 h | Reimplantação a partir do repositório versionado |
| Perda de dados (RPO) | Não aplicável | O sistema não persiste dados; o código e as regras estão no Git |
| *Backup* | Repositório Git com cópia remota | Única "fonte de dados" relevante é o código/JSON |
| Suporte | Resposta em até 2 dias úteis (horário comercial) | Projeto de pequena equipe |
| Atualização normativa | Revisão anual das regras antes do início do ano-calendário | Regras dependem do ano |
| Janela de manutenção | Fora do horário de pico, com aviso prévio | Boa prática de operação |

---

## 31. Segurança, privacidade e LGPD

**Estado atual do MVP.**

- Não há conta de usuário, banco de dados nem histórico de simulações.
- Os valores informados são processados **na requisição** e exibidos na resposta; não são gravados pela aplicação. Nenhuma sessão é usada.
- Como qualquer servidor web, o ambiente de hospedagem pode registrar metadados técnicos de acesso (por exemplo, endereço IP e rota); isso deve ser considerado em uma implantação futura.
- Os dados financeiros informados são pessoais, embora não estejam no rol de dados pessoais sensíveis do art. 5º, II, da LGPD; merecem cuidado de qualquer forma. Esta seção não é parecer jurídico.

Com isso, o MVP **minimiza a persistência** de dados pessoais. Ainda assim, uma implantação futura deve considerar:

| Princípio/tema | Consideração |
|---|---|
| Finalidade | Declarar que os dados servem apenas à simulação |
| Minimização | Coletar somente o necessário (já é a prática atual) |
| Transparência | Informar ao usuário o que é processado e se há *logs* |
| Retenção | Não reter dados; definir política de *logs* e prazo |
| Segurança | HTTPS, atualização de dependências, configuração segura do servidor |
| Direitos do titular | Canal para solicitações, caso se passe a armazenar dados |

**Segurança de saída e de entrada (implementado):** *autoescaping* do Jinja ativo e nenhum uso de `|safe`; valores digitados são escapados na saída; entradas inválidas são validadas no servidor e nunca geram erro 500 nos cenários testados; o parser de moeda rejeita texto arbitrário, `NaN`, `Infinity` e valores negativos.

---

## 32. Rastreabilidade dos requisitos

| Requisito | Implementação | Regra tributária | Teste | Status |
|---|---|---|---|---|
| RF-01 PF/autônomo | `src/tax_engine/pf_2026.py` | TR-001, TR-002 | `tests/test_pf_2026.py` | Concluído |
| RF-02 MEI | `src/tax_engine/mei_2026.py` | TR-003, TR-004 | `tests/test_mei_2026.py` | Concluído |
| RF-03 Simples | `src/tax_engine/simples_2026.py` | TR-005, TR-008 | `tests/test_simples_2026.py` | Concluído |
| RF-04 Fator R | `simples_2026.py` (`calculate_fator_r_2026`) | TR-009 | `tests/test_simples_2026.py` | Concluído |
| RF-05 Anexos III/V | `simples_2026.py` (`select_tax_bracket`) | TR-006, TR-007 | `tests/test_simples_2026.py` | Concluído |
| RF-06 Pró-labore | `src/tax_engine/prolabore_2026.py` | TR-010 (+ TR-001) | `tests/test_prolabore_dividendos_2026.py` | Concluído |
| RF-07 Dividendos | `src/tax_engine/dividendos_2026.py` | TR-011 | `tests/test_prolabore_dividendos_2026.py` | Concluído |
| RF-08 Comparador | `src/tax_engine/comparator_2026.py` | TR-010, TR-011 e TR-001..TR-009 | `tests/test_comparator_2026.py` | Concluído |
| RF-09 Explicações e avisos | `src/services/presentation.py`, `templates/result.html`, `templates/_macros.html` | TR-001..TR-011 (IDs exibidos) | `tests/test_frontend_integration.py` | Concluído |
| RF-10 Reforma 2026–2033 | `templates/reform.html`, `static/js/app.js` | — (sem regra fiscal) | `tests/test_routes.py` (rota 200) | **Parcial** (estrutura; conteúdo pendente) |
| RF-11 Validação de entradas | `src/services/simulation_input_adapter.py`; validações em `src/models/tax.py` | — | `tests/test_frontend_integration.py`, `tests/test_tax_models.py` | Concluído |
| RF-12 Resultados no navegador | `app.py`, `templates/`, `src/services/simulation_service.py` | — | `tests/test_frontend_integration.py`, `tests/test_routes.py` | Concluído |
| RF-13 Regras versionadas | `src/tax_rules/rule_loader.py`; `data/tax_rules/<ano>/rules.json` | TR-001..TR-011 | `tests/test_rule_loader.py` | Concluído |
| RF-14 Não suportado sem resultado parcial | Motores e `calculator.py` | TR-005 (limites), TR-011 | `tests/test_simples_2026.py`, `tests/test_comparator_2026.py`, `tests/test_frontend_integration.py` | Concluído |
| RNF-01 `Decimal` | `src/tax_rules/decimal_utils.py`; modelos | Todas | `tests/test_rule_loader.py`, testes de "sem float" nos motores | Concluído |
| RNF-03 Sem lógica fiscal na interface | `app.py`, `templates/`, `static/js/` | — | `tests/test_frontend_integration.py` (auditoria de camadas) | Concluído |
| RNF-10 Cobertura ≥ 80% | Suíte completa | — | `pytest` + `coverage` (98%); `docs/project/testing-and-quality.md` | Concluído |
| RNF-07/08 Responsividade e acessibilidade | `static/css/style.css`, `templates/_macros.html` | — | Testes de rótulos/âncoras; medição a 360 px | Concluído (inspeção visual manual pendente) |

Rastreabilidade normativa de cada TR-xxx (fontes oficiais, questões em aberto e validação): `docs/research/tax-rule-catalog.md`, `tax-rule-matrix.md` e `fontes-tributarias.md`.

---

## 33. Resultados alcançados

- **TR-001 a TR-011** pesquisadas, validadas, implementadas e testadas (status `TESTADA` em `rules.json`, sincronizado com a matriz e o catálogo).
- **Pessoa Física** funcional (IRPF mensal com redução de 2026; INSS planos normal e simplificado; tratamento de renda zero e abaixo do mínimo).
- **MEI** funcional (limite anual e proporcional; DAS fixo inclusive com receita zero).
- **Simples Nacional** funcional (RBT12/RBT12p, Fator R, Anexos III/V, limites e sublimite do MVP).
- **Pró-labore e dividendos** funcionais (INSS, IRPF, IRRF de dividendos, limite sem escrituração com a parcela de IRPJ do DAS).
- **Comparador PF × PJ** funcional, lado a lado, com diferenças numéricas e sem recomendação.
- **Frontend** funcional (formulários, `POST /resultado`, resultados explicados).
- **432 testes** e **98% de cobertura** (meta ≥ 80%).
- **Parser de moeda brasileira** com `Decimal` e **validação no servidor**.
- **Tratamento de entradas hostis**: nenhuma resposta 500 nos cenários adversariais testados.
- **Responsividade**: verificação de ausência de rolagem horizontal em 360 px em 15 páginas (sem avaliação estética completa).
- **Processo**: dois *pull requests* integrados; histórico de commits por fase; documentação de pesquisa, projeto e qualidade.

---

## 34. Limitações

- O **cálculo real está restrito ao ano de 2026**. **2027–2033 possuem apenas estrutura educacional**; não há motor fiscal para esses anos.
- O conteúdo educacional por ano da linha do tempo da Reforma (`/reforma`) está **pendente de validação** e exibido como tal.
- Cenários específicos fora do MVP: dependentes, pensão alimentícia e Livro Caixa no IRPF; rendimentos do exterior; MEI Caminhoneiro; Simples Anexos I, II e IV; múltiplas atividades e segregações de receita; ISS devido a outro município, retenção, exportação e substituição tributária; sócio com múltiplas fontes.
- Simples com RBT12/RBT12p acima do sublimite de R$ 3,6 milhões: cálculo integral **não suportado** (o sistema informa, sem valores).
- Tributação anual de altas rendas (art. 16-A): **fora do cálculo integral**; o sistema apenas avisa.
- Complementação previdenciária abaixo do salário mínimo: o sistema informa o mecanismo e considera o valor que alcança o mínimo; não calcula o ajuste individual.
- Sem atualização legislativa automática; a revisão das regras é manual e anual.
- Sem Lucro Presumido e Lucro Real.
- Sem persistência, autenticação ou exportação em PDF; sem integração com APIs governamentais.
- Funcionalidades da especificação inicial não entregues: gráficos comparativos, diferença anual no comparador, atalho MEI → Simples, preservação de dados entre telas, exibição de carga efetiva em percentual e seleção de ano na interface (que opera fixa em 2026).
- Política de arredondamento fiscal em aberto; a tela arredonda apenas a exibição.
- Pendências documentais residuais (ex.: releitura integral de artigo da Resolução CGSN nº 140/2018).
- A cobertura mede linhas e não garante correção normativa; a inspeção visual manual em 360 px está pendente.
- **Consistência documental:** `README.md` e partes de `docs/project/` (requisitos, arquitetura do motor, especificação) preservam textos de fases anteriores (por exemplo, "nenhum cálculo real implementado"). Este relatório descreve o estado final; recomenda-se atualizar esses documentos na revisão final.
- O sistema **não substitui** análise contábil ou jurídica profissional.

---

## 35. Roadmap

Todos os itens abaixo são **futuros** e **não fazem parte** do sistema entregue.

| Item futuro | Observação |
|---|---|
| Lucro Presumido | Novo módulo com pesquisa e validação próprias |
| Lucro Real | Módulo de maior complexidade |
| IBS/CBS detalhados | Conforme regulamentação da Reforma |
| Regras completas 2027–2033 | Um `rules.json` validado por ano |
| Histórico e banco de dados | Exige análise de LGPD |
| Exportação em PDF | Conveniência de uso |
| Autenticação | Dependente de histórico/banco |
| Integração com APIs governamentais | Com isolamento e *fallback* local |
| Atualização normativa assistida | Processo de revisão de regras |
| IA explicativa | Apoio didático, sem recomendação de regime |
| Aplicativo mobile | Ampliação de canal |
| Melhorias de UX previstas na especificação | Gráficos, diferença anual, atalhos entre simulações |

---

## 36. Conclusão

O projeto cumpriu o objetivo de entregar um simulador tributário educacional com motor real para 2026, apoiado em regras catalogadas, validadas contra fontes oficiais e verificadas por 432 testes automatizados, com 98% de cobertura de linhas. A arquitetura em camadas, o uso de `Decimal` e a separação entre fórmulas (código) e parâmetros (JSON por ano) atendem aos requisitos de rastreabilidade, auditabilidade e manutenção, e a interface web torna os cálculos acessíveis com explicações, avisos e tratamento de entradas inválidas.

O trabalho também delimita com clareza o que **não** foi feito: não há cálculo para 2027–2033, nem Lucro Presumido ou Real, nem persistência, autenticação, exportação ou integração com APIs; a linha do tempo da Reforma existe como estrutura, com conteúdo ainda pendente; e o sistema não substitui profissional nem recomenda regime. A análise de viabilidade econômica foi apresentada como cenário acadêmico hipotético, com seus limites explícitos.

Como próximos passos, recomendam-se: a inspeção visual manual em 360 px, a atualização dos documentos das fases iniciais (inclusive o `README`), a definição da política de arredondamento com base em orientação oficial e a escolha, pela equipe, dos itens do roadmap a serem priorizados.
