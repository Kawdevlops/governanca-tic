import os
import pandas as pd
from sqlalchemy import create_engine, text

CAMINHO_EXCEL = "streamlit/saidas/PDSTIC.xlsx"

engine = create_engine(
    f"postgresql+psycopg2://{os.environ['DB_STREAMLIT_USER']}:{os.environ['DB_STREAMLIT_PASSWORD']}"
    f"@{os.environ['DB_STREAMLIT_HOST']}:{os.environ['DB_STREAMLIT_PORT']}/{os.environ['DB_STREAMLIT_DATABASE']}"
)

# 1) Lê o Excel e renomeia as colunas para o padrão da tabela Bronze
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

# 2) Da Bronze para a Prata (tabela padrão compartilhada com o OT)
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
        encode(digest('PDSTIC|' || numero || '|' || objeto, 'sha256'), 'hex') AS chave_natural,
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

# 3) Da Prata para a Ouro: aplica a régua (mesma lógica do card do Power BI)
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
            WHEN status_bruto::numeric = 1 THEN 'Concluída'
            WHEN status_bruto::numeric = 0 THEN 'Não Iniciada'
            ELSE 'Em Andamento'
        END AS status,
        status_bruto::numeric AS percentual_executado,
        valor_previsto,
        valor_realizado,
        COALESCE(valor_previsto, 0) - COALESCE(valor_realizado, 0) AS diferenca
    FROM prata.indicadores_padrao
    WHERE indicador = 'PDSTIC';
""")

with engine.begin() as conn:
    conn.execute(sql_atualizar_ouro)
    print("Ouro atualizada.")