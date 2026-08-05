from neo4j import AsyncDriver
from datetime import datetime, timezone
from app.models.basedados import BaseDadosResponse, BaseDadosCreate, BaseDadosUpdate


class BaseDadosRepository:
    def __init__(self, driver: AsyncDriver):
        self.driver = driver

    def _query_base_return(self) -> str:
        """
        Query base para retornar todos os campos de BaseDados.
        Inclui relacionamento opcional com Sistema.
        """
        return """
            CALL (b) {
                WITH b
                OPTIONAL MATCH (sis:Sistema)-[:POSSUI]->(b)
                RETURN sis.nome AS sistema_vinculado
            }
            RETURN
                elementId(b) AS responsavel_id,
                coalesce(b.nome_sistema, sistema_vinculado) AS nome_sistema,
                b.sigla AS sigla,
                b.orgao AS orgao,
                b.titulo AS titulo,
                b.descricao AS descricao,
                b.tema AS tema,
                b.palavras_chave AS palavras_chave,
                b.area_tecnica_responsavel AS area_tecnica_responsavel,
                b.email_area_tecnica AS email_area_tecnica,
                b.data_publicacao_dados AS data_publicacao_dados,
                b.data_atualizacao_dados AS data_atualizacao_dados,
                b.possui_integracao_externa AS possui_integracao_externa,
                b.possui_dados_pessoais AS possui_dados_pessoais,
                b.categorias_dados_pessoais AS categorias_dados_pessoais,
                b.possui_dados_sensiveis AS possui_dados_sensiveis,
                b.categorias_dados_sensiveis AS categorias_dados_sensiveis,
                b.possui_informacao_sigilosa AS possui_informacao_sigilosa,
                b.formatos AS formatos,
                
        """

    def _query_base(self) -> str:
        return self._query_base_return() + """
            , b.criado_em_sistema AS criado_em_sistema
            , b.atualizado_em_sistema AS atualizado_em_sistema
        """

# Quando alguém chamar listar(), eu vou conversar com o banco de forma assíncrona e devolver várias bases de dados já organizadas.
    async def listar(self) -> list[BaseDadosResponse]:
        async with self.driver.session() as session: # abre conexão → cria sessão → usa sessão → fecha sessão
            query = """
                MATCH (b:BaseDados)  // Encontra todos os nós do tipo BaseDados
                """ + self._query_base() + """
                ORDER BY b.titulo // Coloque em ordem alfabética pelo título.
            """
            result = await session.run(query) # Envie a consulta para o Neo4j e espere a resposta
            registros = await result.data() # Transforma o resultado em uma lista de registros.
        return [self._mapear(r) for r in registros] # resulta em uma lista 


    async def criar(self, payload: BaseDadosCreate) -> BaseDadosResponse:
        props = payload.model_dump(exclude_none=True, mode="json") # pyload é obj pydantic, props vira algo "dict" exclude remove campos vazios
        props["criado_em_sistema"] = datetime.now(timezone.utc) # coloca data do sistema ex: criado_em_sistema": "2026-08-05T17:10:00Z
        props["atualizado_em_sistema"] = datetime.now(timezone.utc)

        async with self.driver.session() as session: # abre sessão 
            query = """
                CREATE (b:BaseDados) // Crie um novo nó chamado b do tipo BaseDados
                SET b += $props // Pegue tudo que está dentro de props e coloque dentro do nó b
                WITH b
            """ + self._query_base_return() + """
                , b.criado_em_sistema AS criado_em_sistema
                , b.atualizado_em_sistema AS atualizado_em_sistema
            """
            result = await session.run(query, props=props) # Execute a query e envie junto o dicionário props
            registro = await result.single() # Me devolva apenas um registro
            
            if not registro:
                raise RuntimeError("Falha ao criar base de dados")
            
        return self._mapear(dict(registro))


    async def obter_por_responsavel_id(self, responsavel_id: str) -> BaseDadosResponse | None:
        async with self.driver.session() as session:
            query = """
                MATCH (b:BaseDados)
                WHERE elementId(b) = $p_responsavel_id
            """ + self._query_base()

            result = await session.run(query, p_responsavel_id=responsavel_id) # Executa query
            registro = await result.single() # tras um registro

            if not registro:
                return None

            return self._mapear(dict(registro))


    async def obter_por_titulo(self, titulo: str) -> BaseDadosResponse | None:
                async with self.driver.session() as session:
                    query = """
                        MATCH (b:BaseDados {titulo: $p_titulo})
                    """ + self._query_base()
        
                    result = await session.run(query, p_titulo=titulo)
                    registro = await result.single()
        
                    if not registro:
                        return None
        
                    return self._mapear(dict(registro))


    async def buscar_por_tema(self, tema: str) -> list[BaseDadosResponse]:
            async with self.driver.session() as session:
                query = """
                    MATCH (b:BaseDados {tema: $p_tema})
                """ + self._query_base() + """
                    ORDER BY b.titulo
                """
                result = await session.run(query, p_tema=tema)
                registros = await result.data()
            return [self._mapear(r) for r in registros]

    
    async def atualizar(self, titulo: str, payload: BaseDadosUpdate) -> BaseDadosResponse | None: # Atualize a base cujo título é X usando os dados enviados no payload.
        props = payload.model_dump(exclude_none=True, mode="json") # pega apenas os campos enviados pelo usuario, o model altera apenas oque foi enviado

        if not props:
            return await self.obter_por_titulo(titulo) # se não atualizou devolve a mesma base caso contrario devolve no () o titulo

        props["atualizado_em_sistema"] = datetime.now(timezone.utc) # atualiza a data da ultima modificação

        async with self.driver.session() as session:
            query = """
                MATCH (b:BaseDados {titulo: $titulo_ref})
                SET b += $props // Pegue tudo que está em props e aplique no nó b. / Atualiza somente os campos que vieram no payload.
                WITH b // Continue trabalhando com o nó atualizado
            """ + self._query_base_return() + """
                , b.criado_em_sistema AS criado_em_sistema
                , b.atualizado_em_sistema AS atualizado_em_sistema
            """
            result = await session.run(query, titulo_ref=titulo, props=props)
            registro = await result.single()

        if not registro:
            return None

        return self._mapear(dict(registro))


    async def deletar(self, titulo: str) -> bool:
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (b:BaseDados {titulo: $p_titulo}) // Procure a base com esse título
                WITH b, count(b) AS total            // conta quantas bases foram encontradas 0 não existe / 1 existe
                DETACH DELETE b                     // Apaga a base e também qualquer relacionamento ligado a ela
                RETURN total > 0 AS removido        // Devolva True se encontrou algo para remover, senão False
            """, p_titulo=titulo)
            registro = await result.single()

        return bool(registro and registro["removido"])


    def _mapear(self, r: dict) -> BaseDadosResponse: # Receba um dicionário vindo do Neo4j e devolva um BaseDadosResponse.
            
            def _to_native(campo): # converte a data do neo4j para datetime python
                valor = r.get(campo)
                return valor.to_native() if valor is not None and hasattr(valor, "to_native") else valor
    
            def _para_lista(valor):
                if valor is None:
                    return []
                if isinstance(valor, list):
                    return valor
                return [valor] if valor else []
    
            return BaseDadosResponse(
                # Cadastro padrão
                responsavel_id=r["responsavel_id"], # [ dentro] Pegue o campo titulo. Se não existir, use string vazia. 
                orgao=r.get("orgao", ""),
                sigla=r.get("sigla", ""),
                
                # Descrição e caracterização
                titulo=r.get("titulo", ""),
                descricao=r.get("descricao", ""),
                tema=r.get("tema", ""),
                palavras_chave=_para_lista(r.get("palavras_chave")), # Pegue palavras_chave e garanta que seja uma lista.
                area_tecnica_responsavel=r.get("area_tecnica_responsavel", ""),
                email_area_tecnica=r.get("email_area_tecnica", ""),
                data_publicacao_dados=_to_native("data_publicacao_dados"),
                data_atualizacao_dados=_to_native("data_atualizacao_dados"),
                
                # Dados técnicos
                formatos=_para_lista(r.get("formatos")),
                
                # Conectividade
                possui_integracao_externa=r.get("possui_integracao_externa", ""),
                
                
                # Dados pessoais e sensíveis (LGPD)
                possui_dados_pessoais=r.get("possui_dados_pessoais", ""),
                categorias_dados_pessoais=r.get("categorias_dados_pessoais"),
                possui_dados_sensiveis=r.get("possui_dados_sensiveis", ""),
                possui_dados_sensiveis=r.get("possui_dados_sensiveis"),
                # Classificação da informação
                possui_informacao_sigilosa=r.get("possui_informacao_sigilosa", ""),
                
                # Vínculo e metadados de sistema
                nome_sistema=r.get("nome_sistema"),
                criado_em_sistema=_to_native("criado_em_sistema"),
                atualizado_em_sistema=_to_native("atualizado_em_sistema"),
            )

   


    

   

     