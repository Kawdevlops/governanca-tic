# Projeto Hydra - Isto faz aquilo o qual se pretende fazer
# Copyright (C) 2026 Secretaria Municipal das Subprefeituras
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

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
