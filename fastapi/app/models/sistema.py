from pydantic import BaseModel, Field
from typing import Optional

DESCRICOES_SISTEMA = {
    "nome" : "Nome do sistema. Por exemplo: Sistema de Gerenciamento de Zeladoria",
    "sigla" : "Sigla do sistema. Por exemplo: SGZ"
}

class SistemaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150, description=DESCRICOES_SISTEMA.get("nome"))
    sigla : str = Field(..., min_length=3, max_length=50, description=DESCRICOES_SISTEMA.get("sigla"))


class SistemaCreate(SistemaBase):
    pass


class SistemaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=150, description=DESCRICOES_SISTEMA.get("nome"))
    sigla: Optional[str] = Field(None, min_length=3, max_length=50, description=DESCRICOES_SISTEMA.get("sigla"))


class SistemaResponse(SistemaBase):
    element_id: str