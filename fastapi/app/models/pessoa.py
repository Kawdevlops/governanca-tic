# app/models/pessoa.py
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.vinculo import Vinculo

DESCRICOES_PESSOA = {
    "nome" : "Nome completo da pessoa.",
    "email" : "Endereço eletrônico institucional.",
    "telefone_movel" : "Número do telefone móvel com DDD, por exemplo: (11) 9145-5401.",
    "telefone_fixo" : "Número do telefone fixo institucional.",
    "ramal" : "Número do ramal relacionado ao telefone fixo institucional"
}

class PessoaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150, description=DESCRICOES_PESSOA.get("nome"))
    email: EmailStr = Field(..., description=DESCRICOES_PESSOA.get("email"))
    telefone_movel: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("telefone_movel"))
    telefone_fixo: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("telefone_fixo"))
    ramal: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("ramal"))


class PessoaVinculos(PessoaBase):
    vinculos: list[Vinculo] = Field(default_factory=list)


class PessoaCreate(PessoaBase):
    pass


class PessoaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=150, description=DESCRICOES_PESSOA.get("nome"))
    email: Optional[EmailStr] = Field(None, description=DESCRICOES_PESSOA.get("email"))
    telefone_movel: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("telefone_movel"))
    telefone_fixo: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("telefone_fixo"))
    ramal: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("ramal"))


class PessoaResponse(PessoaVinculos):
    element_id: str