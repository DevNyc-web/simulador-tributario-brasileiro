# Simulador Tributário Brasileiro 2026–2033

> ⚠️ Ferramenta educacional. Não substitui orientação contábil ou jurídica.

## Problema
A transição da Reforma Tributária (2026–2033) altera gradualmente as regras para pessoas físicas e jurídicas, dificultando a comparação de cenários.

## Objetivo
Simulador educacional que compara cenários de Pessoa Física e Pessoa Jurídica e mostra a evolução das regras ano a ano.

## Stack
Python + Flask · HTML5/CSS3/JavaScript puro · pytest · sem banco de dados (SQLite só se necessário). Sem frameworks frontend.

## Arquitetura
```
Interface (templates/static) → app.py (rotas)
  → src/services → src/tax_engine → src/tax_rules → data/tax_rules/<ano>/
```
Nenhuma fórmula fiscal no HTML, JS ou rotas. Regras vivem só em `data/tax_rules/<ano>/rules.json`.
Tudo não validado é marcado `[REGRA PENDENTE DE VALIDAÇÃO]`; fontes em `docs/research/fontes-tributarias.md`.

## Estrutura
- `app.py` – app Flask e rotas
- `src/tax_engine` – cálculo · `src/tax_rules` – carga de regras · `src/services` – orquestração
- `src/models`, `src/reports` – reservados
- `data/tax_rules/2026…2033` – regras por ano (placeholders)
- `templates/`, `static/` – interface · `tests/` – pytest · `docs/` – documentação

## Executar
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py        # http://127.0.0.1:5000
pytest
```

## Status
Estrutura inicial. **Nenhum cálculo tributário real implementado**; todas as regras pendentes de validação. Meta futura: cobertura ≥ 80%.
