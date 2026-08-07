#!/bin/bash

echo "Executando inicialização..."

echo "Criando constraints..."
cypher-shell -a bolt://neo4j:7687 \
  -u "$DB_NEO4J_USER" \
  -p "$DB_NEO4J_PASSWORD" \
  -d "$DB_NEO4J_DATABASE" \
  -f /scripts/init_constraints.cypher

echo "Criando smsub e unidades..."
cypher-shell -a bolt://neo4j:7687 \
  -u "$DB_NEO4J_USER" \
  -p "$DB_NEO4J_PASSWORD" \
  -d "$DB_NEO4J_DATABASE" \
  -f /scripts/init_smsub_unidades.cypher

echo "Criando subprefeituras..."
cypher-shell -a bolt://neo4j:7687 \
  -u "$DB_NEO4J_USER" \
  -p "$DB_NEO4J_PASSWORD" \
  -d "$DB_NEO4J_DATABASE" \
  -f /scripts/init_subprefeituras.cypher

echo "Criando PDSTIC 2026..."
cypher-shell -a bolt://neo4j:7687 \
  -u "$DB_NEO4J_USER" \
  -p "$DB_NEO4J_PASSWORD" \
  -d "$DB_NEO4J_DATABASE" \
  -f /scripts/init_pdstic_2026.cypher

echo "Finalizado."