from neo4j import AsyncGraphDatabase, AsyncDriver
from app.core.config import settings

class Neo4jConnection:
    _driver: AsyncDriver | None = None

    @classmethod
    async def connect(cls):
        cls._driver = AsyncGraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))

    @classmethod
    async def close(cls):
        if cls._driver:
            await cls._driver.close()

    @classmethod
    def get_driver(cls) -> AsyncDriver:
        if not cls._driver:
            raise RuntimeError("Não conectado ao banco de dados Neo4j")
        return cls._driver
