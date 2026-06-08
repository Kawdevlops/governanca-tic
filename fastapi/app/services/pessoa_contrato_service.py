from fastapi import HTTPException
from app.models.pessoa_contrato import PessoaContrato, VinculoPessoaContrato
from app.repositories.pessoa_repo import PessoaRepository
from app.repositories.contrato_repo import ContratoRepository

class PessoaContratoService():

    def __init__(self, repo_pessoa: PessoaRepository, repo_contrato: ContratoRepository):
        self.repo_pessoa = repo_pessoa
        self.repo_contrato = repo_contrato

    async def vincular_contrato(self, email: str, vinculo: VinculoPessoaContrato, numero:int , ano:int) -> PessoaContrato:
        pessoa = await self.repo_pessoa.obter_por_email(email)
        if not pessoa:
            raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
        contrato = await self.repo_contrato.obter_por_numero_ano(numero, ano)
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado.")
        
        vinculado = await self.repo_pessoa.vincular_contrato(pessoa, contrato, vinculo)
        if not vinculado:
            raise HTTPException(status_code=500, detail="Não foi possível vincular a pessoa ao contrato.")
        return vinculado
