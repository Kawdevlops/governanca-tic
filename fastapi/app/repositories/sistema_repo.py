from neo4j import AsyncDriver
from app.models.sistema import SistemaBase, SistemaCreate, SistemaResponse

class SistemaRepository:

    def __init__(self, driver: AsyncDriver):
        self.driver = driver

    async def criar(self, payload: SistemaCreate) -> SistemaResponse:
        props = payload.model_dump(exclude_none=True)
        async with self.driver.session() as session:
            result = await session.run("""
                CREATE (s:Sistema) 
                SET s += $props
                RETURN 
                    elementId(s) AS element_id,
                    s.nome AS nome,
                    s.sigla AS sigla
            """, props=props)
            registro = await result.single()

        return self._mapear(dict(registro))

    async def obter_por_sigla(self, sigla: str) -> SistemaResponse | None:
        async with self.driver.session() as session:
            result = await session.run(f"""
                MATCH (s:Sistema {{sigla: $p_sigla}})
                RETURN 
                    elementId(s) AS element_id,
                    s.nome AS nome,
                    s.sigla AS sigla
            """, p_sigla=sigla)
            registro = await result.single()

            if not registro:
                return None

            return self._mapear(dict(registro))


    def _mapear(self, r: dict) -> SistemaResponse:
        return SistemaResponse(
            element_id = r.get("element_id"),
            nome = r.get("nome"),
            sigla = r.get("sigla")
        )
