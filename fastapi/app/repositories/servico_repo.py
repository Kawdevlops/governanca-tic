# Projeto Hydra - Isto faz aquilo o qual se pretende fazer
# Copyright (C) 2026 Secretaria Municipal das Subprefeituras
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from neo4j import AsyncDriver
from datetime import datetime, timezone
from app.models.servico import ServicoResponse, ServicoCreate, ServicoUpdate
from app.models.contrato import ContratoBase
from app.models.contrato_servico import ServicoContrato, VinculoContratoServico

class ServicoRepository:
    def __init__(self, driver: AsyncDriver):
        self.driver = driver

    def _query_base_return(self) -> str:
        return """
            CALL (s) {
                WITH s
                OPTIONAL MATCH (s)-[f]->(c:Contrato)
                WITH DISTINCT c, f
                WHERE c IS NOT NULL
                RETURN collect(
                    {
                        descricao_vinculo: type(f),
                        contrato: {
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
                elementId(s) AS element_id,
                s.categoria AS categoria,
                s.nome AS nome,
                s.descricao AS descricao,
                s.publico_alvo AS publico_alvo,
                s.status AS status,
                s.solicitacao_pre_requisitos AS solicitacao_pre_requisitos,
                s.solicitacao_descricao_procedimento AS solicitacao_descricao_procedimento,
                s.solicitacao_canal AS solicitacao_canal,
                s.prazo_estimado AS prazo_estimado,
                s.responsavel_atendimento_unidade AS responsavel_atendimento_unidade,
                s.responsavel_atendimento_equipe AS responsavel_atendimento_equipe,
                s.sla_descricao AS sla_descricao,
                s.sla_tempo_resposta_horas AS sla_tempo_resposta_horas,
                s.sla_tempo_solucao_horas AS sla_tempo_solucao_horas,
                s.sla_horario_atendimento AS sla_horario_atendimento,
                s.sla_observacoes AS sla_observacoes,
                s.contrato_resumo AS contrato_resumo,
                s.prioridade AS prioridade,
                s.periodicidade_revisao AS periodicidade_revisao,
                s.data_ultima_revisao AS data_ultima_revisao,
                s.autor_ultima_revisao AS autor_ultima_revisao,
                s.data_proxima_revisao AS data_proxima_revisao,
                vinculos_contratos
        """

    def _query_base(self) -> str:
        return self._query_base_return() + """
            , s.criado_em AS criado_em
            , s.atualizado_em AS atualizado_em
        """

    async def listar(self) -> list[ServicoResponse]:
        async with self.driver.session() as session:
            query = """
                MATCH (s:ServicoTIC)
                """ + self._query_base() + """
                ORDER BY s.nome
            """
            print(query)
            result = await session.run(query)
            registros = await result.data()
        return [self._mapear(r) for r in registros]
    
    async def criar(self, payload: ServicoCreate) -> ServicoResponse:
        props = payload.model_dump(exclude_none=True)
        props["criado_em"] = datetime.now(timezone.utc)

        async with self.driver.session() as session:
            query = """
                CREATE (s:ServicoTIC)
                SET s += $props
            """ + self._query_base_return() + ", s.criado_em AS criado_em"
            result = await session.run(query, props=props)
            registro = await result.single()
        return self._mapear(dict(registro))

    async def obter_por_nome_servico(self, nome: str) -> ServicoResponse | None:
        async with self.driver.session() as session:
            query = """
                MATCH (s:ServicoTIC {nome: $p_nome})
            """ + self._query_base()

            result = await session.run(query, p_nome=nome)
            registro = await result.single()

            if not registro:
                return None
            
            return self._mapear(dict(registro))

    async def atualizar(self, nome: str, payload: ServicoUpdate) -> ServicoResponse | None:
        campos = payload.model_dump(exclude_none=True)

        if not campos:
            return await self.obter_por_nome_servico(nome)
        
        set_clauses = []
        params = {"nome_ref": nome}

        if "categoria" in campos:
            set_clauses.append("s.categoria = $categoria")
            params["categoria"] = campos["categoria"]

        if "nome" in campos:
            set_clauses.append("s.nome = $nome")
            params["nome"] = campos["nome"]

        if "descricao" in campos:
            set_clauses.append("s.descricao = $descricao")
            params["descricao"] = campos["descricao"]

        if "publico_alvo" in campos:
            set_clauses.append("s.publico_alvo = $publico_alvo")
            params["publico_alvo"] = campos["publico_alvo"]

        if "status" in campos:
            set_clauses.append("s.status = $status")
            params["status"] = campos["status"]

        if "solicitacao_canal" in campos:
            set_clauses.append("s.solicitacao_canal = $solicitacao_canal")
            params["solicitacao_canal"] = campos["solicitacao_canal"]

        if "solicitacao_pre_requisitos" in campos:
            set_clauses.append("s.solicitacao_pre_requisitos = $solicitacao_pre_requisitos")
            params["solicitacao_pre_requisitos"] = campos["solicitacao_pre_requisitos"]

        if "solicitacao_descricao_procedimento" in campos:
            set_clauses.append("s.solicitacao_descricao_procedimento = $solicitacao_descricao_procedimento")
            params["solicitacao_descricao_procedimento"] = campos["solicitacao_descricao_procedimento"]

        if "prazo_estimado" in campos:
            set_clauses.append("s.prazo_estimado = $prazo_estimado")
            params["prazo_estimado"] = campos["prazo_estimado"]

        if "responsavel_atendimento_unidade" in campos:
            set_clauses.append("s.responsavel_atendimento_unidade = $responsavel_atendimento_unidade")
            params["responsavel_atendimento_unidade"] = campos["responsavel_atendimento_unidade"]

        if "responsavel_atendimento_equipe" in campos:
            set_clauses.append("s.responsavel_atendimento_equipe = $responsavel_atendimento_equipe")
            params["responsavel_atendimento_equipe"] = campos["responsavel_atendimento_equipe"]

        if "sla_descricao" in campos:
            set_clauses.append("s.sla_descricao = $sla_descricao")
            params["sla_descricao"] = campos["sla_descricao"]

        if "sla_tempo_resposta_horas" in campos:
            set_clauses.append("s.sla_tempo_resposta_horas = $sla_tempo_resposta_horas")
            params["sla_tempo_resposta_horas"] = campos["sla_tempo_resposta_horas"]

        if "sla_tempo_solucao_horas" in campos:
            set_clauses.append("s.sla_tempo_solucao_horas = $sla_tempo_solucao_horas")
            params["sla_tempo_solucao_horas"] = campos["sla_tempo_solucao_horas"]

        if "sla_horario_atendimento" in campos:
            set_clauses.append("s.sla_horario_atendimento = $sla_horario_atendimento")
            params["sla_horario_atendimento"] = campos["sla_horario_atendimento"]

        if "sla_observacoes" in campos:
            set_clauses.append("s.sla_observacoes = $sla_observacoes")
            params["sla_observacoes"] = campos["sla_observacoes"]

        if "contrato_resumo" in campos:
            set_clauses.append("s.contrato_resumo = $contrato_resumo")
            params["contrato_resumo"] = campos["contrato_resumo"]

        if "prioridade" in campos:
            set_clauses.append("s.prioridade = $prioridade")
            params["prioridade"] = campos["prioridade"]

        if "periodicidade_revisao" in campos:
            set_clauses.append("s.periodicidade_revisao = $periodicidade_revisao")
            params["periodicidade_revisao"] = campos["periodicidade_revisao"]

        if "data_ultima_revisao" in campos:
            set_clauses.append("s.data_ultima_revisao = $data_ultima_revisao")
            params["data_ultima_revisao"] = campos["data_ultima_revisao"]

        if "autor_ultima_revisao" in campos:
            set_clauses.append("s.autor_ultima_revisao = $autor_ultima_revisao")
            params["autor_ultima_revisao"] = campos["autor_ultima_revisao"]

        if "data_proxima_revisao" in campos:
            set_clauses.append("s.data_proxima_revisao = $data_proxima_revisao")
            params["data_proxima_revisao"] = campos["data_proxima_revisao"]

        query = f"""
            MATCH (s:ServicoTIC {{nome: $nome_ref}})
            SET s.atualizado_em = datetime(), {", ".join(set_clauses)}
        """ + self._query_base_return() + ", s.criado_em AS criado_em, s.atualizado_em AS atualizado_em"

        async with self.driver.session() as session:
            result = await session.run(query, **params)
            registro = await result.single()
        
        if not registro:
            return None
        
        return self._mapear(registro)

    async def deletar(self, nome: str) -> bool:
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (s:ServicoTIC {nome: $p_nome})
                WITH s, count(s) AS total
                DETACH DELETE s
                RETURN total > 0 AS removido
            """, p_nome=nome)
            registro = await result.single()

        return bool(registro and registro["removido"])

    def _mapear(self, r: dict) -> ServicoResponse:

        vinculos = []
        for v in r.get("vinculos_contratos", []):
            desc_vinculo = v.get("descricao_vinculo")
            contrato_vinculado = v.get("contrato")
            if contrato_vinculado and desc_vinculo:
                contrato = ContratoBase(
                    numero = contrato_vinculado.get("numero"),
                    ano = contrato_vinculado.get("ano"),
                    fornecedor = contrato_vinculado.get("fornecedor"),
                    vigencia_inicio = contrato_vinculado.get("vigencia_inicio"),
                    vigencia_fim = contrato_vinculado.get("vigencia_fim"),
                    valor_anual_estimado = contrato_vinculado.get("valor_anual_estimado"),
                    processo_sei = contrato_vinculado.get("processo_sei")
                )
                vinculos.append(ServicoContrato(descricao_vinculo=VinculoContratoServico(desc_vinculo),
                                                no=contrato))

        data_ultima_revisao = r.get("data_ultima_revisao")
        data_proxima_revisao = r.get("data_proxima_revisao")
        criado_em = r.get("criado_em")
        atualizado_em = r.get("atualizado_em")

        if data_ultima_revisao is not None:
            data_ultima_revisao = data_ultima_revisao.to_native()

        if data_proxima_revisao is not None:
            data_proxima_revisao = data_proxima_revisao.to_native()

        if criado_em is not None:
            criado_em = criado_em.to_native()

        if atualizado_em is not None:
            atualizado_em = atualizado_em.to_native()

        return ServicoResponse(
            element_id = r["element_id"],
            categoria = r.get("categoria", ""),
            nome = r.get("nome", ""),
            descricao = r.get("descricao", ""),
            publico_alvo = r.get("publico_alvo", ""),
            status = r.get("status", ""),
            solicitacao_pre_requisitos = r["solicitacao_pre_requisitos"],
            solicitacao_descricao_procedimento = r["solicitacao_descricao_procedimento"],
            solicitacao_canal = r["solicitacao_canal"],
            prazo_estimado = r["prazo_estimado"],
            responsavel_atendimento_unidade = r.get("responsavel_atendimento_unidade", ""),
            responsavel_atendimento_equipe = r.get("responsavel_atendimento_equipe", ""),
            sla_descricao = r["sla_descricao"],
            sla_tempo_resposta_horas = r["sla_tempo_resposta_horas"],
            sla_tempo_solucao_horas = r["sla_tempo_solucao_horas"],
            sla_horario_atendimento = r["sla_horario_atendimento"],
            sla_observacoes = r["sla_observacoes"],
            contrato_resumo = r["contrato_resumo"],
            prioridade = r["prioridade"],
            periodicidade_revisao = r["periodicidade_revisao"],
            data_ultima_revisao = data_ultima_revisao,
            autor_ultima_revisao = r.get("autor_ultima_revisao", ""),
            data_proxima_revisao = data_proxima_revisao,
            criado_em = criado_em,
            atualizado_em = atualizado_em,
            vinculos = vinculos
        )