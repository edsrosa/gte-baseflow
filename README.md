# GTE Baseflow

Aplicação para separação de fluxo de base e análise de hidrogramas.  

## Utilização Local

1 - Clone o repositório

```sh
 git clone https://github.com/edsrosa/gte-baseflow.git
```

2 - Crie um ambiente virtual  

```sh
 python -m venv .venv
```

3 - Instale as dependências

```sh
 pip install -r requirements.txt
```

## Execução Local da Ferramenta

```sh
 streamlit run gtebaseflow/app.py
```

## Estrutura de Pastas

```sh
gte-baseflow/ 
├─ gtebaseflow/
│  ├─ app.py
│  ├─ src
│  │  ├─ baseflow.py
│  │  ├─ style.css
│  │  └─ utils.py
│  └─ tools
│     ├─ data.py
│     └─ viewer.py
├─ examples/
├─ .gitignore
├─ LICENSE.txt
├─ README.md
└─ requirements.txt
```
