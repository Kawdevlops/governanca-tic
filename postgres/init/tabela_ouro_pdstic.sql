-- Cria uma nova tabela ouro para PDSTIC

CREATE TABLE IF NOT EXISTS ouro.fato_pdstic (
    chave_natural         TEXT PRIMARY KEY,
    area_responsavel      TEXT,
    objeto                TEXT,
    linha_acao            TEXT,
    status                TEXT,
    percentual_executado  NUMERIC,
    valor_previsto        NUMERIC,
    valor_realizado       NUMERIC,
    diferenca             NUMERIC
);

-- Colunas novas: já existiam no Excel (Comentário, Prazo da Contratação,
-- Número do SEI, Dotação Orçamentária, Público Alvo) mas não eram trazidas
-- pro banco. ADD COLUMN IF NOT EXISTS é seguro mesmo se a tabela já existir.
ALTER TABLE ouro.fato_pdstic ADD COLUMN IF NOT EXISTS publico_alvo       TEXT;
ALTER TABLE ouro.fato_pdstic ADD COLUMN IF NOT EXISTS comentario         TEXT;
ALTER TABLE ouro.fato_pdstic ADD COLUMN IF NOT EXISTS prazo_contratacao  DATE;
ALTER TABLE ouro.fato_pdstic ADD COLUMN IF NOT EXISTS numero_sei         TEXT;
ALTER TABLE ouro.fato_pdstic ADD COLUMN IF NOT EXISTS dotacao_orcamentaria TEXT;
ALTER TABLE ouro.fato_pdstic ADD COLUMN IF NOT EXISTS dotacao_contratacao TEXT;
ALTER TABLE ouro.fato_pdstic ADD COLUMN IF NOT EXISTS projeto_atividade TEXT;
ALTER TABLE ouro.fato_pdstic ADD COLUMN IF NOT EXISTS orcamento_previsto_gc NUMERIC;