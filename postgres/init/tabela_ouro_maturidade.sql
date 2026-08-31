CREATE TABLE IF NOT EXISTS ouro.fato_maturidade (
    codigo_orgao          INTEGER PRIMARY KEY,
    nome_orgao            TEXT,
    sigla_orgao           TEXT,
    pontos_obtidos        INTEGER,
    pontos_possiveis      INTEGER,
    percentual_obtido     NUMERIC,
    pontos_faltantes       INTEGER,
    nivel_maturidade       TEXT,
    ultima_data_avaliacao  TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ouro.fato_maturidade_pilares (
    codigo_orgao       INTEGER,
    codigo_pilar       TEXT,
    nome_pilar         TEXT,
    pontos_obtidos     INTEGER,
    pontos_possiveis   INTEGER,
    percentual_obtido  NUMERIC,
    PRIMARY KEY (codigo_orgao, codigo_pilar)
);