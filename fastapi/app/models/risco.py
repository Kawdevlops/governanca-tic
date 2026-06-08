from pydantic import BaseModel, Field
from typing import Optional

class Risco(BaseModel):
    identificador: str
    nome: str = Field(..., min_length=3, max_length=100) 
    categoria: Optional[str] = None
    probabilidade: Optional[str] = None
    impacto: Optional[str] = None
    nivel: Optional[str] = None
    status: Optional[str] = None