-- Banco isolado para os indicadores (OT, PDSTIC, Maturidade...), separado do banco do Airflow
CREATE DATABASE indicadores_tic;

-- Conectar ao banco recém-criado
\c indicadores_tic;

-- Criar o usuário
CREATE USER indicadores_user WITH ENCRYPTED PASSWORD 'Indic2026';

-- Conceder permissões no banco
GRANT ALL PRIVILEGES ON DATABASE indicadores_tic TO indicadores_user;

-- Criar e conceder permissões no schema da camada de dados final (Ouro).
-- Bronze e Prata foram removidos: as DAGs agora transformam tudo em
-- memória com pandas e gravam direto na camada final.
CREATE SCHEMA IF NOT EXISTS ouro;

GRANT ALL ON SCHEMA public, ouro TO indicadores_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public, ouro TO indicadores_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public, ouro TO indicadores_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public, ouro TO indicadores_user;

-- Garantir que tabelas criadas no futuro nesse schema pertençam ao usuário
ALTER DEFAULT PRIVILEGES IN SCHEMA public, ouro GRANT ALL ON TABLES TO indicadores_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public, ouro GRANT ALL ON SEQUENCES TO indicadores_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public, ouro GRANT ALL ON FUNCTIONS TO indicadores_user;

-- Definir schemas padrão para busca de tabelas
ALTER ROLE indicadores_user SET search_path TO public, ouro;