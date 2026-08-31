CREATE TABLE IF NOT EXISTS ouro.fato_ot (
    chave_natural   TEXT PRIMARY KEY,
    ot              TEXT,
    ot_titulo       TEXT,
    segmento        TEXT,
    status          TEXT,
    data_avaliacao  DATE
);

-- Colunas novas: já existiam no Excel (PESSOA_CONTATO, TEM_EVIDENCIA) mas não
-- eram trazidas pro banco. ADD COLUMN IF NOT EXISTS é seguro mesmo se a
-- tabela já existir de uma execução anterior (não apaga dado nenhum).
ALTER TABLE ouro.fato_ot ADD COLUMN IF NOT EXISTS pessoa_contato TEXT;
ALTER TABLE ouro.fato_ot ADD COLUMN IF NOT EXISTS tem_evidencia  TEXT;
ALTER TABLE ouro.fato_ot ADD COLUMN IF NOT EXISTS evidencias_cumprimento TEXT;
ALTER TABLE ouro.fato_ot ADD COLUMN IF NOT EXISTS observacoes TEXT;
ALTER TABLE ouro.fato_ot ADD COLUMN IF NOT EXISTS recomendacao TEXT;