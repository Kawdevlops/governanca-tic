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
