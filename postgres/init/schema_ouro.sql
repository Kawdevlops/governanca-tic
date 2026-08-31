-- Cria só o schema "ouro" (bronze e prata foram removidos do projeto:
-- agora as DAGs transformam tudo em memória com pandas e gravam direto
-- na camada final).

CREATE SCHEMA IF NOT EXISTS ouro;

GRANT ALL ON SCHEMA ouro TO indicadores_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ouro GRANT ALL ON TABLES TO indicadores_user;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
