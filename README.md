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
gtebaseflow/                #  
├─ gtebaseflow/             #  
├─ examples/                #  
├─ .streamlit               #  
│  └─ config.toml           #  
│  ├─ src                   #  
│  │  ├─ about.html         #  
│  │  ├─ help.html          #  
│  │  ├─ page.py            #  
│  │  ├─ style.css          #  
│  │  └─ utils.py           #  
│  ├─ tools                 #  
│  │  ├─ database.py        #  
│  │  ├─  use.py            #  
│  │  └─ viewer.py          #  
│  └─ app.py                #  
├─ .gitignore               #  
├─ LICENSE                  #  
├─ README.md                #  
└─ requirements.txt         #  
```
