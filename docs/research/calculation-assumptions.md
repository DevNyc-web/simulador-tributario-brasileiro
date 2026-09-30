# Premissas e Decisões de Cálculo

Decisões aprovadas para o MVP 1.0. Mudanças exigem aprovação e atualização deste arquivo.

| # | Decisão | Motivo |
|---|---------|--------|
| 1 | O cálculo completo do MVP será focado em **2026**. | Limita o levantamento legislativo; 2027–2033 seguem preparados por ano. |
| 2 | Pessoa Física terá foco inicial em **profissional autônomo / prestador de serviços**. | Perfil que se compara com PJ de serviços. |
| 3 | O Simples Nacional do MVP terá foco em **prestação de serviços sujeita ao Anexo III / Anexo V e Fator R**. | Cobre o caso central do comparador. |
| 4 | **Não** se tenta suportar todas as atividades do Simples. | Evita cálculo incorreto; o resto vira "não suportado". |
| 5 | O MEI usa um **conjunto fechado de categorias suportadas**. | Regras variam por atividade. |
| 6 | PF x PJ só é comparado quando os dois cenários forem **equivalentes** e todas as regras necessárias estiverem **validadas**. | Evita comparar bases diferentes ou números parciais. |
| 7 | Valores pendentes permanecem **`None`**, nunca zero. | Zero é um valor; pendente é ausência de valor. |
| 8 | O sistema **não classifica** uma alternativa como "melhor" ou "pior". | Ferramenta educacional; a interpretação é do usuário. |
| 9 | A timeline 2026–2033 é **inicialmente educacional**. | Sem cálculo por ano além de 2026 no MVP. |
| 10 | **Lucro Presumido e Lucro Real** não fazem parte do cálculo do MVP 1.0. | Escopo (ver [moscow.md](../project/moscow.md)). |

## Cenário Pessoa Física aprovado (premissa 11)

| # | Decisão | Motivo |
|---|---------|--------|
| 11 | O módulo Pessoa Física do MVP representa inicialmente: pessoa física residente no Brasil; profissional autônomo; prestação de serviços sem vínculo empregatício, por conta própria; rendimentos recebidos de **outras pessoas físicas no Brasil**; ano-calendário 2026. | Enquadra o Carnê-Leão (TR-001) e o contribuinte individual por conta própria (TR-002). |
| 12 | O usuário **seleciona o plano previdenciário** (normal 20% ou simplificado 11%); o sistema não escolhe. | Ambos são compatíveis com o cenário; ver [pf-2026-research.md](pf-2026-research.md). |

**Fora do escopo inicial:** rendimentos do exterior; prestação de serviços para pessoa jurídica; transporte de cargas; transporte de passageiros; representante comercial em situações especiais; leiloeiro; atividade notarial; múltiplas fontes com tratamentos diferentes; dependentes; pensão alimentícia; Livro Caixa no cálculo do MVP inicial.

**Limitação deliberada:** dependentes, pensão alimentícia e Livro Caixa **existem legalmente** como deduções do Carnê-Leão (Lei 9.250/1995, art. 4º; Receita Federal, página Deduções). Ficam fora da primeira versão por escolha de escopo, não por inexistência; a interface deve informar essa limitação ao usuário.

## Regras de uso de fontes

1. Só fonte oficial primária (Receita Federal, Portal do Simples Nacional, CGSN, Planalto, INSS, Ministério da Fazenda, Ministério do Empreendedorismo, Diário Oficial quando necessário).
2. Fonte secundária apenas para descoberta; nunca como fonte final de fórmula.
3. Nenhum valor entra no projeto por conhecimento próprio de quem desenvolve: só o que estiver na fonte registrada.
4. Regra só chega a `rules.json` com status `VALIDADA` no catálogo e linha completa em `fontes-tributarias.md`.
5. Testes fiscais só usam valores rastreáveis à fonte; testes de mecânica usam fixtures fictícias, fora de `data/tax_rules/`.
