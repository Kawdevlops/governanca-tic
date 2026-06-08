from fastapi import HTTPException
from app.models.contrato_servico import ContratoServico, VinculoContratoServico
from app.repositories.contrato_repo import ContratoRepository
from app.repositories.servico_repo import ServicoRepository

class ContratoServicoService():

    def __init__(self, repo_contrato: ContratoRepository, repo_servico: ServicoRepository):
        self.repo_servico = repo_servico
        self.repo_contrato = repo_contrato

    async def vincular_servico(self, numero:int , ano:int, vinculo: VinculoContratoServico, nome: str) -> ContratoServico:
        contrato = await self.repo_contrato.obter_por_numero_ano(numero, ano)
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado.")
        servico = await self.repo_servico.obter_por_nome_servico(nome)        
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado.")
        
        vinculado = await self.repo_contrato.vincular_servico(contrato, servico, vinculo)
        if not vinculado:
            raise HTTPException(status_code=500, detail="Não foi possível vincular o contrato ao serviço.")
        return vinculado

