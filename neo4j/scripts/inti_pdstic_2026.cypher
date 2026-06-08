// Criando as linhas de ações do PDSTIC e as dotações orçamentárias

CALL apoc.load.json("file:///acoes_pdstic.json") YIELD value AS linhas
UNWIND linhas AS laData
WITH laData
WHERE laData.recursos IS NOT NULL AND size(laData.recursos) > 0

MERGE (la:LinhaAcaoPDSTIC {numero_linha: toInteger(laData.numero_linha)})
SET
  la.titulo = coalesce(laData.titulo, 'Sem título'),
  la.descricao = coalesce(laData.descricao, 'Sem descrição'),
  la.status = coalesce(laData.status, 'Indefinido'),
  la.concluido = coalesce(laData.concluido, ''),
  la.comentario = coalesce(laData.comentario, ''),
  la.periodo_inicio = coalesce(laData.periodo[0], ''),
  la.periodo_fim = CASE
    WHEN laData.periodo IS NOT NULL AND size(laData.periodo) > 1 THEN laData.periodo[1]
    ELSE ''
  END,
  la.projeto_estrategico = coalesce(laData.projeto_estrategico, '')

WITH la, laData
UNWIND laData.recursos AS recurso
WITH la, recurso
WHERE recurso.dotacao_orcamentaria IS NOT NULL
  AND trim(recurso.dotacao_orcamentaria) <> ''
  AND recurso.vlr_total IS NOT NULL

WITH
  la,
  recurso.dotacao_orcamentaria AS dotacao,
  sum(toFloat(recurso.vlr_total)) AS vlr_total_agrupado
WHERE vlr_total_agrupado > 0

MERGE (do:DotacaoOrcamentaria {dotacao: dotacao})
MERGE (la)-[rel:PLANEJADO_USAR]->(do)
SET
  rel.linha_numero = la.numero_linha,
  rel.vlr_total = vlr_total_agrupado;

// Atualiza o valor_pdstic nas dotações orçamentárias
MATCH (:LinhaAcaoPDSTIC)-[rel:PLANEJADO_USAR]->(do:DotacaoOrcamentaria)
WITH do, sum(rel.vlr_total) AS valor_planejado_total
SET do.valor_pdstic = valor_planejado_total;

// Cria o nó PDSTIC 2026 (MERGE garante idempotência)
MERGE (pdstic:PDSTIC {ano: 2026})
ON CREATE SET
  pdstic.nome = 'PDSTIC 2026',
  pdstic.criado_em = datetime()
WITH pdstic
MATCH (la:LinhaAcaoPDSTIC)
MERGE (la)-[:PLANEJADA_PARA]->(pdstic)
WITH pdstic, count(la) AS totalLinhas
SET pdstic.total_linhas_planejadas = totalLinhas;

MATCH (pdstic:PDSTIC {ano: 2026})
RETURN 
  pdstic.ano AS ano,
  pdstic.total_linhas_planejadas AS linhasRelacionadas,
  labels(pdstic) AS labels;