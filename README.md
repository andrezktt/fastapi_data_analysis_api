# API de Análise de Dados com Python, FastAPI e Pandas

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-blue?logo=fastapi&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.3-blue?logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

Uma API RESTful de alta performance construída com FastAPI para upload, análise estatística e visualização de dados a partir de arquivos CSV.

## 📖 Sobre o Projeto

Este projeto fornece uma interface web para realizar análises de dados de forma rápida e programática. Usuários podem enviar arquivos CSV e obter em troca:
-   Estatísticas descritivas completas (média, mediana, desvio padrão, etc.).
-   Análises mais complexas como matriz de correlação e agrupamento de dados.
-   Visualizações gráficas, como histogramas, gráficos de barra e de dispersão.

A aplicação é totalmente containerizada com Docker, garantindo um ambiente de execução consistente e facilitando o deploy.

## ✨ Funcionalidades Principais

-   **Upload de Arquivos**: Endpoint para receber arquivos `.csv` via requisições HTTP.
-   **Estatísticas Descritivas**: Calcula e retorna um sumário estatístico completo das colunas numéricas.
-   **Análise de Correlação**: Gera uma matriz de correlação entre as variáveis numéricas.
-   **Agrupamento de Dados**: Permite agrupar dados por uma coluna categórica e aplicar funções de agregação (soma, média, etc.).
-   **Visualização de Dados**: Endpoints dedicados para gerar e retornar imagens de gráficos:
    -   Histograma
    -   Gráfico de Barras
    -   Gráfico de Dispersão (Scatter Plot)

## 🛠️ Tecnologias Utilizadas

-   **Backend**: Python 3.12+
-   **Framework API**: FastAPI
-   **Servidor ASGI**: Uvicorn
-   **Análise de Dados**: Pandas
-   **Visualização de Dados**: Matplotlib
-   **Containerização**: Docker
-   **Validação de Dados**: Pydantic (integrado ao FastAPI)

## 🚀 Como Executar o Projeto

Existem duas maneiras de executar a aplicação: utilizando Docker (recomendado para simplicidade) ou localmente em um ambiente virtual Python.

### Método 1: Usando Docker (Recomendado)

Este é o método mais simples e garante que a aplicação funcione em qualquer ambiente.

**Pré-requisitos:**
-   [Docker](https://www.docker.com/products/docker-desktop/) instalado e em execução.

**Passos:**
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/andrezktt/fastapi_data_analysis_api.git]
    cd fastapi_data_analysis_api
    ```

2.  **Construa a imagem Docker:**
    O comando a seguir lê o `Dockerfile` e constrói a imagem da aplicação.
    ```bash
    docker build -t api-analise-dados .
    ```

3.  **Execute o contêiner:**
    Este comando inicia um contêiner a partir da imagem, mapeando a porta 8000 da sua máquina para a porta 80 do contêiner.
    ```bash
    docker run -d -p 8000:80 --name my-api-container api-data-analysis
    ```

4.  **Acesse a API:**
    A API estará disponível em `http://127.0.0.1:8000`. A documentação interativa pode ser acessada em `http://127.0.0.1:8000/docs`.

### Método 2: Executando Localmente

Use este método se você quiser modificar o código e testar em um ambiente de desenvolvimento.

**Pré-requisitos:**
-   Python 3.12 ou superior.

**Passos:**
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/andrezktt/fastapi_data_analysis_api.git]
    cd fastapi_data_analysis_api
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicie o servidor de desenvolvimento:**
    ```bash
    uvicorn main:app --reload
    ```

5.  **Acesse a API:**
    A API estará disponível em `http://127.0.0.1:8000`.

## 🕹️ Como Usar a API

A forma mais fácil de interagir com a API é através da documentação interativa gerada pelo Swagger UI em `/docs`. Abaixo, exemplos de como usar os endpoints com `curl`.

*Crie um arquivo de exemplo `dados.csv` para os testes.*

### 1. Estatísticas Descritivas
```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/statistics](http://127.0.0.1:8000/statistics)' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@dados.csv;type=text/csv'
```

### 2. Matriz de Correlação
```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/analysis/correlation](http://127.0.0.1:8000/analysis/correlation)' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@dados.csv;type=text/csv'
```

### 3. Agrupamento de Dados
Este exemplo agrupa os dados pela coluna `Categoria` e calcula a `soma` da coluna `Vendas`.
```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/analysis/groupby](http://127.0.0.1:8000/analysis/groupby)' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'coluna_agrupadora=Categoria' \
  -F 'coluna_valor=Vendas' \
  -F 'funcao=soma' \
  -F 'file=@dados.csv;type=text/csv'
```

### 4. Gerar Histograma
Gera um histograma da coluna `Preco`. O resultado é uma imagem PNG.
```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/preview/histogram](http://127.0.0.1:8000/preview/histogram)' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'coluna=Preco' \
  -F 'file=@dados.csv;type=text/csv' \
  --output histograma.png
```

## 🏗️ Estrutura do Projeto
```
/api-analise-dados
|
|-- data 
|-- main.py                # Código principal da aplicação FastAPI
|-- Dockerfile             # "Receita" para construir a imagem Docker
|-- requirements.txt       # Lista de dependências Python
|-- .dockerignore          # Arquivos a serem ignorados pelo Docker
|-- README.md              # Este arquivo
```

## 🔮 Melhorias Futuras

-   [ ] Suporte a outros formatos de arquivo (Excel, Parquet).
-   [ ] Adicionar mais tipos de gráficos (Boxplot, Gráfico de Pizza).
-   [ ] Implementar um sistema de autenticação para proteger os endpoints.
-   [ ] Criar um pipeline de CI/CD (Integração Contínua/Entrega Contínua) com GitHub Actions.
-   [ ] Adicionar testes unitários e de integração.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Feito por **[Seu Nome]**

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andrezicatti/)
[![github](https://img.shields.io/badge/github-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/andrezktt)