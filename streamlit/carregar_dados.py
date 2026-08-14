import os
import pandas as pd
from sqlalchemy import create_engine, text

CAMINHO_EXCEL = "streamlit/saidas/base_consolidada_validada.xlsx"

engine = create_engine(
    f"postgresql+psycopg2://{os.environ['DB_STREAMLIT_USER']}:{os.environ['DB_STREAMLIT_PASSWORD']}"
    f"@{os.environ['DB_STREAMLIT_HOST']}:{os.environ['DB_STREAMLIT_PORT']}/{os.environ['DB_STREAMLIT_DATABASE']}"
)

df = pd.read_excel(CAMINHO_EXCEL, sheet_name="Sheet1")

df = df.rename(columns={
    "SEGMENTO": "segmento",
    "RECOMENDACAO": "recomendacao",
    "PESSOA_CONTATO": "pessoa_contato",
    "DATA_VERIFICACAO_CUMPRIMENTO": "data_verificacao",
    "CUMPRIDA_TOTALMENTE": "cumprida_totalmente",
    "CUMPRIDA_PARCIALMENTE": "cumprida_parcialmente",
    "NAO_CUMPRIDA": "nao_cumprida",
    "EVIDENCIAS_CUMPRIMENTO": "evidencias",
    "OBSERVACOES": "observacoes",
    "OT": "ot",
    "OT_TITULO": "ot_titulo",
})

colunas_bronze = [
    "segmento", "recomendacao", "pessoa_contato", "data_verificacao",
    "cumprida_totalmente", "cumprida_parcialmente", "nao_cumprida",
    "evidencias", "observacoes", "ot", "ot_titulo",
]
df = df[colunas_bronze]
df["fonte_arquivo"] = "base_consolidada_validada.xlsx"

df.to_sql("ot_bruto", engine, schema="bronze", if_exists="replace", index=False)
print(f"Bronze: {len(df)} linhas gravadas.")

sql_upsert_prata = text("""
    INSERT INTO prata.indicadores_padrao (
        indicador, subcategoria, subcategoria_titulo, segmento, item_avaliado,
        responsavel, data_avaliacao, status_bruto, evidencia, observacoes,
        chave_natural, hash_conteudo, fonte_arquivo
    )
    SELECT
        'OT' AS indicador,
        ot AS subcategoria,
        ot_titulo AS subcategoria_titulo,
        segmento,
        recomendacao AS item_avaliado,
        pessoa_contato AS responsavel,
        data_verificacao AS data_avaliacao,
        CASE
            WHEN cumprida_totalmente   THEN 'Cumprida Totalmente'
            WHEN cumprida_parcialmente THEN 'Cumprida Parcialmente'
            WHEN nao_cumprida          THEN 'Não Cumprida'
            ELSE 'Indefinido'
        END AS status_bruto,
        evidencias AS evidencia,
        observacoes,
        encode(digest('OT|' || ot || '|' || segmento || '|' || recomendacao, 'sha256'), 'hex') AS chave_natural,
        encode(digest(
            (CASE
                WHEN cumprida_totalmente   THEN 'Cumprida Totalmente'
                WHEN cumprida_parcialmente THEN 'Cumprida Parcialmente'
                WHEN nao_cumprida          THEN 'Não Cumprida'
                ELSE 'Indefinido'
            END) || '|' || COALESCE(data_verificacao::text, ''),
            'sha256'
        ), 'hex') AS hash_conteudo,
        fonte_arquivo
    FROM bronze.ot_bruto
    ON CONFLICT (chave_natural) DO UPDATE
        SET status_bruto   = EXCLUDED.status_bruto,
            evidencia      = EXCLUDED.evidencia,
            observacoes    = EXCLUDED.observacoes,
            data_avaliacao = EXCLUDED.data_avaliacao,
            hash_conteudo  = EXCLUDED.hash_conteudo,
            data_ingestao  = now()
        WHERE prata.indicadores_padrao.hash_conteudo IS DISTINCT FROM EXCLUDED.hash_conteudo;
""")

with engine.begin() as conn:
    conn.execute(sql_upsert_prata)
    print("Prata: upsert concluído.")

sql_atualizar_ouro = text("""
    TRUNCATE ouro.fato_ot;
    INSERT INTO ouro.fato_ot (chave_natural, ot, ot_titulo, segmento, status, data_avaliacao)
    SELECT chave_natural, subcategoria, subcategoria_titulo, segmento, status_bruto, data_avaliacao
    FROM prata.indicadores_padrao
    WHERE indicador = 'OT';
""")

with engine.begin() as conn:
    conn.execute(sql_atualizar_ouro)
    print("Ouro atualizada.")