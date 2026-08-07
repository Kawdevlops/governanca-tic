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
from app.models.basedados import BaseDadosResponse, BaseDadosCreate, BaseDadosUpdate


class BaseDadosRepository:
    def __init__(self, driver: AsyncDriver):
        self.driver = driver

    def _query_base(self) -> str:
        return """
            CALL (b) {
                WITH b
                OPTIONAL MATCH (sis:Sistema)-[:POSSUI]->(b)
                RETURN sis.nome AS sistema_vinculado
            }
            CALL (b) {
                WITH b
                OPTIONAL MATCH (o:OrgaoSetorial)-[:RESPONSAVEL_POR]->(b)
                RETURN o.name AS orgao_vinculado
            }
            CALL (b) {
                WITH b
                OPTIONAL MATCH (s:Setor)-[:GERE]->(b)
                RETURN s.name AS setor_vinculado
            }
            RETURN
                elementId(b) AS element_id,
                orgao_vinculado AS orgao,
                setor_vinculado AS setor,
                coalesce(b.nome_sistema, sistema_vinculado) AS nome_sistema,
                b.titulo AS titulo,
                b.descricao AS descricao,
                b.tema AS tema,
                b.palavras_chave AS palavras_chave,
                b.area_tecnica_responsavel AS area_tecnica_responsavel,
                b.email_area_tecnica AS email_area_tecnica,
                b.data_publicado_dados AS data_publicado_dados,
                b.data_atualizacao_dados AS data_atualizacao_dados,
                b.possui_integracao_externa AS possui_integracao_externa,
                b.possui_dados_pessoais AS possui_dados_pessoais,
                b.categorias_dados_pessoais AS categorias_dados_pessoais,
                b.possui_dados_sensiveis AS possui_dados_sensiveis,
                b.categorias_dados_sensiveis AS categorias_dados_sensiveis,
                b.possui_informacao_sigilosa AS possui_informacao_sigilosa,
                b.formatos AS formatos,
                b.criado_em_sistema AS criado_em_sistema,
                b.atualizado_em_sistema AS atualizado_em_sistema
        """

    async def listar(self) -> list[BaseDadosResponse]:
        async with self.driver.session() as session:
            result = await session.run(f"""
                MATCH (b:BaseDados)
                {self._query_base()}
                ORDER BY b.titulo
            """)
            registros = await result.data()

        return [self._mapear(r) for r in registros]

    async def listar_orgaos_existentes(self) -> list[str]:
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (o:OrgaoSetorial)
                RETURN DISTINCT o.name AS nome
                ORDER BY o.name
            """)
            registros = await result.data()

        return [r["nome"] for r in registros]

    async def listar_setores_existentes(self, orgao: str | None = None) -> list[str]:
        async with self.driver.session() as session:
            if orgao:
                result = await session.run("""
                    MATCH (o:OrgaoSetorial {name: $orgao})-[:POSSUI_SETOR]->(s:Setor)
                    RETURN DISTINCT s.name AS nome
                    ORDER BY s.name
                """, orgao=orgao)
            else:
                result = await session.run("""
                    MATCH (s:Setor)
                    RETURN DISTINCT s.name AS nome
                    ORDER BY s.name
                """)
            registros = await result.data()

        return [r["nome"] for r in registros]

    async def criar(self, payload: BaseDadosCreate) -> BaseDadosResponse:
        props = payload.model_dump(exclude_none=True, mode="json", exclude={"orgao", "setor"})
        props["criado_em_sistema"] = datetime.now(timezone.utc)
        props["atualizado_em_sistema"] = datetime.now(timezone.utc)

        async with self.driver.session() as session:
            query = f"""
                MERGE (o:OrgaoSetorial {{name: $orgao}})
                CREATE (b:BaseDados)
                SET b += $props
                MERGE (o)-[:RESPONSAVEL_POR]->(b)
                WITH o, b
            """
            if payload.setor:
                query += """
                    MERGE (o)-[:POSSUI_SETOR]->(s:Setor {name: $setor})
                    MERGE (s)-[:GERE]->(b)
                    WITH b
                """
            else:
                query += "WITH b\n"
            query += self._query_base()

            result = await session.run(query, props=props, orgao=payload.orgao, setor=payload.setor)
            registro = await result.single()

        return self._mapear(dict(registro))

    async def obter_por_element_id(self, element_id: str) -> BaseDadosResponse | None:
        async with self.driver.session() as session:
            result = await session.run(f"""
                MATCH (b:BaseDados)
                WHERE elementId(b) = $p_element_id
                {self._query_base()}
            """, p_element_id=element_id)
            registro = await result.single()

        if not registro:
            return None

        return self._mapear(dict(registro))

    async def obter_por_titulo(self, titulo: str) -> BaseDadosResponse | None:
        async with self.driver.session() as session:
            result = await session.run(f"""
                MATCH (b:BaseDados {{titulo: $p_titulo}})
                {self._query_base()}
            """, p_titulo=titulo)
            registro = await result.single()

        if not registro:
            return None

        return self._mapear(dict(registro))

    async def buscar_por_tema(self, tema: str) -> list[BaseDadosResponse]:
        async with self.driver.session() as session:
            result = await session.run(f"""
                MATCH (b:BaseDados {{tema: $p_tema}})
                {self._query_base()}
                ORDER BY b.titulo
            """, p_tema=tema)
            registros = await result.data()

        return [self._mapear(r) for r in registros]

    async def atualizar(self, titulo: str, payload: BaseDadosUpdate) -> BaseDadosResponse | None:
        props = payload.model_dump(exclude_none=True, mode="json", exclude={"orgao", "setor"})

        if not props and payload.orgao is None and payload.setor is None:
            return await self.obter_por_titulo(titulo)

        props["atualizado_em_sistema"] = datetime.now(timezone.utc)

        async with self.driver.session() as session:
            query = "MATCH (b:BaseDados {titulo: $titulo_ref})\n"
            if props:
                query += "SET b += $props\n"

            if payload.orgao is not None:
                query += """
                    WITH b
                    OPTIONAL MATCH (:OrgaoSetorial)-[r_org:RESPONSAVEL_POR]->(b)
                    DELETE r_org
                    WITH b
                    OPTIONAL MATCH (:Setor)-[r_set:GERE]->(b)
                    DELETE r_set
                    WITH b
                    MERGE (o:OrgaoSetorial {name: $orgao})
                    MERGE (o)-[:RESPONSAVEL_POR]->(b)
                    WITH o, b
                """
                if payload.setor:
                    query += """
                        MERGE (o)-[:POSSUI_SETOR]->(s:Setor {name: $setor})
                        MERGE (s)-[:GERE]->(b)
                        WITH b
                    """
                else:
                    query += "WITH b\n"
            elif payload.setor is not None:
                query += """
                    WITH b
                    OPTIONAL MATCH (o:OrgaoSetorial)-[:RESPONSAVEL_POR]->(b)
                    OPTIONAL MATCH (:Setor)-[r_set:GERE]->(b)
                    DELETE r_set
                    WITH o, b
                    MERGE (o)-[:POSSUI_SETOR]->(s:Setor {name: $setor})
                    MERGE (s)-[:GERE]->(b)
                    WITH b
                """
            else:
                query += "WITH b\n"

            query += self._query_base()
            result = await session.run(query, titulo_ref=titulo, props=props, orgao=payload.orgao, setor=payload.setor)
            registro = await result.single()

        if not registro:
            return None

        return self._mapear(dict(registro))

    async def deletar(self, titulo: str) -> bool:
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (b:BaseDados {titulo: $p_titulo})
                WITH b, count(b) AS total
                DETACH DELETE b
                RETURN total > 0 AS removido
            """, p_titulo=titulo)
            registro = await result.single()

        return bool(registro and registro["removido"])

    def _mapear(self, r: dict) -> BaseDadosResponse:
        def _to_native(campo):
            valor = r.get(campo)
            return valor.to_native() if valor is not None and hasattr(valor, "to_native") else valor

        def _para_lista(valor):
            if valor is None:
                return []
            if isinstance(valor, list):
                return valor
            return [valor] if valor else []

        return BaseDadosResponse(
            element_id=r["element_id"],
            orgao=r.get("orgao", ""),
            setor=r.get("setor"),
            titulo=r.get("titulo", ""),
            descricao=r.get("descricao", ""),
            tema=r.get("tema", ""),
            palavras_chave=_para_lista(r.get("palavras_chave")),
            area_tecnica_responsavel=r.get("area_tecnica_responsavel", ""),
            email_area_tecnica=r.get("email_area_tecnica", ""),
            data_publicado_dados=_to_native("data_publicado_dados"),
            data_atualizacao_dados=_to_native("data_atualizacao_dados"),
            formatos=_para_lista(r.get("formatos")),
            possui_integracao_externa=r.get("possui_integracao_externa", ""),
            possui_dados_pessoais=r.get("possui_dados_pessoais", ""),
            categorias_dados_pessoais=r.get("categorias_dados_pessoais"),
            possui_dados_sensiveis=r.get("possui_dados_sensiveis", ""),
            categorias_dados_sensiveis=r.get("categorias_dados_sensiveis"),
            possui_informacao_sigilosa=r.get("possui_informacao_sigilosa", ""),
            nome_sistema=r.get("nome_sistema"),
            criado_em_sistema=_to_native("criado_em_sistema"),
            atualizado_em_sistema=_to_native("atualizado_em_sistema"),
        )