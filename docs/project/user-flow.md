# Fluxos do Usuário

## 1. Fluxo principal de simulação

```mermaid
flowchart TD
    A[Home] --> B[Nova Simulação]
    B --> C[Escolha do Perfil]
    C --> D1[PF]
    C --> D2[MEI]
    C --> D3[Simples Nacional]
    C --> D4[Comparador PF x PJ]
    D1 & D2 & D3 & D4 --> E[Preenchimento dos dados]
    E --> F{Validação}
    F -- inválido --> E
    F -- válido --> G[Services]
    G --> H[Tax Engine]
    H --> I{Regras validadas para o ano?}
    I -- não --> J[Resultado: PENDENTE, sem valores]
    I -- sim --> K[Resultado]
    K --> L[Explicação]
    L --> M{Próxima ação}
    M -- Comparar cenário --> D4
    M -- Nova simulação --> C
    M -- MEI incompatível --> D3
```

## 2. Fluxo da Reforma Tributária

```mermaid
flowchart TD
    A[Home] --> B[Reforma Tributária]
    B --> C[Timeline 2026–2033]
    C --> D[Seleção do ano]
    D --> E[Explicação do ano: resumo, tributos, etapa, observações, fonte]
    E --> C
    E --> F[Nova Simulação naquele ano]
```

## 3. Fluxo MEI → Simples

```mermaid
flowchart LR
    M[Resultado MEI] --> Q{Acima do limite ou incompatível?}
    Q -- sim --> X[Alerta + botão 'Simular no Simples Nacional']
    X --> S[Simples com faturamento e ano pré-preenchidos]
    Q -- não --> R[Resultado normal]
```

## 4. Fluxo Comparador

```mermaid
flowchart TD
    A[Cenário único] --> V{Validação}
    V --> PF[Serviço PF]
    V --> PJ[Serviço PJ: Simples]
    PF --> C[ComparisonResult]
    PJ --> C
    C --> T[Colunas lado a lado + diferenças + explicação]
```

## Navegação global
Cabeçalho: Home · Simulações · Reforma · Sobre. Rodapé com aviso educacional em todas as telas.
