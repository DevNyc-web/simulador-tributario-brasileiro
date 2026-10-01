# Testes e qualidade

Registro da estratégia de testes e da medição de cobertura do MVP 2026 (atualizado após a simulação guiada).

## Como reproduzir

```
python -m pytest -v
python -m coverage erase
python -m coverage run --source=src,app -m pytest
python -m coverage report -m
```

- **Testes:** `pytest` (dependência já existente em `requirements.txt`).
- **Cobertura:** `coverage` 7.16.2, instalado **apenas no ambiente virtual local** (`python -m pip install coverage`). É ferramenta de desenvolvimento: **não** consta em `requirements.txt` e não é dependência de produção. O arquivo `.coverage` e o diretório `htmlcov/` já estão no `.gitignore`; nenhum relatório HTML é versionado.
- Dependências de runtime: Flask e a biblioteca padrão do Python.

## Resultado (Fase 4G)

- **Testes:** 535, todos passando.
- **Cobertura total (`src` + `app.py`): 98%** (meta acadêmica: ≥ 80%).

| Grupo | Cobertura |
|---|---|
| `src/tax_engine` (motores PF, MEI, Simples, pró-labore, dividendos, comparador, calculator) | ≈ 99,5% |
| `src/tax_rules` (loader, `parse_decimal`, exceções) | ≈ 93% |
| `src/services` (serviço, adaptador de formulário, simulação guiada, apresentação) | ≈ 97% |
| `src/models` | 98% |
| `app.py` | 98% |

Linhas sem cobertura: ramos defensivos (validação de ano não suportado em `dividendos_2026.py`/`comparator_2026.py`, erros raros de arquivo em `rule_loader.py`, guard `if __name__ == "__main__"` em `app.py`). Não foram criados testes artificiais para aumentar o número.

## Estratégia de testes

1. **Infraestrutura de regras** (`test_rule_loader.py`, `test_tax_models.py`): schema do `rules.json`, anos suportados (2026 com TR-001 a TR-011; 2027–2033 com `regras: []`), IDs únicos, status válidos, parâmetros decimais sempre como string, parser decimal estrito, modelos imutáveis.
2. **Motores fiscais**, um arquivo por módulo: `test_pf_2026.py` (TR-001/TR-002), `test_mei_2026.py` (TR-003/TR-004), `test_simples_2026.py` (TR-005 a TR-009), `test_prolabore_dividendos_2026.py` (TR-010/TR-011), `test_comparator_2026.py`. Os valores esperados vêm da pesquisa validada (`docs/research/`); exemplos oficiais da Receita aparecem como `test_irpf_official_example_*`.
3. **Fronteiras** (valores de corte, inclusive/exclusive): IRPF 5.000 / 5.000,01 e 7.350 / 7.350,01 e limites das faixas; MEI 81.000 / 81.000,01 e 97.200 / 97.200,01, inclusive proporcional; Fator R 0,27 / 0,28 / 0,29 e truncamento em duas casas; Simples 3.600.000 / 3.600.000,01 e 4.800.000 / 4.800.000,01; dividendos 50.000 / 50.000,01; altas rendas 600.000 / 600.000,01.
4. **Regressão e invariantes:** `total = soma dos itens`, `líquido = bruto − tributos`, ausência de `float` nos resultados, valores zero (renda zero, MEI sem receita, pró-labore zero, dividendos zero) e casos não suportados que nunca devolvem resultado parcial.
5. **Integração frontend/backend** (`test_frontend_integration.py`): `POST /resultado` para os quatro módulos, parser de moeda brasileira, validação server-side (erros por campo, sem 500), histórico do Simples, comparador com receita única e folha derivada do pró-labore, ausência de veredito PF/PJ.
6. **Robustez:** varredura de entradas hostis (vazio, `NaN`, `Infinity`, `1e10`, negativos, números enormes, enums e booleanos inválidos, meses fora da faixa, histórico faltante ou extra, HTML) em todos os campos dos quatro formulários, com `PROPAGATE_EXCEPTIONS` ligado: nenhuma exceção não tratada nem 500.
7. **Camadas:** auditoria automática de que `app.py`, `templates/`, `static/js/` e os módulos de serviço não contêm parâmetros fiscais; nenhum `|safe` nos templates; valores digitados são escapados na saída.
8. **Simulação guiada** (`test_guided_simulation.py`): faturamento derivado (ticket médio × clientes), cenários de equipe, identidade da sobra operacional, projeções de 12 e 60 meses, regra de empregados do MEI (limite de quantidade, com salário mínimo ou piso da categoria), premissas e ressalvas explícitas, validação e entradas hostis, e ausência de "lucro líquido" nos textos.
9. **Linha do tempo da Reforma:** sete etapas (2026 a 2033), selos "Cálculo implementado no MVP" × "Conteúdo educacional / motor futuro", contagens reais de regras por exercício, cronograma oficial resumido (proporções 10/90 a 40/60 apresentadas como progressão, não como alíquota) e explicação do versionamento por exercício.
10. **Lógica fiscal fora do JavaScript:** testes automáticos que varrem os JS e templates novos (guiado, reforma e mapa mental) em busca de alíquotas, limites e termos fiscais, e que proíbem rede e navegação livre.

## Verificação de layout a 360px

Sem instalar framework de automação, foi feita uma medição programática no Chrome local: as 9 páginas GET e 6 respostas de POST (PF, MEI, Simples, comparador, com e sem erro) foram carregadas em um quadro de 360px de largura e nenhuma gerou rolagem horizontal. **Inspeção visual manual em 360px continua pendente para a revisão final** (a medição não avalia estética).

## Dívidas técnicas conhecidas

- A cobertura mede linhas, não ramos (`--branch` não foi usado).
- Política de arredondamento do DAS e do IRPF segue em aberto (Q-02 / Q-SN-04); a tela arredonda apenas a exibição.
- Q-PJ-05 (releitura do art. 145 da Resolução CGSN 140) permanece como pendência documental.
