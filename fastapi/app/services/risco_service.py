from fastapi import HTTPException
from app.models.risco import RiscoCreate, RiscoUpdate, RiscoResponse, RiscoVinculo, StatusRisco
from app.repositories.risco_repo import RiscoRepository


class RiscoService:
    def __init__(self, repo: RiscoRepository):
        self.repo = repo

    async def criar(self, payload: RiscoCreate) -> RiscoResponse:
        existente = await self.repo.obter_por_identificador(payload.identificador)
        if existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um risco com este identificador.",
            )
        return await self.repo.criar(payload)

    async def listar(self) -> list[RiscoResponse]:
        return await self.repo.listar()

    async def obter_por_identificador(self, identificador: str) -> RiscoResponse:
        risco = await self.repo.obter_por_identificador(identificador)
        if not risco:
            raise HTTPException(
                status_code=404,
                detail="Risco não encontrado.",
            )
        return risco

    async def atualizar(self, identificador: str, dados_novos: RiscoUpdate) -> RiscoResponse:
        risco_atual = await self.repo.obter_por_identificador(identificador)
        if not risco_atual:
            raise HTTPException(status_code=404, detail="Risco não encontrado.")

        # validação de negócio: se o usuário está mudando o status para ACEITO, ele precisa obrigatoriamente informar a justificativa.
        # Sem isso não há rastreabilidade da decisão de aceitar o risco, o que viola o princípio de auditoria da IN 1/2019.
        novo_status = dados_novos.status or risco_atual.status
        if novo_status == StatusRisco.ACEITO:
            justificativa = dados_novos.justificativa_aceite or risco_atual.justificativa_aceite
            if not justificativa:
                raise HTTPException(
                    status_code=422,
                    detail="Para aceitar um risco é obrigatório informar 'justificativa_aceite'.",
                )

        dados_antigos = risco_atual.model_dump(
            exclude={"element_id", "pontuacao", "nivel"},
            mode="json",
        )
        dados_atualizados = dados_novos.model_dump(exclude_none=True, mode="json")
        dados_antigos.update(dados_atualizados)

        risco_recalculado = RiscoCreate(**dados_antigos)
        return await self.repo.atualizar(identificador, risco_recalculado)

    async def deletar(self, identificador: str) -> dict:
        removido = await self.repo.deletar(identificador)
        if not removido:
            raise HTTPException(status_code=404, detail="Risco não encontrado.")
        return {"detail": "Risco removido com sucesso."}

    async def vincular(self, identificador: str, vinculo: RiscoVinculo) -> dict:
        risco = await self.repo.obter_por_identificador(identificador)
        if not risco:
            raise HTTPException(status_code=404, detail="Risco não encontrado.")

        vinculado = await self.repo.vincular(identificador, vinculo)
        if not vinculado:
            raise HTTPException(
                status_code=404,
                detail="Item afetado não encontrado ou tipo de alvo inválido.",
            )
        return {"detail": "Risco vinculado com sucesso."}

    # delega ao repo e retorna o dict de métricas.
    async def metricas(self) -> dict:
        return await self.repo.metricas()