import pandas as pd
import matplotlib.pyplot as plt
import io

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List
from enum import Enum

app = FastAPI(
    title="API de Análise de Dados com Pandas",
    description="Uma API para realizar análises estatísticas e gerar visualizações a partir de um arquivo CSV.",
    version="1.0.0"
)

def get_dataframe(file: UploadFile = File(..., description="Arquivo CSV para análise.")):
    try:
        file.file.seek(0)
        df = pd.read_csv(file.file)
        return df
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar arquivo CSV: {e}")

class AggFunction(str, Enum):
    soma = "soma",
    media = "media",
    contagem = "contagem",
    maximo = "maximo",
    minimo = "minimo"

@app.get("/", summary="Endpoint Root")
def read_root():
    return {"message": "Bem-vindo à API de Análise de Dados"}

@app.post("/statistics", summary="Calcula Estatísticas Descritivas")
async def get_statistics(df: pd.DataFrame = Depends(get_dataframe)):
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if not numeric_cols:
        raise HTTPException(status_code=400, detail="O arquivo CSV não contém colunas numéricas para análise.")

    statistics = df[numeric_cols].describe()
    json_result = statistics.to_dict()
    return JSONResponse(content=json_result)

@app.post("/preview/histogram", summary="Gera um Histograma")
async def generate_histogram(
        column: str = Form(..., description="Nome da coluna para gerar o histograma."),
        df: pd.DataFrame = Depends(get_dataframe)
):
    if column not in df.columns:
        raise HTTPException(status_code=400, detail="")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise HTTPException(status_code=400, detail="")

    plt.figure(figsize=(10, 6))
    plt.hist(df[column], bins=20, color="skyblue", edgecolor="black")
    plt.title(label=f"Histograma da Coluna: {column}")
    plt.xlabel(xlabel=column)
    plt.ylabel(ylabel="Frequência")
    plt.grid(True, linestyle="--", alpha=0.6)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    return StreamingResponse(buffer, media_type="image/png")

@app.post("/preview/bars", summary="Gera um Gráfico de Barras")
async def generate_bar_chart(
        column_x: str = Form(..., description="Nome da coluna categórica para o eixo X."),
        column_y: str = Form(..., description="Nome da coluna numérica para o eixo Y."),
        df: pd.DataFrame = Depends(get_dataframe)
):
    if column_x not in df.columns or column_y not in df.columns:
        raise HTTPException(status_code=400, detail="Uma ou ambas as colunas não foram encontradas no arquivo.")
    if not pd.api.types.is_numeric_dtype(df[column_y]):
        raise HTTPException(status_code=400, detail=f"A coluna do eixo Y ('{column_y}') deve ser numérica.")

    plt.figure(figsize=(10, 7))
    plt.bar(df[column_x], df[column_y], color='cornflowerblue')
    plt.title(f"Gráfico de Barras: {column_y} por {column_x}")
    plt.xlabel(column_x)
    plt.ylabel(column_y)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    return StreamingResponse(buffer, media_type="image/png")

@app.post("/preview/scatter", summary="Gera um Gráfico de Dispersão")
async def generate_scatter(
        column_x: str = Form(..., description="Nome da coluna categórica para o eixo X."),
        column_y: str = Form(..., description="Nome da coluna numérica para o eixo Y."),
        df: pd.DataFrame = Depends(get_dataframe)
):

    if column_x not in df.columns or column_y not in df.columns:
        raise HTTPException(status_code=400, detail="Uma ou ambas as colunas não foram encontradas no arquivo.")
    if not pd.api.types.is_numeric_dtype(df[column_x]) or not pd.api.types.is_numeric_dtype(df[column_y]):
        raise HTTPException(status_code=400, detail=f"Ambas as colunas devem ser numéricas para o gráfico de dispersão.")

    plt.figure(figsize=(10, 6))
    plt.scatter(df[column_x], df[column_y], alpha=0.7, color='purple')
    plt.title(f"Gráfico de Dispersão: {column_y} vs. {column_x}")
    plt.xlabel(column_x)
    plt.ylabel(column_y)
    plt.grid(visible=True, linestyle="--", alpha=0.6)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    return StreamingResponse(buffer, media_type="image/png")

@app.post("/analysis/correlation", summary="Calcula a Matriz de Correlação")
async def get_correlation(df: pd.DataFrame = Depends(get_dataframe)):
    df_numeric = df.select_dtypes(include=["number"])

    if df_numeric.shape[1] < 2:
        raise HTTPException(status_code=400, detail="São necessárias pelo menos duas colunas numéricas para calcular a correlação.")

    correlation = df_numeric.corr()
    json_result = correlation.to_dict()
    return JSONResponse(content=json_result)

@app.post("/analysis/groupby", summary="Agrupa os Dados por Categoria")
async def get_group(
        group_by: str = Form(..., description="Coluna categórica a ser usada para o agrupamento."),
        values: str = Form(..., description="Coluna numérica cujos valores serão agregados."),
        function: AggFunction = Form(..., description="A função de agregação a ser aplicada (soma, media, etc.)."),
        df: pd.DataFrame = Depends(get_dataframe)
):
    func_map = {
        "soma": "sum",
        "media": "mean",
        "contagem": "count",
        "maximo": "max",
        "minimo": "min"
    }

    if group_by not in df.columns or values not in df.columns:
        raise HTTPException(status_code=400, detail="")

    if not pd.api.types.is_numeric_dtype(df[values]):
        raise HTTPException(status_code=400, detail=f"A coluna de valor '{values}' deve ser numérica.")

    try:
        agg_func = func_map[function.value]
        result = df.groupby(group_by)[values].agg(agg_func)
        json_result = result.to_dict()
        return JSONResponse(content=json_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao processar o agrupamento: {e}")