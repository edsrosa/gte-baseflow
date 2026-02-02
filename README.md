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
gtebaseflow/
├─ gtebaseflow/             #  Diretório principal da aplicação
│  ├─ src/                  #  
│  │  ├─ about.html         #  Conteúdo da página com o Sobre da aplicação
│  │  ├─ help.html          #  Contéudo do texto de ajuda da aplicação
│  │  ├─ page.py            #  Estruturação da página principal
│  │  ├─ style.css          #  Folha de estilos CSS
│  │  └─ utils.py           #  Chamada de ferramentas para montar a página
│  ├─ tools/                #  
│  │  ├─ database.py        #  Processamento de dados e arquivos
│  │  ├─ use.py             #  Chamada das ferramentas de uso
│  │  └─ viewer.py          #  Visualização de gráficos e mapas
│  └─ app.py                #  Entry point principal para chamada da aplicação
├─ examples/                #  Pasta com arquivos de exemplo de entrada e saída
├─ .streamlit/              #  
│  └─ config.toml           #  Configurações do Streamlit
├─ .gitignore               #  Diretórios e arquivos a serem ignorados pelo Git
├─ LICENSE                  #  Licença do projeto
├─ README.md                #  README do projeto
└─ requirements.txt         #  Dependências da aplicação
```