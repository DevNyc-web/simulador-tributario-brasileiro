# Matriz MoSCoW do MVP

> **Status posterior (MVP final):** matriz original, preservada como histórico. Entregues: todos os itens Must, e a "Timeline 2026–2033" foi entregue com conteúdo educacional e fonte oficial (sem motor para 2027–2033). Entregue além do plano: simulação guiada e gráficos (na simulação guiada). Não entregues: itens Should (gráficos no comparador, indicador de carga efetiva, atalhos entre simulações) e Could (exportação, histórico temporário, Lucro Presumido simplificado). A priorização consolidada da entrega final (com dividendos como Should) está em [../academic/relatorio-final.md](../academic/relatorio-final.md), seção 10, e prevalece para a versão entregue.

## Must have
| Item | Justificativa |
|------|---------------|
| PF / autônomo | Base do comparador. |
| MEI | Perfil-alvo do público; porta de entrada ao Simples. |
| Simples Nacional (serviços) | Principal módulo. |
| Fator R | Determina o anexo; sem ele o Simples é incorreto. |
| Comparador PF x PJ | Funcionalidade central da apresentação. |
| Resultados explicados | Finalidade educacional. |
| Timeline 2026–2033 (conteúdo pendente aceito) | Objetivo do projeto. |
| Layout responsivo | RNF-006. |
| Testes automatizados (≥ 80% no núcleo) | Meta do projeto. |
| Fontes rastreáveis | Sem fonte, sem regra (RF-027). |
| Validação de entrada | Evita cálculo com dado inválido (RF-029). *(adicionado)* |
| Página Sobre / Metodologia | Transparência de premissas e limites. *(adicionado)* |

## Should have
- Gráficos comparativos (PF x PJ; carga por componente).
- Explicações visuais (passo a passo).
- Indicadores de carga tributária efetiva.
- Atalhos entre simulações (ex.: MEI → Simples, Simples → Comparador).

## Could have
- Exportação simples (impressão/PDF pelo navegador ou CSV).
- Histórico temporário (só na sessão do navegador, sem servidor).
- Lucro Presumido simplificado.

## Won't have nesta entrega
- Lucro Real completo
- Lucro Presumido completo
- Banco de usuários / login
- API governamental
- Atualização automática de legislação
- IA
- Aplicativo mobile
- Cálculo completo de 2027–2033
- IBS/CBS detalhado por operação

## Ajustes em relação à sugestão inicial
1. **Validação de entrada** e **Sobre/Metodologia** promovidos a Must: são pré-requisitos de RF-029 e RF-025.
2. **Lucro Presumido simplificado** permanece Could, mas o card já existe na home; deve mostrar "em breve" e não um cálculo. Ver risco de escopo.
3. **Simples híbrido** (IBS/CBS fora do DAS) fica fora do MVP; entra na Versão 2.
