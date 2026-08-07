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

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import Neo4jConnection
from app.routers import pessoa, contrato, servico, risco, basedados

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Neo4jConnection.connect()
    yield
    await Neo4jConnection.close()

app = FastAPI(
    title="API de Governança TIC - SMSUB",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def get_health_check():
    return {"status": "ok"}

app.include_router(servico.router, prefix="/v1/governanca")
app.include_router(pessoa.router, prefix="/v1/governanca")
app.include_router(contrato.router, prefix="/v1/governanca")
app.include_router(risco.router, prefix="/v1/governanca")
app.include_router(basedados.router, prefix="/v1/governanca")