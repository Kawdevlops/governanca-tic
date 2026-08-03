from fastapi import HTTPException
from app.repositories.sistema_repo import SistemaRepository
from app.models.sistema import SistemaCreate, SistemaResponse

class SistemaService:
    
    def __init__(self, repo: SistemaRepository):
        self.repo = repo

    async def criar(self, payload: SistemaCreate) -> SistemaResponse:
        sistema_existente = await self.repo.obter_por_sigla(str(payload.sigla))
        if sistema_existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um sistema com esta sigla."
            )
        return await self.repo.criar(payload)