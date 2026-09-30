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

## Regras de uso de fontes

1. Só fonte oficial primária (Receita Federal, Portal do Simples Nacional, CGSN, Planalto, INSS, Ministério da Fazenda, Ministério do Empreendedorismo, Diário Oficial quando necessário).
2. Fonte secundária apenas para descoberta; nunca como fonte final de fórmula.
3. Nenhum valor entra no projeto por conhecimento próprio de quem desenvolve: só o que estiver na fonte registrada.
4. Regra só chega a `rules.json` com status `VALIDADA` no catálogo e linha completa em `fontes-tributarias.md`.
5. Testes fiscais só usam valores rastreáveis à fonte; testes de mecânica usam fixtures fictícias, fora de `data/tax_rules/`.
