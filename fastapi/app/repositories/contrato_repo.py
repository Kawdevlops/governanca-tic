from neo4j import AsyncDriver
from app.models.contrato import ContratoBase, ContratoCreate, ContratoUpdate, ContratoResponse
from app.models.pessoa import PessoaBase
from app.models.pessoa_contrato import ContratoPessoa, VinculoPessoaContrato
from app.models.contrato_servico import ContratoServico, VinculoContratoServico
from app.models.servico import ServicoBase


class ContratoRepository:
    def __init__(self, driver: AsyncDriver):
        self.driver = driver

    def _query_base(self) -> str:
        return """
            CALL (c) {
                WITH c
                OPTIONAL MATCH (p:Pessoa)-[r]->(c)
                WITH DISTINCT p, r
                WHERE p IS NOT NULL
                RETURN collect(
                    {
                        descricao_vinculo: type(r),
                        pessoa: {
                            element_id: elementId(p),
                            nome: p.nome,
                            email: p.email,
                            telefone_movel: p.telefone_movel,
                            telefone_fixo: p.telefone_fixo,
                            ramal: p.ramal
                        }
                    }
                ) AS vinculos_pessoas
            }

            CALL (c) {
                WITH c
                OPTIONAL MATCH (c)-[f]->(s:ServicoTIC)
                WITH DISTINCT s, f
                WHERE s IS NOT NULL
                RETURN collect(
                    {
                        descricao_vinculo: type(f),
                        servico: {
                            element_id: elementId(s),
                            categoria: s.categoria,
                            nome: s.nome,
                            descricao: s.descricao,
                            publico_alvo: s.publico_alvo,
                            status: s.status,
                            responsavel_atendimento_unidade: s.responsavel_atendimento_unidade,
                            responsavel_atendimento_equipe: s.responsavel_atendimento_equipe,
                            data_ultima_revisao: s.data_ultima_revisao,
                            autor_ultima_revisao: s.autor_ultima_revisao
                        }
                    }
                ) AS vinculos_servicos
            }

            RETURN
                elementId(c) AS element_id,
                c.numero AS numero,
                c.ano AS ano,
                c.fornecedor AS fornecedor,
                c.vigencia_inicio AS vigencia_inicio,
                c.vigencia_fim AS vigencia_fim,
                c.valor_anual_estimado AS valor_anual_estimado,
                c.processo_sei AS processo_sei,
                vinculos_pessoas,
                vinculos_servicos
        """

    async def criar(self, payload: ContratoCreate) -> ContratoResponse:
        props =payload.model_dump(exclude_none=True)
        async with self.driver.session() as session:
            result = await session.run("""
                MERGE (c:Contrato {numero: $props.numero, ano: $props.ano})
                ON CREATE SET c += $props
                RETURN elementId(c) AS element_id,
                    c.numero AS numero,
                    c.ano AS ano,
                    c.fornecedor AS fornecedor,
                    c.vigencia_inicio AS vigencia_inicio,
                    c.vigencia_fim AS vigencia_fim,
                    c.valor_anual_estimado AS valor_anual_estimado,
                    c.processo_sei AS processo_sei
            """, props=props)
            registro = await result.single()
        return self._mapear(dict(registro))

    async def obter_por_numero_ano(self, numero:int, ano:int) -> ContratoResponse | None:
        async with self.driver.session() as session:
            query = """
                MATCH (c:Contrato {numero: $numero, ano: $ano})
            """ + self._query_base()

            result = await session.run(query, numero=numero, ano=ano)
            registro = await result.single()
            
            if not registro:
                return None
            
            return self._mapear(dict(registro))

    async def listar(self) -> list[ContratoResponse]:
        async with self.driver.session() as session:
            query = """
                MATCH (c:Contrato)
                """ + self._query_base() + """
                ORDER BY c.ano, c.numero
            """
            result = await session.run(query)
            registros = await result.data()
        return [self._mapear(dict(r)) for r in registros]

    async def atualizar(self, numero: int, ano: int, payload: ContratoUpdate) -> ContratoResponse | None:
        campos = payload.model_dump(exclude_none=True)

        if not campos:
            return await self.obter_por_numero_ano(numero, ano)
        
        set_clauses = []
        params = {"numero_ref": numero, "ano_ref": ano}

        if "numero" in campos:
            set_clauses.append("c.numero = $numero")
            params["numero"] = campos["numero"]

        if "ano" in campos:
            set_clauses.append("c.ano = $ano")
            params["ano"] = campos["ano"]

        if "fornecedor" in campos:
            set_clauses.append("c.fornecedor = $fornecedor")
            params["fornecedor"] = campos["fornecedor"]

        if "vigencia_inicio" in campos:
            set_clauses.append("c.vigencia_inicio = $vigencia_inicio")
            params["vigencia_inicio"] = campos["vigencia_inicio"]

        if "vigencia_fim" in campos:
            set_clauses.append("c.vigencia_fim = $vigencia_fim")
            params["vigencia_fim"] = campos["vigencia_fim"]

        if "valor_anual_estimado" in campos:
            set_clauses.append("c.valor_anual_estimado = $valor_anual_estimado")
            params["valor_anual_estimado"] = campos["valor_anual_estimado"]

        if "processo_sei" in campos:
            set_clauses.append("c.processo_sei = $processo_sei")
            params["processo_sei"] = campos["processo_sei"]
        
        query = f"""
            MATCH (c:Contrato {{numero: $numero_ref, ano: $ano_ref}})
            SET {", ".join(set_clauses)}
            RETURN 
                elementId(c) AS element_id,
                c.numero AS numero,
                c.ano AS ano,
                c.fornecedor AS fornecedor,
                c.vigencia_inicio AS vigencia_inicio,
                c.vigencia_fim AS vigencia_fim,
                c.valor_anual_estimado AS valor_anual_estimado,
                c.processo_sei AS processo_sei
        """
        async with self.driver.session() as session:
            result = await session.run(query, **params)
            registro = await result.single()

        if not registro:
            return None

        return self._mapear(registro)

    async def deletar(self, numero: int, ano: int) -> bool:
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (c:Contrato {numero: $numero, ano: $ano})
                WITH c, count(c) AS total
                DETACH DELETE c
                RETURN total > 0 AS removido
            """, numero=numero, ano=ano)
            registro = await result.single()
        
        return bool(registro and registro["removido"])

    async def vincular_servico(self, contrato: ContratoBase, servico: ServicoBase, vinculo:VinculoContratoServico) -> ContratoServico | None:
        async with self.driver.session() as session:

            if not isinstance(servico, ServicoBase):
                return None
            
            if vinculo == VinculoContratoServico.FORNECE:
                query = """
                    MATCH (c:Contrato {numero: $p_numero, ano: $p_ano})
                    MATCH (s:ServicoTIC {nome: $p_nome})
                    MERGE (c)-[:FORNECE]->(s)
                    MERGE (s)-[:FORNECIDO]->(c)
                    RETURN true AS vinculado
                """
            else:
                return None
            
            result = await session.run(query, p_numero=contrato.numero, p_ano=contrato.ano, p_nome=servico.nome)
            registro = await result.single()
            if bool(registro and registro["vinculado"]):
                contrato_servico = ContratoServico(descricao_vinculo=vinculo, no=servico)
                contrato.vinculos.append(contrato_servico)
                return contrato_servico
            
        return None

    def _mapear(self, r: dict) -> ContratoResponse:
        #print(r)
        vinculos = []

        for v in r.get("vinculos_pessoas", []):
            desc_vinculo = v["descricao_vinculo"]
            pessoa_vinculada = v.get("pessoa")
            if pessoa_vinculada and desc_vinculo:
                pessoa = PessoaBase(
                    nome = pessoa_vinculada.get("nome"),
                    email = pessoa_vinculada.get("email"),
                    telefone_movel = pessoa_vinculada.get("telefone_movel"),
                    telefone_fixo = pessoa_vinculada.get("telefone_fixo"),
                    ramal = pessoa_vinculada.get("ramal")
                )
                vinculos.append(ContratoPessoa(descricao_vinculo=VinculoPessoaContrato(desc_vinculo), no=pessoa))

        for v in r.get("vinculos_servicos", []):
            desc_vinculo = v["descricao_vinculo"]
            servico_vinculado = v.get("servico")
            if servico_vinculado and desc_vinculo:
                servico = ServicoBase(
                    categoria = servico_vinculado.get("categoria"),
                    nome = servico_vinculado.get("nome"),
                    descricao = servico_vinculado.get("descricao"),
                    publico_alvo = servico_vinculado.get("publico_alvo"),
                    responsavel_atendimento_unidade = servico_vinculado.get("responsavel_atendimento_unidade"),
                    responsavel_atendimento_equipe = servico_vinculado.get("responsavel_atendimento_equipe"),
                    data_ultima_revisao = servico_vinculado.get("data_ultima_revisao"),
                    autor_ultima_revisao = servico_vinculado.get("autor_ultima_revisao"),
                    status = servico_vinculado.get("status")
                )
                vinculos.append(ContratoServico(descricao_vinculo=VinculoContratoServico(desc_vinculo), no=servico))

        vigencia_inicio = r.get("vigencia_inicio")
        vigencia_fim = r.get("vigencia_fim")

        if vigencia_inicio is not None:
            vigencia_inicio = vigencia_inicio.to_native()

        if vigencia_fim is not None:
            vigencia_fim = vigencia_fim.to_native()

        return ContratoResponse(
            element_id=r["element_id"],
            numero=r["numero"],
            ano = r["ano"],
            fornecedor = r.get("fornecedor", None),
            vigencia_inicio = vigencia_inicio,
            vigencia_fim = vigencia_fim,
            valor_anual_estimado = r.get("valor_anual_estimado", None),
            processo_sei = r.get("processo_sei", None),
            vinculos=vinculos
        )