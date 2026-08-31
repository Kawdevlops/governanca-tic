"""
DAG: carga_indicadores_ot

Lê a planilha de OT (Orientações Técnicas), transforma tudo em memória com
pandas e grava direto na tabela final `ouro.fato_ot`.

Antes esse pipeline passava por 3 camadas (bronze -> prata -> ouro), cada
uma virando uma tabela no Postgres. Isso foi simplificado: agora só existe
a camada ouro no banco. As transformações que antes eram feitas em SQL
(dentro das camadas bronze/prata) agora são feitas aqui em Python, com
pandas, antes de gravar.
"""
import hashlib
import os
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text

from airflow import DAG
from airflow.operators.python import PythonOperator

CAMINHO_EXCEL = "/opt/airflow/saidas/base_consolidada_validada.xlsx"

PASTA_SQL_SETUP = "/opt/airflow/sql_setup"

# Só precisa garantir o schema "ouro" e a própria tabela ouro.fato_ot.
# (Antes essa lista também criava bronze/prata e as tabelas da outra DAG;
# agora cada DAG cuida só da sua própria tabela ouro.)
ARQUIVOS_ESTRUTURA = [
    "schema_ouro.sql",
    "tabela_ouro.sql",
]


def conectar():
    return create_engine(
        f"postgresql+psycopg2://{os.environ['DB_STREAMLIT_USER']}:{os.environ['DB_STREAMLIT_PASSWORD']}"
        f"@{os.environ['DB_STREAMLIT_HOST']}:{os.environ['DB_STREAMLIT_PORT']}/{os.environ['DB_STREAMLIT_DATABASE']}"
    )


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
    """
    Mesmo hash (SHA-256) que antes era gerado pelo Postgres via
    `digest('OT|' || ot || '|' || segmento || '|' || recomendacao, 'sha256')`.
    Calculado aqui em Python pra não depender mais da extensão pgcrypto
    numa camada intermediária — o resultado final é idêntico.
    """
    texto = f"OT|{row['ot']}|{row['segmento']}|{row['recomendacao']}"
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def carregar_e_publicar_ouro():
    """
    Lê o Excel, aplica as mesmas transformações que antes ficavam na camada
    prata (status calculado, chave natural), e grava direto em
    `ouro.fato_ot` — substituindo o conteúdo antigo (TRUNCATE + INSERT).
    """
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
        # Colunas que já existiam no Excel, mas antes eram descartadas:
        "PESSOA_CONTATO": "pessoa_contato",
        "TEM_EVIDENCIA": "tem_evidencia",
        "EVIDENCIAS_CUMPRIMENTO": "evidencias_cumprimento",
        "OBSERVACOES": "observacoes",
    })

    # Monta as colunas finais que a tabela ouro.fato_ot espera:
    # chave_natural, ot, ot_titulo, segmento, status, data_avaliacao,
    # pessoa_contato, tem_evidencia, evidencias_cumprimento, observacoes,
    # recomendacao
    df["status"] = df.apply(_calcular_status, axis=1)
    df["chave_natural"] = df.apply(_calcular_chave_natural, axis=1)

    df_final = df[[
        "chave_natural", "ot", "ot_titulo", "segmento", "status", "data_avaliacao",
        "pessoa_contato", "tem_evidencia", "evidencias_cumprimento", "observacoes",
        "recomendacao",
    ]]

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