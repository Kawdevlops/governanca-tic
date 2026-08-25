import os
from datetime import datetime

import pandas as pd
import requests
from sqlalchemy import create_engine, text

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


BASE_URL_PADRAO = (
    "http://ec2-18-229-112-109.sa-east-1.compute.amazonaws.com/api/public"
)

# Código do órgão da SMSUB na base FATIMA/PETIC.
CODIGO_ORGAO_SMSUB = 39

PASTA_SQL_SETUP = "/opt/airflow/sql_setup"

ARQUIVOS_ESTRUTURA = [
    "tabela_bronze_maturidade.sql",
    "tabela_ouro_maturidade.sql",
]


def conectar():
    return create_engine(
        f"postgresql+psycopg2://{os.environ['DB_ETL_USER']}:{os.environ['DB_ETL_PASSWORD']}"
        f"@{os.environ['DB_STREAMLIT_HOST']}:{os.environ['DB_STREAMLIT_PORT']}"
        f"/{os.environ['DB_STREAMLIT_DATABASE']}"
    )


def garantir_estrutura():
    engine = conectar()

    with engine.begin() as conn:
        for nome_arquivo in ARQUIVOS_ESTRUTURA:
            caminho = os.path.join(PASTA_SQL_SETUP, nome_arquivo)

            if not os.path.exists(caminho):
                print(f"Aviso: {nome_arquivo} não encontrado, pulando.")
                continue

            with open(caminho, "r", encoding="utf-8") as arquivo:
                sql = arquivo.read()

            conn.execute(text(sql))
            print(f"Estrutura aplicada: {nome_arquivo}")


def buscar_dados_api() -> dict:
    url = os.environ.get("MATURIDADE_API_BASE_URL", BASE_URL_PADRAO)

    resposta = requests.get(
        f"{url}/obter-pontos-criterios-orgao",
        params={"codigo_orgao": CODIGO_ORGAO_SMSUB},
        timeout=30,
    )
    resposta.raise_for_status()

    dados = resposta.json()["pontos_criterios_orgao"]

    if not dados:
        raise ValueError("API retornou pontos_criterios_orgao vazio.")

    return dados


def carregar_bronze():
    engine = conectar()
    dados = buscar_dados_api()
    orgao = dados["orgao"]

    df_org = pd.DataFrame(
        [
            {
                "codigo_orgao": orgao["codigo"],
                "nome_orgao": orgao["nome"],
                "sigla_orgao": orgao["sigla"],
                "pontos_obtidos": dados["pontos_obtidos"],
                "pontos_possiveis": dados["pontos_possiveis"],
                "percentual_obtido": dados["percentual_obtido"],
                "nivel_maturidade": dados["nivel_maturidade"],
                "ultima_data_avaliacao": dados["ultima_data_avaliacao"],
            }
        ]
    )

    # A API entrega a data como texto ISO.
    # Convertemos explicitamente antes de gravar na Bronze.
    df_org["ultima_data_avaliacao"] = pd.to_datetime(
        df_org["ultima_data_avaliacao"],
        errors="raise",
    )

    linhas_pilares = [
        {
            "codigo_orgao": orgao["codigo"],
            "codigo_pilar": int(pilar["codigo_pilar"]),
            "nome_pilar": pilar["nome_pilar"],
            "pontos_obtidos": pilar["pontos_obtidos"],
            "pontos_possiveis": pilar["pontos_possiveis"],
            "percentual_obtido": pilar["percentual_obtido"],
        }
        for pilar in dados["pilares"]
    ]

    df_pilares = pd.DataFrame(linhas_pilares)

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM bronze.maturidade_bruto;"))
        conn.execute(text("DELETE FROM bronze.maturidade_pilares_bruto;"))

    df_org.to_sql(
        "maturidade_bruto",
        engine,
        schema="bronze",
        if_exists="append",
        index=False,
    )

    df_pilares.to_sql(
        "maturidade_pilares_bruto",
        engine,
        schema="bronze",
        if_exists="append",
        index=False,
    )

    print(
        f"Bronze: 1 órgão, {len(df_pilares)} pilares gravados. "
        f"Última avaliação: {df_org['ultima_data_avaliacao'].iloc[0]}"
    )


def atualizar_ouro():
    engine = conectar()

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM ouro.fato_maturidade;"))

        conn.execute(
            text(
                """
                INSERT INTO ouro.fato_maturidade (
                    codigo_orgao,
                    nome_orgao,
                    sigla_orgao,
                    pontos_obtidos,
                    pontos_possiveis,
                    percentual_obtido,
                    pontos_faltantes,
                    nivel_maturidade,
                    ultima_data_avaliacao
                )
                SELECT
                    codigo_orgao,
                    nome_orgao,
                    sigla_orgao,
                    pontos_obtidos,
                    pontos_possiveis,
                    percentual_obtido,
                    pontos_possiveis - pontos_obtidos,
                    nivel_maturidade,
                    ultima_data_avaliacao::timestamp
                FROM bronze.maturidade_bruto;
                """
            )
        )

        conn.execute(text("DELETE FROM ouro.fato_maturidade_pilares;"))

        conn.execute(
            text(
                """
                INSERT INTO ouro.fato_maturidade_pilares (
                    codigo_orgao,
                    codigo_pilar,
                    nome_pilar,
                    pontos_obtidos,
                    pontos_possiveis,
                    percentual_obtido
                )
                SELECT
                    codigo_orgao,
                    codigo_pilar,
                    nome_pilar,
                    pontos_obtidos,
                    pontos_possiveis,
                    percentual_obtido
                FROM bronze.maturidade_pilares_bruto;
                """
            )
        )

    print("Ouro atualizada com sucesso.")


with DAG(
    dag_id="carga_indicadores_maturidade",
    schedule="@monthly",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["indicadores", "maturidade"],
) as dag:

    tarefa_estrutura = PythonOperator(
        task_id="garantir_estrutura",
        python_callable=garantir_estrutura,
    )

    tarefa_bronze = PythonOperator(
        task_id="carregar_bronze",
        python_callable=carregar_bronze,
    )

    tarefa_ouro = PythonOperator(
        task_id="atualizar_ouro",
        python_callable=atualizar_ouro,
    )

    tarefa_estrutura >> tarefa_bronze >> tarefa_ouro
