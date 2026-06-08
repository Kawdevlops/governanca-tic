from pydantic import BaseModel, Field
from typing import Optional

class Indicador(BaseModel):
    identificador: str
    nome: str = Field(..., min_length=3, max_length=50)
    formula: Optional[str] = None
    unidade_medida: Optional[str] = None
    meta: Optional[str] = None
    periodicidade: Optional[str] = None
    fonte: Optional[str] = None