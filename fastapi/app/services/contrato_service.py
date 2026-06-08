from fastapi import HTTPException
from app.repositories.contrato_repo import ContratoRepository
from app.models.contrato import ContratoCreate, ContratoUpdate, ContratoResponse

class ContratoService:
    def __init__(self, repo: ContratoRepository):
        self.repo = repo
    
    async def listar(self) -> list[ContratoResponse]:
        return await self.repo.listar()

    async def obter_por_numero_ano(self, numero: int, ano: int) -> ContratoResponse:
        contrato = await self.repo.obter_por_numero_ano(numero, ano)
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado.")
        return contrato

    async def criar(self, payload: ContratoCreate) -> ContratoResponse:
        existente = await self.repo.obter_por_numero_ano(int(payload.numero), int(payload.ano))
        if existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um contrato com este número e ano."
            )
        return await self.repo.criar(payload)
    
    async def atualizar(self, numero: int, ano: int, payload: ContratoUpdate) -> ContratoResponse:
        contrato = await self.repo.atualizar(numero, ano, payload)
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado.")
        return contrato
        
    async def deletar(self, numero: int, ano: int) -> dict:
        removido = await self.repo.deletar(numero, ano)
        if not removido:
            raise HTTPException(status_code=404, detail="Contrato não encontrado.")
        return {"detail": "Contrato removido com sucesso."}