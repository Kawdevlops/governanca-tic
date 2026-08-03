from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import Neo4jConnection
from app.routers import pessoa, contrato, servico, risco

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