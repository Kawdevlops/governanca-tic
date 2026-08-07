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

from pydantic import BaseModel, Field, EmailStr, ConfigDict, model_validator
"""
BaseModel -> cria um modelo de dados valido
Field -> adiciona regras ao campo do atributo
EmailStr -> verifica se o texto é um e-mail válido
ConfigDict -> configura o comportamento do modelo
model_validator -> cria validações mais inteligentes envolvendo varios campos
"""
from datetime import date, datetime
from typing import Optional  # diz se o campo é opcional
from enum import Enum  # lista de opções fixas

DESCRICOES_BASEDADOS = {

    # DICIONARIOS DOS ATRIBUTOS, aparece no endpoint oque precisa ser preenchido
    # Vínculo e metadados de sistema
    "nome_sistema": "Nome do Sistema de informação ao qual esta base está vinculada, quando aplicável.",
    "criado_em_sistema": "Data e hora de criação do registro no catálogo interno.",
    "atualizado_em_sistema": "Data e hora da última atualização do registro no catálogo interno.",
    "element_id": "Identificador único do elemento no banco de dados",

    # Descrição do cadastro
    "orgao": "Órgão/entidade responsável pela base (ex: SUB-AD, Secretaria Municipal de Finanças).",
    "setor": "Setor específico do órgão responsável pela base (ex: Departamento de Tributos Imobiliários).",
    "titulo": "Nome do conjunto de dados. Evite usar apenas a sigla — escreva por extenso na primeira menção.",
    "descricao": "Breve descrição sobre a criação do conjunto de dados, objetivos e finalidades.",
    "tema": "Área temática à qual o conjunto de dados está vinculado.",
    "palavras_chave": "Palavras que resumem os principais aspectos do conjunto de dados (máx. 30 caracteres cada).",
    "area_tecnica_responsavel": "Área técnica do órgão/entidade responsável pelo conjunto de dados.",
    "email_area_tecnica": "E-mail de contato da área técnica responsável pelo conjunto de dados.",
    "data_publicado_dados": "Data de publicação/catalogação no Portal de Dados Abertos ou similar.",
    "data_atualizacao_dados": "Data mais recente de atualização ou modificação do conjunto de dados.",

    # Dados técnicos
    "formatos": "Formato(s) em que o conjunto de dados será disponibilizado.",

    # Conectividade
    "possui_integracao_externa": "Indica se a base é acessada ou atualizada por outros sistemas externos.",

    # Dados pessoais e sensíveis (LGPD)
    "possui_dados_pessoais": "Indica se a base contém dados que identificam uma pessoa (nome, CPF, endereço etc.).",
    "categorias_dados_pessoais": "Categorias de dados pessoais presentes na base. Obrigatório se possui_dados_pessoais=Sim.",
    "possui_dados_sensiveis": "Indica se a base contém dados pessoais sensíveis (LGPD art. 5º, II).",
    "categorias_dados_sensiveis": "Categorias de dados sensíveis presentes na base. Obrigatório se possui_dados_sensiveis=Sim.",

    # Classificação da informação
    "possui_informacao_sigilosa": "Indica se existem informações classificadas em algum grau de sigilo na base.",
}


# ENUMS Listas fechada de opções fixa ao preencher
class RespostaSimNao(str, Enum):
    SIM = "Sim"
    NAO = "Não"


class TemaBaseDados(str, Enum):
    ADMINISTRACAO_E_GESTAO = "Administração e Gestão"
    CULTURA = "Cultura"
    DEMOGRAFIA = "Demografia"
    DIREITOS_HUMANOS = "Direitos Humanos"
    EDUCACAO = "Educação"
    ESPORTES_E_LAZER = "Esportes e Lazer"
    HABITACAO = "Habitação"
    INFRAESTRUTURA_E_URBANISMO = "Infraestrutura e Urbanismo"
    MEIO_AMBIENTE = "Meio Ambiente"
    NEGOCIOS = "Negócios"
    PARTICIPACAO_SOCIAL = "Participação Social"
    ORCAMENTO_E_FINANCAS = "Orçamento e Finanças"
    SAUDE_E_BEM_ESTAR = "Saúde e Bem-Estar"
    TRABALHO_E_RENDA = "Trabalho e Renda"
    SEGURANCA_URBANA = "Segurança Urbana"
    TRANSPORTES_E_MOBILIDADE = "Transportes e Mobilidade"


class SituacaoBaseDados(str, Enum):
    ATIVA = "Ativa"
    INATIVA = "Inativa"


class FormatoArquivo(str, Enum):
    CSV = "CSV"
    ODS = "ODS"
    JSON = "JSON"
    GEOJSON = "GeoJSON"
    XML = "XML"
    SHP = "SHP"
    DOC = "DOC"
    TXT = "TXT"
    ODT = "ODT"
    JPEG = "JPEG"
    API = "API"
    OUTROS = "Outros"


# CLASSE BASE PRINCIPAL definindo como vai ser a base de dados
class BaseDadosBase(BaseModel):

    # Descrição do cadastro
    orgao: str = Field(..., min_length=3, max_length=200, description=DESCRICOES_BASEDADOS["orgao"])
    setor: Optional[str] = Field(None, min_length=3, max_length=200, description=DESCRICOES_BASEDADOS["setor"])
    titulo: str = Field(..., min_length=3, max_length=200, description=DESCRICOES_BASEDADOS["titulo"])
    descricao: str = Field(..., min_length=10, max_length=1000, description=DESCRICOES_BASEDADOS["descricao"])
    tema: TemaBaseDados = Field(..., description=DESCRICOES_BASEDADOS["tema"])
    palavras_chave: list[str] = Field(default_factory=list, max_length=10, description=DESCRICOES_BASEDADOS["palavras_chave"])
    area_tecnica_responsavel: str = Field(..., min_length=3, max_length=200, description=DESCRICOES_BASEDADOS["area_tecnica_responsavel"])
    email_area_tecnica: EmailStr = Field(..., description=DESCRICOES_BASEDADOS["email_area_tecnica"])
    data_publicado_dados: date = Field(..., description=DESCRICOES_BASEDADOS["data_publicado_dados"])
    data_atualizacao_dados: date = Field(..., description=DESCRICOES_BASEDADOS["data_atualizacao_dados"])

    # Dados técnicos
    formatos: list[FormatoArquivo] = Field(..., min_length=1, description=DESCRICOES_BASEDADOS["formatos"])

    # Conectividade
    possui_integracao_externa: RespostaSimNao = Field(..., description=DESCRICOES_BASEDADOS["possui_integracao_externa"])

    # Dados pessoais e sensíveis (LGPD)
    possui_dados_pessoais: RespostaSimNao = Field(..., description=DESCRICOES_BASEDADOS["possui_dados_pessoais"])
    categorias_dados_pessoais: Optional[str] = Field(None, min_length=3, description=DESCRICOES_BASEDADOS["categorias_dados_pessoais"])
    possui_dados_sensiveis: RespostaSimNao = Field(..., description=DESCRICOES_BASEDADOS["possui_dados_sensiveis"])
    categorias_dados_sensiveis: Optional[str] = Field(None, min_length=3, description=DESCRICOES_BASEDADOS["categorias_dados_sensiveis"])

    # Classificação da informação
    possui_informacao_sigilosa: RespostaSimNao = Field(..., description=DESCRICOES_BASEDADOS["possui_informacao_sigilosa"])

    # Vínculo e metadados de sistema
    nome_sistema: Optional[str] = Field(None, min_length=3, max_length=200, description=DESCRICOES_BASEDADOS["nome_sistema"])

    model_config = ConfigDict(use_enum_values=True)

    @model_validator(mode="after")
    def validar_campos_condicionais(self):

        if self.possui_dados_pessoais == RespostaSimNao.SIM and not self.categorias_dados_pessoais:
            raise ValueError(
                f"'{DESCRICOES_BASEDADOS['categorias_dados_pessoais']}' "
                f"Obrigatório quando possui_dados_pessoais=Sim."
            )

        if self.possui_dados_sensiveis == RespostaSimNao.SIM and not self.categorias_dados_sensiveis:
            raise ValueError(
                f"'{DESCRICOES_BASEDADOS['categorias_dados_sensiveis']}' "
                f"Obrigatório quando possui_dados_sensiveis=Sim."
            )

        return self


# CLASSES DE OPERAÇÃO
class BaseDadosCreate(BaseDadosBase):
    pass


class BaseDadosUpdate(BaseModel):
    orgao: Optional[str] = Field(None, min_length=3, max_length=200, description=DESCRICOES_BASEDADOS["orgao"])
    setor: Optional[str] = Field(None, min_length=3, max_length=200, description=DESCRICOES_BASEDADOS["setor"])
    titulo: Optional[str] = Field(None, min_length=3, max_length=200, description=DESCRICOES_BASEDADOS["titulo"])
    descricao: Optional[str] = Field(None, min_length=10, max_length=1000, description=DESCRICOES_BASEDADOS["descricao"])
    tema: Optional[TemaBaseDados] = Field(None, description=DESCRICOES_BASEDADOS["tema"])
    palavras_chave: Optional[list[str]] = Field(None, max_length=10, description=DESCRICOES_BASEDADOS["palavras_chave"])
    area_tecnica_responsavel: Optional[str] = Field(None, min_length=3, max_length=200, description=DESCRICOES_BASEDADOS["area_tecnica_responsavel"])
    email_area_tecnica: Optional[EmailStr] = Field(None, description=DESCRICOES_BASEDADOS["email_area_tecnica"])
    data_atualizacao_dados: Optional[date] = Field(None, description=DESCRICOES_BASEDADOS["data_atualizacao_dados"])
    data_publicado_dados: Optional[date] = Field(None, description=DESCRICOES_BASEDADOS["data_publicado_dados"])
    formatos: Optional[list[FormatoArquivo]] = Field(None, description=DESCRICOES_BASEDADOS["formatos"])
    possui_integracao_externa: Optional[RespostaSimNao] = Field(None, description=DESCRICOES_BASEDADOS["possui_integracao_externa"])
    possui_dados_pessoais: Optional[RespostaSimNao] = Field(None, description=DESCRICOES_BASEDADOS["possui_dados_pessoais"])
    categorias_dados_pessoais: Optional[str] = Field(None, min_length=3, description=DESCRICOES_BASEDADOS["categorias_dados_pessoais"])
    possui_dados_sensiveis: Optional[RespostaSimNao] = Field(None, description=DESCRICOES_BASEDADOS["possui_dados_sensiveis"])
    categorias_dados_sensiveis: Optional[str] = Field(None, min_length=3, description=DESCRICOES_BASEDADOS["categorias_dados_sensiveis"])
    possui_informacao_sigilosa: Optional[RespostaSimNao] = Field(None, description=DESCRICOES_BASEDADOS["possui_informacao_sigilosa"])
    nome_sistema: Optional[str] = Field(None, min_length=3, max_length=200, description=DESCRICOES_BASEDADOS["nome_sistema"])

    model_config = ConfigDict(use_enum_values=True)


# MODELO DE RESPOSTA
class BaseDadosResponse(BaseDadosBase):
    element_id: str = Field(..., description=DESCRICOES_BASEDADOS.get("element_id"))
    criado_em_sistema: datetime = Field(..., description=DESCRICOES_BASEDADOS.get("criado_em_sistema"))
    atualizado_em_sistema: Optional[datetime] = Field(None, description=DESCRICOES_BASEDADOS.get("atualizado_em_sistema"))

    model_config = ConfigDict(use_enum_values=True)