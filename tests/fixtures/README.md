# Fixtures de teste

Todo arquivo neste diretório contém **dados fictícios para teste de infraestrutura**.

Nenhum valor aqui é uma regra tributária real. Nada neste diretório é lido
pelo sistema de produção (`src/tax_rules/rule_loader.py` só lê de
`data/tax_rules/<ano>/rules.json`) — os testes leem estes arquivos
diretamente, por caminho explícito, apenas para verificar a forma dos
modelos e contratos.
