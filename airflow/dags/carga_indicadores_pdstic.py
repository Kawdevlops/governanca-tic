import os
import pandas as pd
from sqlalchemy import create_engine, text
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

CAMINHO_EXCEL = "/opt/airflow/saidas/PDSTIC.xlsx"

def conectar():
    return create_engine(
        f"postgresql+psycopg2://{os.environ['DB_ETL_USER']}:{os.environ['DB_ETL_PASSWORD']}"
        f"@{os.environ['DB_STREAMLIT_HOST']}:{os.environ['DB_STREAMLIT_PORT']}/{os.environ['DB_STREAMLIT_DATABASE']}"
    )

PASTA_SQL_SETUP = "/opt/airflow/sql_setup"
ARQUIVOS_ESTRUTURA = [
    "schema_bronze_prata_ouro.sql",
    "tabela_bronze_ot.sql",
    "tabela_bronze_pdstic.sql",
    "tabela_prata.sql",
    "extender_prata_pdstic.sql",
    "tabela_ouro.sql",
    "tabela_ouro_pdstic.sql",
]


def garantir_estrutura():
    engine = conectar()
    with engine.begin() as conn:
        for nome_arquivo in ARQUIVOS_ESTRUTURA:
            caminho = os.path.join(PASTA_SQL_SETUP, nome_arquivo)
            if not os.path.exists(caminho):
                print(f"Aviso: {nome_arquivo} não encontrado, pulando.")
                continue
            with open(caminho, "r", encoding="utf-8") as f:
                sql = f.read()
            conn.execute(text(sql))
            print(f"Estrutura aplicada: {nome_arquivo}")
def carregar_bronze():
    engine = conectar()


def carregar_bronze():
    engine = conectar()

    # CRIAÇÃO DOS SCHEMAS (Garante que bronze, prata e ouro existam)
        # -------------------------------------------------------------
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS prata;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS ouro;"))

    df = pd.read_excel(CAMINHO_EXCEL, sheet_name="Página1")
    df = df.rename(columns={
        "Número": "numero",
        "Linha de Ação": "linha_acao",
        "Objeto": "objeto",
        "Área Responsável": "area_responsavel",
        "Público Alvo": "publico_alvo",
        "Percentual Executado": "percentual_executado",
        "Comentário": "comentario",
        "Prazo da Contratação": "prazo_contratacao",
        "Número do SEI": "numero_sei",
        "Dotação Orçamentária": "dotacao_orcamentaria",
        "Orçamento Previsto no PDSTIC": "orcamento_previsto_pdstic",
        "Dotação Orçamentária da Contratação": "dotacao_orcamentaria_contratacao",
        "Projeto/Atividade": "projeto_atividade",
        "Orçamento Previsto no GC": "orcamento_previsto_gc",
        "Orçamento Liquidado": "orcamento_liquidado",
        "Observações": "observacoes",
    })
    colunas_bronze = [
        "numero", "linha_acao", "objeto", "area_responsavel", "publico_alvo",
        "percentual_executado", "comentario", "prazo_contratacao", "numero_sei",
        "dotacao_orcamentaria", "orcamento_previsto_pdstic",
        "dotacao_orcamentaria_contratacao", "projeto_atividade",
        "orcamento_previsto_gc", "orcamento_liquidado", "observacoes",
    ]
    df = df[colunas_bronze].dropna(subset=["numero"])
    df["fonte_arquivo"] = "PDSTIC.xlsx"
    df.to_sql("pdstic_bruto", engine, schema="bronze", if_exists="replace", index=False)
    print(f"Bronze: {len(df)} linhas gravadas.")


def carregar_prata():
    engine = conectar()
    sql_upsert_prata = text("""
        INSERT INTO prata.indicadores_padrao (
            indicador, subcategoria, subcategoria_titulo, segmento, item_avaliado,
            responsavel, status_bruto, evidencia, observacoes,
            valor_previsto, valor_realizado,
            chave_natural, hash_conteudo, fonte_arquivo
        )
        SELECT
            'PDSTIC' AS indicador,
            area_responsavel AS subcategoria,
            area_responsavel AS subcategoria_titulo,
            objeto AS segmento,
            linha_acao AS item_avaliado,
            area_responsavel AS responsavel,
            percentual_executado::text AS status_bruto,
            numero_sei AS evidencia,
            observacoes,
            orcamento_previsto_pdstic AS valor_previsto,
            orcamento_liquidado AS valor_realizado,
            encode(digest('PDSTIC|' || COALESCE(numero::text, '') || '|' || COALESCE(objeto, linha_acao, ''), 'sha256'), 'hex') AS chave_natural,
            encode(digest(
                COALESCE(percentual_executado::text, '') || '|' ||
                COALESCE(orcamento_liquidado::text, ''),
                'sha256'
            ), 'hex') AS hash_conteudo,
            fonte_arquivo
        FROM bronze.pdstic_bruto
        ON CONFLICT (chave_natural) DO UPDATE
            SET status_bruto     = EXCLUDED.status_bruto,
                evidencia        = EXCLUDED.evidencia,
                observacoes      = EXCLUDED.observacoes,
                valor_previsto   = EXCLUDED.valor_previsto,
                valor_realizado  = EXCLUDED.valor_realizado,
                hash_conteudo    = EXCLUDED.hash_conteudo,
                data_ingestao    = now()
            WHERE prata.indicadores_padrao.hash_conteudo IS DISTINCT FROM EXCLUDED.hash_conteudo;
    """)
    with engine.begin() as conn:
        conn.execute(sql_upsert_prata)
    print("Prata: upsert concluído.")


def atualizar_ouro():
    engine = conectar()
    sql_atualizar_ouro = text("""
        TRUNCATE ouro.fato_pdstic;
        INSERT INTO ouro.fato_pdstic (
            chave_natural, area_responsavel, objeto, linha_acao, status,
            percentual_executado, valor_previsto, valor_realizado, diferenca
        )
        SELECT
            chave_natural,
            subcategoria AS area_responsavel,
            segmento AS objeto,
            item_avaliado AS linha_acao,
            CASE
                WHEN status_bruto ~ '^[0-9]+(\.[0-9]+)?$' AND status_bruto::numeric >= 1 THEN 'Concluída'
                WHEN status_bruto ~ '^[0-9]+(\.[0-9]+)?$' AND status_bruto::numeric = 0 THEN 'Não Iniciada'
                ELSE 'Em Andamento'
            END AS status,
            CASE 
                WHEN status_bruto ~ '^[0-9]+(\.[0-9]+)?$' THEN status_bruto::numeric
                ELSE NULL
            END AS percentual_executado,
            valor_previsto,
            valor_realizado,
            COALESCE(valor_previsto, 0) - COALESCE(valor_realizado, 0) AS diferenca
        FROM prata.indicadores_padrao
        WHERE indicador = 'PDSTIC';
    """)
    with engine.begin() as conn:
        conn.execute(sql_atualizar_ouro)
    print("Ouro atualizada.")


with DAG(
    dag_id="carga_indicadores_pdstic",
    schedule="@monthly",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["indicadores", "pdstic"],
) as dag:

        tarefa_estrutura = PythonOperator(task_id="garantir_estrutura", python_callable=garantir_estrutura)
        tarefa_bronze = PythonOperator(task_id="carregar_bronze", python_callable=carregar_bronze)
        tarefa_prata = PythonOperator(task_id="carregar_prata", python_callable=carregar_prata)
        tarefa_ouro = PythonOperator(task_id="atualizar_ouro", python_callable=atualizar_ouro)

        tarefa_estrutura >> tarefa_bronze >> tarefa_prata >> tarefa_ouro