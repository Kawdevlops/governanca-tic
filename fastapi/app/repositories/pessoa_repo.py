from neo4j import AsyncDriver
from app.models.pessoa import PessoaBase, PessoaCreate, PessoaUpdate, PessoaResponse
from app.models.contrato import ContratoBase
from app.models.pessoa_contrato import PessoaContrato, VinculoPessoaContrato

from enum import Enum

class PessoaRepository:
    def __init__(self, driver: AsyncDriver):
        self.driver = driver

    def _query_base(self) -> str:
        return """
            CALL (p) {
                WITH p
                OPTIONAL MATCH (p)-[r]->(c:Contrato)
                WITH DISTINCT c, r
                WHERE c IS NOT NULL
                RETURN collect(
                    {
                        descricao_vinculo: type(r),
                        contrato : {
                            element_id: elementId(c),
                            numero: c.numero,
                            ano: c.ano,
                            fornecedor: c.fornecedor,
                            vigencia_inicio: c.vigencia_inicio,
                            vigencia_fim: c.vigencia_fim,
                            valor_anual_estimado: c.valor_anual_estimado,
                            processo_sei: c.processo_sei
                        }
                    }
                ) AS vinculos_contratos
            }
            RETURN
                elementId(p) AS element_id,
                p.nome AS nome,
                p.email AS email,
                p.telefone_movel AS telefone_movel,
                p.telefone_fixo AS telefone_fixo,
                p.ramal AS ramal,
                vinculos_contratos
        """

    async def criar(self, payload: PessoaCreate) -> PessoaResponse:
        props = payload.model_dump(exclude_none=True)
        props["email"] = str(payload.email)
        async with self.driver.session() as session:
            result = await session.run("""
                CREATE (p:Pessoa)
                SET p += $props
                RETURN
                    elementId(p) AS element_id,
                    p.nome AS nome,
                    p.email AS email,
                    p.telefone_movel AS telefone_movel,
                    p.telefone_fixo AS telefone_fixo,
                    p.ramal AS ramal
            """, props=props)
            registro = await result.single()

        return self._mapear(dict(registro))

    async def obter_por_email(self, email: str) -> PessoaResponse | None:
        async with self.driver.session() as session:
            result = await session.run(f"""
                MATCH (p:Pessoa {{email: $email}})
                {self._query_base()}
            """, email=email)
            registro = await result.single()

        if not registro:
            return None

        return self._mapear(dict(registro))

    async def listar(self) -> list[PessoaResponse]:
        async with self.driver.session() as session:
            result = await session.run(f"""
                MATCH (p:Pessoa)
                {self._query_base()}
                ORDER BY p.nome
            """)
            registros = await result.data()

        return [self._mapear(r) for r in registros]

    async def atualizar(self, email: str, payload: PessoaUpdate) -> PessoaResponse | None:
        campos = payload.model_dump(exclude_none=True)

        if not campos:
            return await self.obter_por_email(email)

        set_clauses = []
        params = {"email_ref": email}

        if "nome" in campos:
            set_clauses.append("p.nome = $nome")
            params["nome"] = campos["nome"]

        if "email" in campos:
            set_clauses.append("p.email = $novo_email")
            params["novo_email"] = str(campos["email"])

        if "telefone_movel" in campos:
            set_clauses.append("p.telefone_movel = $telefone_movel")
            params["telefone_movel"] = campos["telefone_movel"]

        if "telefone_fixo" in campos:
            set_clauses.append("p.telefone_fixo = $telefone_fixo")
            params["telefone_fixo"] = campos["telefone_fixo"]

        if "ramal" in campos:
            set_clauses.append("p.ramal = $ramal")
            params["ramal"] = campos["ramal"]
            
        query = f"""
            MATCH (p:Pessoa {{email: $email_ref}})
            SET {", ".join(set_clauses)}
            RETURN
                elementId(p) AS element_id,
                p.nome AS nome,
                p.email AS email,
                p.telefone_movel AS telefone_movel,
                p.telefone_fixo AS telefone_fixo,
                p.ramal AS ramal
        """

        async with self.driver.session() as session:
            result = await session.run(query, **params)
            registro = await result.single()

        if not registro:
            return None

        return self._mapear(registro)

    async def deletar(self, email: str) -> bool:
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (p:Pessoa {email: $email})
                WITH p, count(p) AS total
                DETACH DELETE p
                RETURN total > 0 AS removido
            """, email=email)
            registro = await result.single()

        return bool(registro and registro["removido"])

    async def vincular_contrato(self, pessoa: PessoaBase, contrato: ContratoBase, vinculo: VinculoPessoaContrato) -> PessoaContrato | None:
        async with self.driver.session() as session:

            if not isinstance(contrato, ContratoBase):
                return None
            
            if vinculo == VinculoPessoaContrato.FISCALIZA:
                query = """
                    MATCH (p:Pessoa {email: $p_email})
                    MATCH (c:Contrato {numero: $p_numero, ano: $p_ano})
                    MERGE (p)-[:FISCALIZA]->(c)
                    RETURN true AS vinculado
                """
            elif vinculo == VinculoPessoaContrato.SUPLENTE_FISCAL:
                query = """
                    MATCH (p:Pessoa {email: $p_email})
                    MATCH (c:Contrato {numero: $p_numero, ano: $p_ano})
                    MERGE (p)-[:SUPLENTE_FISCAL]->(c)
                    RETURN true AS vinculado
                """
            elif vinculo == VinculoPessoaContrato.GESTOR_CONTRATO:
                query = """
                    MATCH (p:Pessoa {email: $p_email})
                    MATCH (c:Contrato {numero: $p_numero, ano: $p_ano})
                    MERGE (p)-[:GESTOR_CONTRATO]->(c)
                    RETURN true AS vinculado
                """

            result = await session.run(query, p_email=pessoa.email, p_numero=contrato.numero, p_ano=contrato.ano)
            registro = await result.single()
            if bool(registro and registro["vinculado"]):
                pessoa_contrato = PessoaContrato(descricao_vinculo=vinculo, no=contrato)
                pessoa.vinculos.append(pessoa_contrato)
                return pessoa_contrato
            
        return None
     
    def _mapear(self, r: dict) -> PessoaResponse:

        vinculos = []

        for v in r.get("vinculos_contratos", []):
            desc_vinculo = v["descricao_vinculo"]
            contrato_vinculado = v.get("contrato")
            if contrato_vinculado and desc_vinculo:

                vigencia_inicio = r.get("vigencia_inicio")
                vigencia_fim = r.get("vigencia_fim")

                if vigencia_inicio is not None:
                    vigencia_inicio = vigencia_inicio.to_native()

                if vigencia_fim is not None:
                    vigencia_fim = vigencia_fim.to_native()

                contrato = ContratoBase(
                    numero = contrato_vinculado.get("numero"),
                    ano = contrato_vinculado.get("ano"),
                    fornecedor = contrato_vinculado.get("fornecedor"),
                    vigencia_inicio = vigencia_inicio,
                    vigencia_fim = vigencia_fim,
                    valor_anual_estimado = contrato_vinculado.get("valor_anual_estimado"),
                    processo_sei = contrato_vinculado.get("processo_sei")
                )

                vinculos.append(PessoaContrato(descricao_vinculo=VinculoPessoaContrato(desc_vinculo),no=contrato))


        return PessoaResponse(
            element_id=r["element_id"],
            nome=r["nome"],
            email=r["email"],
            telefone_movel=r.get("telefone_movel",""),
            telefone_fixo=r.get("telefone_fixo",""),
            ramal=r.get("ramal",""),
            vinculos=vinculos
        )