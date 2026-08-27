"""
DAG: carga_indicadores_pdstic

Lê a planilha do PDSTIC, transforma tudo em memória com pandas e grava
direto na tabela final `ouro.fato_pdstic`.
"""
import hashlib
import os
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text

from airflow import DAG
from airflow.operators.python import PythonOperator

CAMINHO_EXCEL = "/opt/airflow/saidas/PDSTIC.xlsx"

PASTA_SQL_SETUP = "/opt/airflow/sql_setup"

ARQUIVOS_ESTRUTURA = [
    "schema_ouro.sql",
    "tabela_ouro_pdstic.sql",
]


def conectar():
    return create_engine(
        f"postgresql+psycopg2://{os.environ['DB_STREAMLIT_USER']}:{os.environ['DB_STREAMLIT_PASSWORD']}"
        f"@{os.environ['DB_STREAMLIT_HOST']}:{os.environ['DB_STREAMLIT_PORT']}/{os.environ['DB_STREAMLIT_DATABASE']}"
    )


def garantir_estrutura():
    """Cria o schema `ouro` e a tabela `ouro.fato_pdstic`, se ainda não existirem."""
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


def _calcular_status(percentual) -> str:
    """Mesma regra que antes era um CASE WHEN em SQL sobre status_bruto."""
    if pd.isna(percentual):
        return "Em Andamento"
    if percentual >= 1:
        return "Concluída"
    if percentual == 0:
        return "Não Iniciada"
    return "Em Andamento"


def _calcular_chave_natural(row) -> str:
    """
    Mesmo hash (SHA-256) que antes era gerado pelo Postgres via
    `digest('PDSTIC|' || numero || '|' || COALESCE(objeto, linha_acao), 'sha256')`.
    """
    identificador = row["objeto"] if pd.notna(row["objeto"]) else row["linha_acao"]
    texto = f"PDSTIC|{row['numero']}|{identificador or ''}"
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def carregar_e_publicar_ouro():
    engine = conectar()

    df = pd.read_excel(CAMINHO_EXCEL, sheet_name="Página1")
    df = df.rename(columns={
        "Número": "numero",
        "Linha de Ação": "linha_acao",
        "Objeto": "objeto",
        "Área Responsável": "area_responsavel",
        "Percentual Executado": "percentual_executado",
        "Orçamento Previsto no PDSTIC": "valor_previsto",
        "Orçamento Liquidado": "valor_realizado",
    })
    df = df.dropna(subset=["numero"])

    # Garante que percentual/valores sejam numéricos (o Excel às vezes traz texto).
    df["percentual_executado"] = pd.to_numeric(df["percentual_executado"], errors="coerce")
    df["valor_previsto"] = pd.to_numeric(df["valor_previsto"], errors="coerce")
    df["valor_realizado"] = pd.to_numeric(df["valor_realizado"], errors="coerce")

    # Monta as colunas finais que a tabela ouro.fato_pdstic espera.
    df["status"] = df["percentual_executado"].apply(_calcular_status)
    df["diferenca"] = df["valor_previsto"].fillna(0) - df["valor_realizado"].fillna(0)
    df["chave_natural"] = df.apply(_calcular_chave_natural, axis=1)

    df_final = df[[
        "chave_natural", "area_responsavel", "objeto", "linha_acao", "status",
        "percentual_executado", "valor_previsto", "valor_realizado", "diferenca",
    ]]

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE ouro.fato_pdstic;"))
        df_final.to_sql("fato_pdstic", conn, schema="ouro", if_exists="append", index=False)

    print(f"Ouro (fato_pdstic) atualizada: {len(df_final)} linhas gravadas.")


with DAG(
    dag_id="carga_indicadores_pdstic",
    schedule="@monthly",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["indicadores", "pdstic"],
) as dag:

    tarefa_estrutura = PythonOperator(task_id="garantir_estrutura", python_callable=garantir_estrutura)
    tarefa_ouro = PythonOperator(task_id="carregar_e_publicar_ouro", python_callable=carregar_e_publicar_ouro)

    tarefa_estrutura >> tarefa_ouro