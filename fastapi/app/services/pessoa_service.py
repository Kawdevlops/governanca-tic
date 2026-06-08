from fastapi import HTTPException
from app.repositories.pessoa_repo import PessoaRepository
from app.models.pessoa import PessoaCreate, PessoaUpdate, PessoaResponse

class PessoaService:
    def __init__(self, repo: PessoaRepository):
        self.repo = repo

    async def listar(self) -> list[PessoaResponse]:
        return await self.repo.listar()

    async def obter_por_email(self, email: str) -> PessoaResponse:
        pessoa = await self.repo.obter_por_email(email)
        if not pessoa:
            raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
        return pessoa

    async def criar(self, payload: PessoaCreate) -> PessoaResponse:
        existente = await self.repo.obter_por_email(str(payload.email))
        if existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe uma pessoa com este e-mail."
            )
        return await self.repo.criar(payload)

    async def atualizar(self, email: str, payload: PessoaUpdate) -> PessoaResponse:
        pessoa = await self.repo.atualizar(email, payload)
        if not pessoa:
            raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
        return pessoa

    async def deletar(self, email: str) -> dict:
        removido = await self.repo.deletar(email)
        if not removido:
            raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
        return {"detail": "Pessoa removida com sucesso."}
    


