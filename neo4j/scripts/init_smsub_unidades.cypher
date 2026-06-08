// Criando a SMSUB
MERGE (o:OrgaoSetorial {name: 'SMSUB'})
SET o.sigla = 'SMSUB'

// Importando as unidades de SMSUB com base no arquivo CSV
//CALL apoc.load.csv("file:///smsub_unidades.csv", {header: true}) YIELD map
LOAD CSV WITH HEADERS
FROM "file:///smsub_unidades.csv"
AS map

MERGE (u:Unidade {name: map.sigla})
SET u.sigla = map.sigla,
    u.tipo = map.tipo,
    u.norma = map.norma,
    u.artigo = map.artigo
MERGE (p {name: map.pertence_a})
MERGE (u)-[:PERTENCE_A]->(p);