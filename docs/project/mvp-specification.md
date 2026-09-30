# Especificação Funcional do MVP

Simulador Tributário Brasileiro 2026–2033 · Fase 2 (documentação; sem código de cálculo)

> **Status posterior (MVP final):** especificação da Fase 2, preservada como histórico. Os módulos PF, MEI, Simples, pró-labore/dividendos e comparador foram implementados e testados para 2026 (432 testes; 98% de cobertura) e integrados à interface. Permanecem **não entregues** gráficos, diferença anual, atalho MEI → Simples, preservação de dados entre telas e o conteúdo por ano da linha do tempo da Reforma (estrutura entregue, conteúdo pendente). As referências a "hoje", "rotas vazias" e a estados pendentes descrevem a Fase 2. Estado final: [relatório acadêmico](../academic/relatorio-final.md).

Documentos relacionados: [requirements.md](requirements.md) · [moscow.md](moscow.md) · [user-flow.md](user-flow.md) · [fontes](../research/fontes-tributarias.md)

> **Regra de ouro:** nenhum valor fiscal é definido aqui. Tudo é `[REGRA PENDENTE DE VALIDAÇÃO]` até ter fonte oficial registrada.
> Aviso obrigatório: *Ferramenta educacional. Não substitui orientação contábil ou jurídica.*

## 1. Objetivo e escopo

Simulador educacional com cinco módulos: PF/Autônomo, MEI, Simples Nacional (serviços), Comparador PF x PJ e Timeline da Reforma 2026–2033.
Cálculos reais do MVP: **regras de 2026**. Arquitetura preparada para 2027–2033 (um `rules.json` por ano).
Fora do escopo: ver [moscow.md](moscow.md), seção "Won't have".

## 2. Telas

Convenções gerais: campos monetários em R$ com máscara opcional em JS (o servidor sempre revalida); erros por campo abaixo do input, em texto (não só cor); botão primário único por tela; mobile: coluna única, botões largura total, alvos ≥ 44 px.
Estado de resultado pendente (comum): cartão "Regras deste ano ainda pendentes de validação" sem nenhum número.

### T1. Home `/` (existe)
- **Objetivo:** apresentar o projeto e encaminhar.
- **Campos:** nenhum.
- **Botões:** "Nova Simulação" → T2; cards de perfil → respectiva simulação; "Reforma Tributária" → T8.
- **Validações:** n/a.
- **Estados vazios:** gráficos: "Disponível após validação das regras".
- **Erros:** n/a.
- **Resultado esperado:** usuário chega à simulação em 1 clique.
- **Mobile:** menu hambúrguer (existe); cards em 1 coluna.
- **Evolução:** trocar o card "Lucro Presumido" por selo "Em breve" (fora do MVP) e ligar cada card à sua tela.

### T2. Escolha de Simulação `/simulacao`
- **Objetivo:** escolher o perfil.
- **Campos:** seleção de 1 entre PF, MEI, Simples, Comparador (cards clicáveis).
- **Botões:** "Continuar" (desabilitado sem seleção).
- **Validações:** uma opção obrigatória.
- **Estados vazios:** nenhum perfil selecionado → botão inativo com dica.
- **Erros:** "Escolha um perfil para continuar."
- **Resultado:** redireciona para T3–T6.
- **Mobile:** cards empilhados. *(Hoje `/simulacao` lista os 8 anos pendentes; passará a ser esta tela, e a listagem por ano migra para o Resultado.)*

### T3. Pessoa Física `/simulacao/pf`
- **Objetivo:** estimar tributação de PF/autônomo.
- **Campos:** ano (select 2026–2033) · renda mensal (R$) · renda anual (somente leitura, = mensal × 12) · perfil de recebimento (lista: `[PENDENTE DE VALIDAÇÃO]`) · despesas/deduções (ocultas até haver regra suportada).
- **Botões:** "Simular" · "Limpar" · "Voltar".
- **Validações:** VAL-01..05.
- **Estados vazios:** antes de simular, painel de resultado com instrução.
- **Erros:** por campo; ano sem regras → mensagem de pendência.
- **Resultado esperado:** T7 com renda bruta, base, IRPF, previdência, total, carga efetiva, líquido, explicação.
- **Mobile:** formulário em coluna; resultado abaixo do formulário.

### T4. MEI `/simulacao/mei`
- **Campos:** ano · faturamento mensal · faturamento anual (leitura) · atividade/categoria (lista pendente).
- **Botões:** "Simular" · "Limpar" · (condicional) "Simular no Simples Nacional".
- **Validações:** VAL-01..05.
- **Estados vazios:** idem T3.
- **Erros:** por campo; atividade fora do suporte → "Atividade não suportada no MVP".
- **Resultado:** situação frente ao limite, % do limite, DAS, líquido, alertas.
- **Navegação:** incompatível/acima do limite → T5 com dados pré-preenchidos.
- **Mobile:** barra de % do limite em largura total.

### T5. Simples Nacional `/simulacao/simples`
- **Campos:** ano · faturamento mensal · RBT12 · folha 12 meses · pró-labore · atividade · categoria de serviço · demais campos só se estritamente necessários (a definir com a regra validada).
- **Botões:** "Simular" · "Limpar" · "Voltar".
- **Validações:** VAL-01..07.
- **Estados vazios:** idem T3.
- **Erros:** por campo; RBT12 ausente; categoria não suportada.
- **Resultado:** Fator R, anexo (III/V quando suportado), faixa, alíquota nominal, parcela a deduzir, alíquota efetiva, DAS, contribuição do pró-labore, carga, % efetivo, líquido, explicação detalhada.
- **Mobile:** campos agrupados em seções recolhíveis ("Faturamento", "Folha e pró-labore", "Atividade").

### T6. Comparador PF x PJ `/simulacao/comparar`
- **Objetivo:** mostrar PF e PJ lado a lado, sem veredito.
- **Campos:** ano · renda/faturamento mensal · dados mínimos da PJ (RBT12, folha, pró-labore, atividade) · perfil PF.
- **Botões:** "Comparar" · "Limpar".
- **Validações:** união de T3 e T5.
- **Estados vazios:** colunas vazias com instrução.
- **Erros:** se um lado estiver pendente/não suportado, ele mostra o motivo e o comparativo de diferença é ocultado (nunca comparar com número parcial).
- **Resultado:** colunas PF e PJ (RF-016/017), diferença mensal e anual, gráfico (Should), texto explicativo neutro ("A diferença é de X sob as premissas Y").
- **Mobile:** colunas viram abas ou blocos empilhados PF → PJ → Diferença.

### T7. Resultado `/resultado` (ou seção na própria tela de simulação)
- **Objetivo:** apresentar o `SimulationResult` e sua explicação.
- **Campos:** nenhum.
- **Botões:** "Comparar cenário" (→ T6 com dados) · "Nova simulação" (→ T2) · "Ver explicação" · "Ver fonte" (→ T9).
- **Validações:** n/a (dados já validados).
- **Estados vazios:** acesso sem simulação prévia → redireciona para T2 com mensagem.
- **Erros:** falha do motor → "Não foi possível calcular. Revise os dados." (sem detalhes técnicos).
- **Resultado:** itens de imposto (`TaxItem`), totais, passo a passo (`ExplanationItem`), metadados da regra (ano, fonte, status).
- **Mobile:** totais no topo; passo a passo em acordeão.

### T8. Reforma Tributária `/reforma`
- **Objetivo:** timeline educacional.
- **Campos:** seleção de ano (2026…2033).
- **Botões:** chips de ano · "Simular neste ano" (só se houver regras validadas).
- **Validações:** ano na faixa.
- **Estados vazios:** nenhum ano selecionado → mostra 2026.
- **Erros:** conteúdo ausente → `[CONTEÚDO PENDENTE DE VALIDAÇÃO]`.
- **Resultado:** para o ano: resumo, tributos envolvidos, etapa da transição, observações, fonte oficial.
- **Mobile:** timeline com rolagem horizontal *dentro do componente*; detalhe abaixo.

### T9. Sobre / Metodologia `/sobre`
- **Objetivo:** transparência.
- **Conteúdo:** finalidade educacional; como as regras são obtidas e versionadas; tabela de fontes (lida de `fontes-tributarias.md`); limitações; aviso jurídico.
- **Botões:** voltar à Home.
- **Mobile:** texto em coluna única.

## 3. Modelos de dados propostos (sem fórmulas)

Dataclasses imutáveis em `src/models/`. Dinheiro sempre `Decimal`.

```python
@dataclass(frozen=True)
class SimulationInput:
    profile: Literal["PF", "MEI", "SIMPLES", "COMPARISON"]
    year: int
    monthly_amount: Decimal                 # renda ou faturamento mensal
    activity: str | None = None
    service_category: str | None = None
    rbt12: Decimal | None = None
    payroll_12m: Decimal | None = None
    pro_labore: Decimal | None = None
    deductions: Decimal | None = None       # só quando houver regra suportada
    # annual_amount é derivado (propriedade), não campo

@dataclass(frozen=True)
class TaxRuleMetadata:
    rule_id: str
    tax: str                # IRPF, DAS, INSS...
    year: int
    source: str             # fonte oficial
    url: str
    legislation: str
    consulted_on: date
    validation_status: Literal["VALIDADA", "PENDENTE"]

@dataclass(frozen=True)
class TaxItem:
    name: str
    base: Decimal | None
    amount: Decimal | None      # None quando pendente
    rule: TaxRuleMetadata | None

@dataclass(frozen=True)
class ExplanationItem:
    step: int
    title: str
    text: str
    rule: TaxRuleMetadata | None

@dataclass(frozen=True)
class SimulationResult:
    input: SimulationInput
    status: Literal["OK", "PENDENTE", "NAO_SUPORTADO", "INCOMPATIVEL"]
    gross: Decimal | None
    items: tuple[TaxItem, ...]
    total_tax: Decimal | None
    effective_rate: Decimal | None
    net: Decimal | None
    alerts: tuple[str, ...]
    explanation: tuple[ExplanationItem, ...]

@dataclass(frozen=True)
class ComparisonResult:
    pf: SimulationResult
    pj: SimulationResult
    monthly_difference: Decimal | None      # None se algum lado não for OK
    annual_difference: Decimal | None
    notes: tuple[str, ...]                  # premissas; sem "melhor/pior"
```

Estado `PENDENTE` substitui o dict atual `{"status": ..., "resultado": None}` de `calculate()`; migração planejada para a fase de motor.
`TaxRuleMetadata` alimenta `fontes-tributarias.md` (mesmas colunas) e o Sobre.

## 4. Rotas propostas (não implementadas)

| Rota | Tela | Motivo |
|------|------|--------|
| `/simulacao` | T2 | já existe; muda de papel |
| `/simulacao/pf`, `/mei`, `/simulacao/simples`, `/simulacao/comparar` | T3–T6 | uma rota por perfil evita `if` de perfil |
| `/resultado` | T7 | separa entrada de saída |
| `/reforma` | T8 | fluxo próprio |
| `/sobre` | T9 | transparência |

Serviços previstos em `src/services/`: `pf_service`, `mei_service`, `simples_service`, `comparison_service`, `timeline_service`. As rotas só validam formato, chamam o serviço e renderizam.
**Ainda não criadas.** Aguardando aprovação para criar as rotas/templates vazios (páginas "em construção", sem cálculo).

## 5. Rastreabilidade preliminar

| Requisito | Tela | Serviço | Módulo futuro | Teste esperado |
|-----------|------|---------|---------------|----------------|
| RF-001..003, RF-005 | T3 | `pf_service` | `tax_engine/pf.py` | `test_pf_simulation` |
| RF-004 | T3 | `pf_service` | `tax_rules` | `test_pf_deductions_only_when_supported` |
| RF-006, RF-007 | T4 | `mei_service` | `tax_engine/mei.py` | `test_mei_simulation` |
| RF-008 | T4→T5 | `mei_service` | `tax_engine/mei.py` | `test_mei_over_limit_redirects_to_simples` |
| RF-009, RF-011..013 | T5 | `simples_service` | `tax_engine/simples.py` | `test_simples_simulation` |
| RF-010 | T5 | `simples_service` | `tax_engine/fator_r.py` | `test_fator_r_selects_annex` |
| RF-014 | T5 | `simples_service` | `tax_engine/simples.py` | `test_unsupported_activity` |
| RF-015..019 | T6 | `comparison_service` | `tax_engine/comparison.py` | `test_comparison_no_verdict` |
| RF-020 | T6 | `comparison_service` | `reports/` | `test_comparison_chart_data` |
| RF-021..023 | T8 | `timeline_service` | `tax_rules` | `test_timeline_pending_placeholders` |
| RF-024, RF-030 | T2, T7 | — | rotas | `test_navigation_routes` |
| RF-025 | T9 | — | rotas | `test_about_page` |
| RF-026 | todas | — | `base.html` | `test_disclaimer_on_all_pages` |
| RF-027 | T7, T9 | todos | `tax_rules` | `test_rules_have_source` |
| RF-028, RNF-013 | T3–T6 | todos | `tax_engine` | `test_pending_year_returns_no_numbers` |
| RF-029, VAL-* | T3–T6 | todos | `services/validation.py` | `test_input_validation` |
| RNF-001 | — | — | — | `test_no_tax_constants_outside_rules` |
| RNF-004 | — | — | — | `pytest --cov` no CI local |
| RNF-006, RNF-008 | todas | — | CSS | revisão manual 320 px |
| RNF-009 | — | — | `tax_engine` | `test_money_uses_decimal` |

## 6. Roadmap

**MVP 1.0** — cálculos validados de 2026; PF; MEI; Simples com Fator R; comparação; timeline educacional; Sobre; testes ≥ 80%.
**Versão 2** — Lucro Presumido; Simples híbrido; IBS/CBS mais detalhado; exportação.
**Versão 3** — regras completas 2027–2033; histórico; banco de dados (SQLite); relatórios.
**Versão futura** — atualização automática; APIs; IA; mobile.

## 7. Evolução da interface atual (sem redesign)

- Home: ligar cards às telas; "Lucro Presumido" com selo "Em breve".
- `/simulacao`: vira a Escolha de Simulação (T2).
- Cabeçalho: acrescentar "Reforma" e "Sobre".
- Manter identidade visual e CSS existentes; novos componentes: formulário, campo com erro, cartão de resultado, timeline clicável, acordeão de explicação.

## 8. Riscos de escopo

| # | Risco | Mitigação |
|---|-------|-----------|
| R1 | **Validação das regras** depende de fontes oficiais e possível revisão contábil; é o caminho crítico. | Começar o levantamento de fontes já; nada é codificado sem linha validada. |
| R2 | "Cálculo real de 2026" convive com a transição da Reforma já iniciada em 2026; risco de interpretação incompleta. | Definir na pesquisa exatamente o que vigora em 2026 para cada perfil e declarar premissas na tela Sobre. |
| R3 | **Simples + Fator R + pró-labore** têm muitas combinações (anexos, faixas, INSS do pró-labore, IRPF do pró-labore). | Limitar a serviços em Anexo III/V; demais atividades = "não suportado". |
| R4 | Comparador PF x PJ exige premissas equivalentes dos dois lados; comparar bases diferentes induz erro. | Cenário único, premissas listadas, sem veredito, lado pendente oculta a diferença. |
| R5 | MEI: regras de atividade/categoria e limite mudam; compatibilidade com o Simples é sutil. | Lista fechada de atividades suportadas; resto "incompatível/não suportado". |
| R6 | Card "Lucro Presumido" na home sugere cobertura que não existe. | Selo "Em breve". |
| R7 | Timeline 2027–2033 pode virar pesquisa aberta. | Placeholders aceitos no MVP; preencher só o que tiver fonte. |
| R8 | Cobertura ≥ 80% sem regras validadas é enganosa. | Testes do motor usam regras fictícias de teste (fixtures) claramente marcadas, nunca em `data/tax_rules/`. |
| R9 | Prazo acadêmico vs. levantamento legislativo. | Ordem: Simples/Fator R → PF → MEI → comparador; cortar Should/Could primeiro. |

## 9. Próximos passos

1. Aprovar esta especificação (e o plano de rotas vazias da seção 4).
2. Levantamento de fontes oficiais de 2026 (PF, MEI, Simples/Fator R, previdência), registrando em `fontes-tributarias.md`.
3. Definir premissas e decisões de cálculo com o orientador/contador.
4. Implementar `models`, validação e rotas/telas vazias.
5. Implementar o motor por módulo com testes, usando só regras validadas.
