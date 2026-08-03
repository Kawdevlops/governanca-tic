from neo4j import AsyncDriver
from app.models.risco import RiscoCreate, RiscoResponse, RiscoVinculo


_RETURN_RISCO = """
    RETURN
        elementId(r)          AS element_id,
        r.identificador       AS identificador,
        r.nome                AS nome,
        r.descricao           AS descricao,
        r.categoria           AS categoria,
        r.probabilidade       AS probabilidade,
        r.impacto             AS impacto,
        r.criticidade         AS criticidade,
        r.exposicao           AS exposicao,
        r.prejuizo            AS prejuizo,
        r.origem              AS origem,
        r.responsavel         AS responsavel,
        r.status              AS status,
        r.pontuacao           AS pontuacao,
        r.nivel               AS nivel,
        r.acao_preventiva     AS acao_preventiva,
        r.acao_contingencia   AS acao_contingencia,
        r.data_identificacao  AS data_identificacao,
        r.prazo_tratamento    AS prazo_tratamento,
        r.justificativa_aceite AS justificativa_aceite
"""

_ALVOS_PERMITIDOS = {
    "servico": {"label": "ServicoTIC", "campo": "nome", "relacao": "AFETA"},
    "risco":   {"label": "Risco",      "campo": "identificador", "relacao": "RELACIONADO_A"},
    "sistema": {"label": "Sistema",    "campo": "nome", "relacao": "AFETA"},
    "unidade": {"label": "Unidade",    "campo": "nome", "relacao": "RELACIONADO_A"},
}


class RiscoRepository:
    def __init__(self, driver: AsyncDriver):
        self.driver = driver

    def _mapear(self, registro: dict) -> RiscoResponse:
        return RiscoResponse(
            element_id            = registro["element_id"],
            identificador         = registro["identificador"],
            nome                  = registro["nome"],
            descricao             = registro.get("descricao"),
            categoria             = registro["categoria"],
            probabilidade         = registro["probabilidade"],
            impacto               = registro["impacto"],
            criticidade           = registro["criticidade"],
            exposicao             = registro["exposicao"],
            prejuizo              = registro["prejuizo"],
            origem                = registro.get("origem"),
            responsavel           = registro.get("responsavel"),
            status                = registro["status"],
            pontuacao             = registro["pontuacao"],
            nivel                 = registro["nivel"],
            acao_preventiva       = registro.get("acao_preventiva"),
            acao_contingencia     = registro.get("acao_contingencia"),
            data_identificacao    = registro.get("data_identificacao"),
            prazo_tratamento      = registro.get("prazo_tratamento"),
            justificativa_aceite  = registro.get("justificativa_aceite"),
        )

    async def obter_por_identificador(self, identificador: str) -> RiscoResponse | None:
        async with self.driver.session() as session:
            result = await session.run(
                f"MATCH (r:Risco {{identificador: $identificador}}) {_RETURN_RISCO}",
                identificador=identificador,
            )
            registro = await result.single()
        if not registro:
            return None
        return self._mapear(dict(registro))

    async def criar(self, payload: RiscoCreate) -> RiscoResponse:
        props = payload.gerar_dados_para_banco()
        async with self.driver.session() as session:
            result = await session.run(
                f"CREATE (r:Risco) SET r += $props {_RETURN_RISCO}",
                props=props,
            )
            registro = await result.single()
        return self._mapear(dict(registro))

    async def listar(self) -> list[RiscoResponse]:
        async with self.driver.session() as session:
            result = await session.run(
                f"MATCH (r:Risco) {_RETURN_RISCO} ORDER BY r.pontuacao DESC"
            )
            registros = await result.data()
        return [self._mapear(dict(r)) for r in registros]

    async def atualizar(self, identificador: str, payload: RiscoCreate) -> RiscoResponse | None:
        dados = payload.gerar_dados_para_banco()
        async with self.driver.session() as session:
            result = await session.run(
                f"""
                MATCH (r:Risco {{identificador: $identificador}})
                SET r += $dados
                {_RETURN_RISCO}
                """,
                identificador=identificador,
                dados=dados,
            )
            registro = await result.single()
        if not registro:
            return None
        return self._mapear(dict(registro))

    async def deletar(self, identificador: str) -> bool:
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (r:Risco {identificador: $identificador})
                WITH r, count(r) AS total
                DETACH DELETE r
                RETURN total > 0 AS removido
                """,
                identificador=identificador,
            )
            registro = await result.single()
        return bool(registro and registro["removido"])

    async def vincular(self, identificador: str, vinculo: RiscoVinculo) -> bool:
        configuracao = _ALVOS_PERMITIDOS.get(vinculo.tipo_alvo)
        if not configuracao:
            return False

        label  = configuracao["label"]
        campo  = configuracao["campo"]
        relacao = configuracao["relacao"]

        query = f"""
            MATCH (r:Risco {{identificador: $identificador}})
            MATCH (alvo:{label} {{{campo}: $valor_alvo}})
            MERGE (r)-[:{relacao}]->(alvo)
            RETURN true AS vinculado
        """
        async with self.driver.session() as session:
            result = await session.run(
                query,
                identificador=identificador,
                valor_alvo=vinculo.identificador_alvo,
            )
            registro = await result.single()
        return bool(registro and registro["vinculado"])

    async def metricas(self) -> dict:
        async with self.driver.session() as session:
            r_nivel = await session.run(
                "MATCH (r:Risco) RETURN r.nivel AS nivel, count(r) AS total"
            )
            por_nivel = {row["nivel"]: row["total"] for row in await r_nivel.data()}

            r_status = await session.run(
                "MATCH (r:Risco) RETURN r.status AS status, count(r) AS total"
            )
            por_status = {row["status"]: row["total"] for row in await r_status.data()}

            r_cat = await session.run(
                "MATCH (r:Risco) RETURN r.categoria AS categoria, count(r) AS total"
            )
            por_categoria = {row["categoria"]: row["total"] for row in await r_cat.data()}

            r_vencidos = await session.run(
                """
                MATCH (r:Risco)
                WHERE r.prazo_tratamento < date()
                  AND r.status NOT IN ['encerrado', 'mitigado', 'aceito']
                RETURN count(r) AS total
                """
            )
            vencidos = (await r_vencidos.single() or {}).get("total", 0)

        return {
            "por_nivel":     por_nivel,
            "por_status":    por_status,
            "por_categoria": por_categoria,
            "prazo_vencido": vencidos,
        }
