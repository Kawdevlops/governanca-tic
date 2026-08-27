

# Lê a planilha de OT (Orientações Técnicas), transforma tudo em memória com pandas e grava direto na tabela final `ouro.fato_ot`.

import hashlib
import os
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text

from airflow import DAG
from airflow.operators.python import PythonOperator

CAMINHO_EXCEL = "/opt/airflow/saidas/base_consolidada_validada.xlsx"

PASTA_SQL_SETUP = "/opt/airflow/sql_setup"


ARQUIVOS_ESTRUTURA = [
    "schema_ouro.sql",
    "tabela_ouro.sql",
]


def conectar():
    return create_engine(
        f"postgresql+psycopg2://{os.environ['DB_STREAMLIT_USER']}:{os.environ['DB_STREAMLIT_PASSWORD']}"
        f"@{os.environ['DB_STREAMLIT_HOST']}:{os.environ['DB_STREAMLIT_PORT']}/{os.environ['DB_STREAMLIT_DATABASE']}"
    )


"""Cria o schema `ouro` e a tabela `ouro.fato_ot`, se ainda não existirem."""

def garantir_estrutura():
    """Cria o schema `ouro` e a tabela `ouro.fato_ot`, se ainda não existirem."""
    engine = conectar()
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))
        for nome_arquivo in ARQUIVOS_ESTRUTURA:
            caminho = os.path.join(PASTA_SQL_SETUP, nome_arquivo)
            if not os.path.exists(caminho):
                raise FileNotFoundError(
                    f"Arquivo de estrutura obrigatório não encontrado: {caminho}. "
                    f"Verifique o volume montado em {PASTA_SQL_SETUP}."
                )
            with open(caminho, "r", encoding="utf-8") as f:
                sql = f.read()
            conn.execute(text(sql))
            print(f"Estrutura aplicada: {nome_arquivo}")


def _calcular_status(row) -> str:
    """Repete em Python a mesma regra que antes era um CASE WHEN em SQL."""
    if row["cumprida_totalmente"]:
        return "Cumprida Totalmente"
    if row["cumprida_parcialmente"]:
        return "Cumprida Parcialmente"
    if row["nao_cumprida"]:
        return "Não Cumprida"
    return "Indefinido"


def _calcular_chave_natural(row) -> str:
    texto = f"OT|{row['ot']}|{row['segmento']}|{row['recomendacao']}"
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def carregar_e_publicar_ouro():
    engine = conectar()

    df = pd.read_excel(CAMINHO_EXCEL, sheet_name="Sheet1")
    df = df.rename(columns={
        "SEGMENTO": "segmento",
        "RECOMENDACAO": "recomendacao",
        "DATA_VERIFICACAO_CUMPRIMENTO": "data_avaliacao",
        "CUMPRIDA_TOTALMENTE": "cumprida_totalmente",
        "CUMPRIDA_PARCIALMENTE": "cumprida_parcialmente",
        "NAO_CUMPRIDA": "nao_cumprida",
        "OT": "ot",
        "OT_TITULO": "ot_titulo",
    })

    df["status"] = df.apply(_calcular_status, axis=1)
    df["chave_natural"] = df.apply(_calcular_chave_natural, axis=1)

    df_final = df[["chave_natural", "ot", "ot_titulo", "segmento", "status", "data_avaliacao"]]

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE ouro.fato_ot;"))
        df_final.to_sql("fato_ot", conn, schema="ouro", if_exists="append", index=False)

    print(f"Ouro (fato_ot) atualizada: {len(df_final)} linhas gravadas.")


with DAG(
    dag_id="carga_indicadores_ot",
    schedule="@monthly",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["indicadores", "ot"],
) as dag:

    tarefa_estrutura = PythonOperator(task_id="garantir_estrutura", python_callable=garantir_estrutura)
    tarefa_ouro = PythonOperator(task_id="carregar_e_publicar_ouro", python_callable=carregar_e_publicar_ouro)

    tarefa_estrutura >> tarefa_ouro