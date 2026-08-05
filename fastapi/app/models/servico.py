from pydantic import BaseModel, Field, ConfigDict
from app.models.vinculo import Vinculo
from datetime import date, datetime
from typing import Optional
from enum import Enum

DESCRICOES_SERVICO = {

    "categoria" : "Categoria funcional do serviço de TIC.",
    "nome": "Nome oficial do serviço, conforme será exibido para consulta e gestão.",
    "descricao" : "Resumo do que o serviço faz, incluindo sua finalidade principal.",
    "publico_alvo": "Unidades, perfis ou grupos que podem utilizar ou solicitar o serviço.",
    "status": "Situação atual do serviço, indicando se está ativo, em desenvolvimento, obsoleto ou suspenso.",

    "solicitacao_canal" : "Canal ou ferramenta pelo qual a solicitação deve ser registrada ou encaminhada.",
    "solicitacao_pre_requisitos" : "Condições, documentos ou dependências necessárias antes de solicitar o serviço.",
    "solicitacao_descricao_procedimento" : "Passo a passo ou orientação para abertura da solicitação.",
    "prazo_estimado" : "Prazo esperado para atendimento, implantação ou conclusão da solicitação.",

    "responsavel_atendimento_unidade": "Unidade organizacional responsável por atender o serviço.",
    "responsavel_atendimento_equipe": "Equipe, célula ou time operacional responsável pelo atendimento.",

    "sla_descricao" : "Texto explicativo sobre o SLA aplicado ao serviço.",
    "sla_tempo_resposta_horas" : "Tempo máximo esperado para início da resposta ao chamado, em horas.",
    "sla_tempo_solucao_horas" : "Tempo máximo esperado para solução do chamado, em horas.",
    "sla_horario_atendimento" : "Janela de horário em que o serviço ou suporte é prestado.",
    "sla_observacoes" : "Observações complementares sobre regras, exceções ou limitações do SLA.",

    "contrato_resumo" : "Resumo do contrato, acordo ou instrumento que sustenta o serviço.",
    "prioridade" : "Nível de prioridade do serviço, considerando criticidade e impacto.",

    "periodicidade_revisao" : "Frequência com que o cadastro do serviço deve ser revisado.",
    "data_ultima_revisao" : "Data em que o serviço foi revisado pela última vez.",
    "autor_ultima_revisao" : "Nome de quem realizou ou registrou a última revisão.",
    "data_proxima_revisao" : "Data prevista para a próxima revisão do cadastro.",

    "criado_em" : "Data e hora de criação do serviço.",
    "atualizado_em" : "Data e hora da última atualização do serviço.",

    "element_id" : "Identificador único do serviço no banco de dados."
}

class CategoriaServico(str, Enum):
    # Antes do alinhamento com o CATSER
    #CAPACITACAO = "Capacitação"
    #COMUNICACAO_VOZ = "Comunicação e Voz"
    #CONSULTORIA_GESTAO_CONTRATUAL = "Consultoria e Gestão Contratual"
    #DESENVOLVIMENTO_SISTEMAS = "Desenvolvimento de Sistemas"
    #IMPRESSAO_DISPOSITIVOS_CAMPO = "Impressão e Dispositivos de Campo"
    #INFRAESTRUTURA_CONECTIVIDADE = "Infraestrutura e Conectividade"
    #LICENCAS_FERRAMENTAS_DIGITAIS = "Licenças e Ferramentas Digitais"

    # Alinhado aos Grupos do CATSER: https://dadosabertos.compras.gov.br/modulo-servico/2_consultarDivisaoServico?pagina=1&codigoSecao=1&statusDivisao=true
    DESENVOLVIMENTO_SISTEMAS = "Desenvolvimento, Manutenção e Sustentação de Software"
    COMPUTACAO_NUVEM = "Computação em Nuvem"
    TELECOMUNICACAO_TELEFONIA = "Telecomunicação e Telefonia"
    OUTSOURCE_IMPRESSAO = "Outsourcing de Impressão"
    INFRAESTRUTURA_TIC = "Infraestrutura de TIC"
    CONSULTORIA_GESTAO_CONTRATUAL = "Pesquisa, Análise de Dados e Indicadores, Consultoria e Projetos de TIC"
    LICENCIAMENTO = "Arrendamento, Licenciamento de Direitos e Transferência de Tecnologia"

    # Existem subclassificações (Classes) no CATSER: https://dadosabertos.compras.gov.br/modulo-servico/4_consultarClasseServico?pagina=1&codigoGrupo=131&statusGrupo=true
    

class StatusServico(str, Enum):
    ATIVO = "ativo"
    EM_DESENVOLVIMENTO = "em_desenvolvimento"
    OBSOLETO = "obsoleto"
    SUSPENSO = "suspenso"


class PrioridadeServico(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica" 


class ServicoBase(BaseModel):
    categoria: CategoriaServico = Field(..., description=DESCRICOES_SERVICO.get("categoria"))
    nome: str = Field(..., min_length=3, max_length=150, description=DESCRICOES_SERVICO.get("nome"))
    descricao: str = Field(..., min_length=10, description=DESCRICOES_SERVICO.get("descricao"))
    publico_alvo: str = Field(..., min_length=3, description=DESCRICOES_SERVICO.get("publico_alvo"))
    status: StatusServico = Field(..., description=DESCRICOES_SERVICO.get("status"))
    model_config = ConfigDict(use_enum_values=True)


class ServicoDetalhes(ServicoBase):
    solicitacao_canal: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("solicitacao_canal"))
    solicitacao_pre_requisitos: Optional[str] = Field(None, min_length=3, description=DESCRICOES_SERVICO.get("solicitacao_pre_requisitos"))
    solicitacao_descricao_procedimento: Optional[str] = Field(None, min_length=3, description=DESCRICOES_SERVICO.get("solicitacao_descricao_procedimento"))
    prazo_estimado: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("prazo_estimado"))

    responsavel_atendimento_unidade: str = Field(..., min_length=3, max_length=150, description=DESCRICOES_SERVICO.get("responsavel_atendimento_unidade"))
    responsavel_atendimento_equipe: str = Field(..., min_length=3, max_length=150, description=DESCRICOES_SERVICO.get("responsavel_atendimento_equipe"))

    sla_descricao: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("sla_descricao"))
    sla_tempo_resposta_horas: Optional[int] = Field(None, ge=0, description=DESCRICOES_SERVICO.get("sla_tempo_resposta_horas"))
    sla_tempo_solucao_horas: Optional[int] = Field(None, ge=0, description=DESCRICOES_SERVICO.get("sla_tempo_solucao_horas"))
    sla_horario_atendimento: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("sla_horario_atendimento"))
    sla_observacoes: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("sla_observacoes"))

    contrato_resumo: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("contrato_resumo"))
    prioridade: Optional[PrioridadeServico] = Field(None, description=DESCRICOES_SERVICO.get("prioridade"))

    periodicidade_revisao: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("periodicidade_revisao"))
    data_ultima_revisao: date = Field(..., description=DESCRICOES_SERVICO.get("data_ultima_revisao"))
    autor_ultima_revisao: str = Field(..., min_length=3, max_length=150, description=DESCRICOES_SERVICO.get("autor_ultima_revisao"))
    data_proxima_revisao: Optional[date] = Field(None, description=DESCRICOES_SERVICO.get("data_proxima_revisao"))

    #vinculo_risco (dependencias: List[str] = Field(default_factory=list)) (risco:Risco)-[:AFETA]->(servico:ServicoTIC)
    #vinculo_contrato (contrato:Contrato)-[:SUSTENTA]->(servico:ServicoTIC)
    #vinculo_indicador (indicador:Indicador)-[:MEDE]->(servico:ServicoTIC)
    #vinculo_sistema


class ServicoVinculo(ServicoDetalhes):
    vinculos: list[Vinculo] = Field(default_factory=list)


class ServicoCreate(ServicoDetalhes):
    pass


class ServicoUpdate(BaseModel):
    categoria: Optional[CategoriaServico] = Field(None, description=DESCRICOES_SERVICO.get("categoria"))
    nome: Optional[str] = Field(None, min_length=3, max_length=150, description=DESCRICOES_SERVICO.get("nome"))
    descricao: Optional[str] = Field(None, min_length=10, description=DESCRICOES_SERVICO.get("descricao"))
    publico_alvo: Optional[str] = Field(None, min_length=3, description=DESCRICOES_SERVICO.get("publico_alvo"))
    status: Optional[StatusServico] = Field(None, description=DESCRICOES_SERVICO.get("status"))

    solicitacao_pre_requisitos: Optional[str] = Field(None, min_length=3, description=DESCRICOES_SERVICO.get("solicitacao_pre_requisitos"))
    solicitacao_descricao_procedimento: Optional[str] = Field(None, min_length=3, description=DESCRICOES_SERVICO.get("solicitacao_descricao_procedimento"))
    solicitacao_canal: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("solicitacao_canal"))
    prazo_estimado: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("prazo_estimado"))

    responsavel_atendimento_unidade: Optional[str] = Field(None, min_length=3, max_length=150, description=DESCRICOES_SERVICO.get("responsavel_atendimento_unidade"))
    responsavel_atendimento_equipe: Optional[str] = Field(None, min_length=3, max_length=150, description=DESCRICOES_SERVICO.get("responsavel_atendimento_equipe"))

    sla_descricao: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("sla_descricao"))
    sla_tempo_resposta_horas: Optional[int] = Field(None, ge=0, description=DESCRICOES_SERVICO.get("sla_tempo_resposta_horas"))
    sla_tempo_solucao_horas: Optional[int] = Field(None, ge=0,  description=DESCRICOES_SERVICO.get("sla_tempo_solucao_horas"))
    sla_horario_atendimento: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("sla_horario_atendimento"))
    sla_observacoes: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("sla_observacoes"))

    contrato_resumo: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("contrato_resumo"))
    prioridade: Optional[PrioridadeServico] = Field(None, description=DESCRICOES_SERVICO.get("prioridade"))

    periodicidade_revisao: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("periodicidade_revisao"))
    data_ultima_revisao: Optional[date] = Field(None, description=DESCRICOES_SERVICO.get("data_ultima_revisao"))
    autor_ultima_revisao: Optional[str] = Field(None, description=DESCRICOES_SERVICO.get("autor_ultima_revisao"))
    data_proxima_revisao: Optional[date] = Field(None, description=DESCRICOES_SERVICO.get("data_proxima_revisao"))

    model_config = ConfigDict(use_enum_values=True)


class ServicoResponse(ServicoVinculo):
    element_id: str = Field(..., description=DESCRICOES_SERVICO.get("element_id"))
    criado_em: Optional[datetime] = Field(None, description=DESCRICOES_SERVICO.get("criado_em"))
    atualizado_em: Optional[datetime] = Field(None, description=DESCRICOES_SERVICO.get("atualizado_em"))
    model_config = ConfigDict(use_enum_values=True)