import pandas as pd
import matplotlib.pyplot as plt
import io

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List

app = FastAPI(
    title="API de Análise de Dados com Pandas",
    description="Uma API para realizar análises estatísticas e gerar visualizações a partir de um arquivo CSV.",
    version="1.0.0"
)

def data_processing(file: UploadFile):
    try:
        df = pd.read_csv(file.file)
        return df
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar arquivo CSV: {e}")

@app.get("/", summary="Endpoint Root")
def read_root():
    return {"message": "Bem-vindo à API de Análise de Dados"}

@app.post("/statistics", summary="Calcula Estatísticas Descritivas")
async def get_statistics(file: UploadFile = File(..., description="Arquivo CSV para análise.")):
    df = data_processing(file)

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if not numeric_cols:
        raise HTTPException(status_code=400, detail="O arquivo CSV não contém colunas numéricas para análise.")

    statistics = df[numeric_cols].describe()
    json_result = statistics.to_dict()
    return JSONResponse(content=json_result)

@app.post("/preview/histogram", summary="Gera um Histograma")
async def generate_histogram(
        column: str = Form(..., description="Nome da coluna para gerar o histograma."),
        file: UploadFile = File(..., description="Arquivo CSV com os dados.")
):
    df = data_processing(file)
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