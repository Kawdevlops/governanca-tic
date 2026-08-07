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

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date  
from enum import Enum


class CategoriaRisco(str, Enum):
    GOVERNANCA     = "governanca"
    CONTRATO       = "contrato"
    OPERACIONAL    = "operacional"
    SEGURANCA      = "seguranca"
    DADOS          = "dados"
    INFRAESTRUTURA = "infraestrutura"
    SISTEMAS       = "sistemas"
    FINANCEIRO     = "financeiro"

class OrigemRisco(str, Enum):
    PLANEJAMENTO_CONTRATACAO = "planejamento_contratacao"
    SOLUCAO_TIC              = "solucao_tic"
    SELECAO_FORNECEDOR       = "selecao_fornecedor"
    GESTAO_CONTRATUAL        = "gestao_contratual"
    MONITORAMENTO_CONTINUO   = "monitoramento_continuo"


class StatusRisco(str, Enum):
    ABERTO         = "aberto"
    EM_ANALISE     = "em_analise"
    EM_TRATAMENTO  = "em_tratamento"
    MITIGADO       = "mitigado"
    # a NBR ISO 31000 prevê formalmente aceitar um risco quando o custo de mitigar supera o dano esperado.
    # Sem este status, riscos aceitos ficam presos em MITIGADO, o que é semanticamente errado.
    ACEITO         = "aceito"
    ENCERRADO      = "encerrado"


class RiscoBase(BaseModel):
    identificador: str = Field(..., min_length=3, max_length=50)
    nome:          str = Field(..., min_length=3, max_length=180)
    descricao:     Optional[str] = None
    categoria:     CategoriaRisco

    probabilidade: int = Field(..., ge=1, le=5)
    impacto:       int = Field(..., ge=1, le=5)
    criticidade:   int = Field(..., ge=1, le=5)
    exposicao:     int = Field(..., ge=1, le=5)
    prejuizo:      int = Field(..., ge=1, le=5)

    # era Optional[str], agora é o Enum OrigemRisco.
    # Isso permite saber em qual fase do processo o risco surgiu,
    # conforme exige o MGR da IN 1/2019.
    origem:     Optional[OrigemRisco] = None
    responsavel: Optional[str]        = None
    status:      StatusRisco          = StatusRisco.ABERTO

    # acao_preventiva: ação que atua na causa do risco ANTES de ele ocorrer. Campo obrigatório no MGR da IN 1/2019.
    # Exemplo: "Configurar backup automático diário no Neo4j"
    acao_preventiva: Optional[str] = None

    # acao_contingencia: ação executada APÓS o risco ocorrer para minimizar o dano. Também obrigatório no MGR.
    # Exemplo: "Ativar servidor reserva e acionar fornecedor"
    acao_contingencia: Optional[str] = None

    # data em que o risco foi identificado. Essencial para auditoria e para calcular há quanto tempo
    # o risco está aberto sem tratamento.
    data_identificacao: Optional[date] = None

    # data limite para concluir o tratamento do risco.
    # Permite que o Airflow dispare alertas quando o prazo vencer.
    prazo_tratamento: Optional[date] = None

    # justificativa obrigatória quando o status for ACEITO.
    # Sem ela, não há rastreabilidade da decisão de aceitar o risco.
    justificativa_aceite: Optional[str] = None

    def calcular_pontuacao(self) -> int:
        return (
            self.probabilidade * self.impacto
            + self.criticidade
            + self.exposicao
            + self.prejuizo
        )

    def classificar_nivel(self) -> str:
        pontuacao = self.calcular_pontuacao()
        # Pontuação máxima teórica: 5×5 + 5 + 5 + 5 = 40
        # Faixas calibradas para essa escala:
        if pontuacao <= 8:
            return "baixo"      # Ex: P=1, I=2, C=1, E=1, Prej=1 → 5
        if pontuacao <= 18:
            return "moderado"   # Ex: P=2, I=3, C=2, E=2, Prej=2 → 12
        if pontuacao <= 28:
            return "alto"       # Ex: P=3, I=4, C=3, E=3, Prej=3 → 21
        return "critico"        # Ex: P=4, I=5, C=4, E=4, Prej=4 → 32


    def gerar_dados_para_banco(self) -> dict:
        dados = self.model_dump(mode="json")
        dados["pontuacao"] = self.calcular_pontuacao()
        dados["nivel"]     = self.classificar_nivel()
        return dados


class RiscoCreate(RiscoBase):
    pass


class RiscoUpdate(BaseModel):
    nome:      Optional[str]           = None
    descricao: Optional[str]           = None
    categoria: Optional[CategoriaRisco] = None

    probabilidade: Optional[int] = Field(None, ge=1, le=5)
    impacto:       Optional[int] = Field(None, ge=1, le=5)
    criticidade:   Optional[int] = Field(None, ge=1, le=5)
    exposicao:     Optional[int] = Field(None, ge=1, le=5)
    prejuizo:      Optional[int] = Field(None, ge=1, le=5)

    origem:     Optional[OrigemRisco] = None
    responsavel: Optional[str]        = None
    status:      Optional[StatusRisco] = None

    # campos incluídos para permitir atualização via PATCH
    acao_preventiva:      Optional[str]  = None
    acao_contingencia:    Optional[str]  = None
    data_identificacao:   Optional[date] = None
    prazo_tratamento:     Optional[date] = None
    justificativa_aceite: Optional[str]  = None


class RiscoResponse(RiscoBase):
    element_id: str
    pontuacao:  int
    nivel:      str

class RiscoVinculo(BaseModel):
    tipo_alvo:          str  # "servico" | "risco" | "sistema" | "unidade"
    identificador_alvo: str