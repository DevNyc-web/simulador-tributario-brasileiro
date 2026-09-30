# Simulador Tributário Brasileiro 2026–2033

> ⚠️ Ferramenta educacional. Não substitui orientação contábil ou jurídica.

Sistema web educacional para simulação e comparação tributária. Relatório acadêmico completo: [docs/academic/relatorio-final.md](docs/academic/relatorio-final.md).

## Problema
A complexidade do sistema tributário brasileiro dificulta que pessoas físicas, autônomos, MEIs e prestadores de serviços compreendam o impacto aproximado de diferentes estruturas tributárias.

## Objetivo
Simular e comparar cenários de 2026 de forma transparente e rastreável (cálculo, premissas, avisos e diferenças numéricas), sem recomendar regime tributário.

## Escopo da versão atual
**Cálculo tributário real apenas para o ano-calendário de 2026**, com regras TR-001 a TR-011 pesquisadas, validadas, implementadas e testadas:

- **Pessoa Física / autônomo** — IRPF mensal e INSS do contribuinte individual (planos normal e simplificado). Funcional.
- **MEI** — limite anual/proporcional e DAS-MEI. Funcional.
- **Simples Nacional (serviços)** — Anexos III e V, RBT12/RBT12p, Fator R, nove atividades validadas. Funcional.
- **Pró-labore e dividendos** — INSS/IRPF do pró-labore, IRRF sobre dividendos e limite sem escrituração. Funcional.
- **Comparador PF × PJ** — lado a lado, com diferenças numéricas e sem recomendação. Funcional.
- **Interface web integrada** — formulários, validação no servidor e resultados explicados.

**2027–2033:** apenas linha do tempo educacional da Reforma (estrutura de navegação; conteúdo por ano ainda pendente de validação). Não há motor fiscal para esses anos; os arquivos de regras correspondentes estão vazios.

Fora do escopo: Lucro Presumido, Lucro Real, banco de dados/histórico, autenticação, exportação em PDF, integração com APIs governamentais, atualização legal automática. Limitações detalhadas no relatório final.

**Qualidade:** 432 testes automatizados; 98% de cobertura de linhas (`src` + `app.py`). Ver [docs/project/testing-and-quality.md](docs/project/testing-and-quality.md).

## Stack
Python + Flask · HTML5/CSS3/JavaScript puros · `decimal.Decimal` para valores monetários · pytest. Sem banco de dados, sem login, sem sessão e sem framework de front-end.

## Arquitetura
```
Navegador → app.py (rotas Flask)
  → src/services (adaptadores e orquestração) → src/tax_engine (cálculo)
  → src/tax_rules (carga de regras) → data/tax_rules/<ano>/rules.json
```
Nenhuma fórmula fiscal no HTML, JS ou rotas. Os parâmetros fiscais vivem só em `data/tax_rules/<ano>/rules.json`; as fórmulas, em `src/tax_engine`. Fontes e rastreabilidade das regras: `docs/research/` (catálogo, matriz e fontes).

## Estrutura
- `app.py` – app Flask e rotas (`POST /resultado` executa as simulações)
- `src/tax_engine` – motores de cálculo · `src/tax_rules` – carga de regras · `src/services` – adaptadores, serviço e apresentação · `src/models` – modelos imutáveis e enums
- `data/tax_rules/2026…2033` – regras por ano (2026 com TR-001 a TR-011; 2027–2033 vazios)
- `templates/`, `static/` – interface · `tests/` – pytest · `docs/` – pesquisa, projeto e relatório acadêmico

## Executando localmente
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py          # http://127.0.0.1:5000
python -m pytest       # executa os testes
```
Cobertura (ferramenta de desenvolvimento, não consta em `requirements.txt`):
```
pip install coverage
python -m coverage run --source=src,app -m pytest
python -m coverage report -m
```
