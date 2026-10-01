# Simulador Tributário Brasileiro

Projeto acadêmico desenvolvido por **Beatriz Madeira Lima** e **Nychollas W. D. de Freitas**.

## Sobre o projeto

O **Simulador Tributário Brasileiro** é uma aplicação em Python criada para apresentar, de forma simples, como diferentes regras tributárias podem afetar pessoas físicas e pequenas empresas.

O projeto também apresenta a transição da **Reforma Tributária do Consumo entre 2026 e 2033** e possui um mapa mental para apoiar a apresentação e a compreensão do conteúdo.

## Principais recursos

- Simulação de cenários tributários;
- Comparação entre **Pessoa Física e Pessoa Jurídica**;
- Simples Nacional;
- Fator R;
- Comparação entre **Anexo III e Anexo V**, quando aplicável;
- Visão da Reforma Tributária de **2026 a 2033**;
- Página de simulação guiada;
- Mapa mental para apresentação do projeto;
- Testes automatizados para validação dos cálculos.

## Tecnologias utilizadas

- Python
- Flask
- HTML
- CSS
- JavaScript
- Pytest

## Como executar localmente

No Windows, abra o terminal dentro da pasta do projeto.

### 1. Criar o ambiente virtual

```bat
python -m venv .venv
```

### 2. Ativar o ambiente virtual

```bat
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bat
python -m pip install -r requirements.txt
```

### 4. Executar o projeto

```bat
python app.py
```

Depois, abra no navegador:

http://127.0.0.1:5000/

## Páginas principais

- **Página inicial:** http://127.0.0.1:5000/
- **Simulação guiada:** http://127.0.0.1:5000/simulacao-guiada
- **Reforma Tributária:** http://127.0.0.1:5000/reforma
- **Mapa mental:** http://127.0.0.1:5000/mapa-mental

## Executar os testes

Com o ambiente virtual ativado:

```bat
python -m pytest -q
```

## Objetivo acadêmico

O objetivo do projeto é facilitar a compreensão de conceitos tributários por meio de simulações e comparações visuais.

A aplicação foi desenvolvida para apoiar o estudo e a apresentação do tema.

## Autores

**Beatriz Madeira Lima**  
RGM: 11241104413

**Nychollas W. D. de Freitas**  
RGM: 11241103061
