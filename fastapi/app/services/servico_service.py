from app.repositories.servico_repo import ServicoRepository
from app.models.servico import ServicoCreate, ServicoResponse, ServicoUpdate
from fastapi import HTTPException

class ServicoService:
    def __init__(self, repo: ServicoRepository):
        self.repo = repo

    async def listar_catalogo(self) -> list[ServicoResponse]:
        return await self.repo.listar()
    
    async def obter_por_nome_servico(self, nome: str) -> ServicoResponse:
        servico = await self.repo.obter_por_nome_servico(nome)
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado.")
        return servico

    async def criar(self, payload: ServicoCreate) -> ServicoResponse:
        existente = await self.repo.obter_por_nome_servico(str(payload.nome))
        if existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um serviço com este nome."
            )
        return await self.repo.criar(payload)

    async def atualizar(self, nome: str, payload: ServicoUpdate) -> ServicoUpdate:
        servico = await self.repo.atualizar(nome, payload)
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado.")
        return servico
    
    async def deletar(self, nome: str) -> dict:
        removido = await self.repo.deletar(nome)
        if not removido:
            raise HTTPException(status_code=404, detail="Serviço não encontrado.")
        return {"detail": "Serviço removido com sucesso."}
