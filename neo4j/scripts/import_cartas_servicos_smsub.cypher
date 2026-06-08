CALL apoc.load.json("file:///lista_cartas_servico_smsub.json") YIELD value
RETURN value.codigo_servico, value.titulo, value.caminho_servico

CALL apoc.load.json("file:///lista_cartas_servico_smsub.json") YIELD value
MERGE (c:CartaServico {name: value.codigo_servico})
SET c.link = value.link,
    c.data_hora_extracao = value.data_hora_extracao
RETURN count(c) AS total_cartas

CALL apoc.load.json("file:///lista_cartas_servico_smsub.json") YIELD value
WITH value
WHERE value.caminho_servico IS NOT NULL AND size(value.caminho_servico) = 2
MERGE (s1:ServicoOnline {name: value.caminho_servico[0]})
MERGE (s2:ServicoOnline {name: value.caminho_servico[1]})
RETURN count(*) AS registros_processados

CALL apoc.load.json("file:///lista_cartas_servico_smsub.json") YIELD value
WITH value
WHERE value.caminho_servico IS NOT NULL AND size(value.caminho_servico) = 2

MATCH (p:Portal {name: "SP156"})
MERGE (s1:ServicoOnline {name: value.caminho_servico[0]})
MERGE (s2:ServicoOnline {name: value.caminho_servico[1]})
MERGE (c:CartaServico {name: value.codigo_servico})

ON CREATE SET c.link = value.link,
              c.data_hora_extracao = value.data_hora_extracao,
              c.caminho_servico = value.caminho_servico
ON MATCH SET  c.link = value.link,
              c.data_hora_extracao = value.data_hora_extracao,
              c.caminho_servico = value.caminho_servico

MERGE (p)-[:DISPONIBILIZA]->(s1)
MERGE (s1)-[:DISPONIBILIZA]->(s2)
MERGE (s2)-[:DISPONIBILIZA]->(c)

RETURN count(*) AS relacionamentos_processados