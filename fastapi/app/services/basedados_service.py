from app.repositories.basedados_repo import BaseDadosRepository
from app.models.basedados import BaseDadosCreate, BaseDadosResponse, BaseDadosUpdate
from fastapi import HTTPException


class BaseDadosService:
    def __init__(self, repo: BaseDadosRepository):
        self.repo = repo

    async def listar_catalogo(self) -> list[BaseDadosResponse]:
        return await self.repo.listar()

    async def obter_por_titulo(self, titulo: str) -> BaseDadosResponse:
        base = await self.repo.obter_por_titulo(titulo)
        if not base:
            raise HTTPException(status_code=404, detail="Base de dados não encontrada.")
        return base

    async def criar(self, payload: BaseDadosCreate) -> BaseDadosResponse:
        existente = await self.repo.obter_por_titulo(payload.titulo)
        if existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe uma base de dados cadastrada com este título."
            )
        return await self.repo.criar(payload)

    async def atualizar(self, titulo: str, payload: BaseDadosUpdate) -> BaseDadosResponse:
        base = await self.repo.atualizar(titulo, payload)
        if not base:
            raise HTTPException(status_code=404, detail="Base de dados não encontrada.")
        return base

    async def deletar(self, titulo: str) -> dict:
        removido = await self.repo.deletar(titulo)
        if not removido:
            raise HTTPException(status_code=404, detail="Base de dados não encontrada.")
        return {"detail": "Base de dados removida com sucesso."}