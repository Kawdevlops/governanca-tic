from pydantic import BaseModel, Field, computed_field, model_validator
from app.models.vinculo import Vinculo
from typing import Optional
from datetime import date, datetime


class ContratoBase(BaseModel):
    numero: int = Field(..., gt=0)
    ano: int = Field(..., gt=0, le=datetime.today().year)
    fornecedor: str | None = None
    vigencia_inicio: date | None = None
    vigencia_fim: date | None = None
    valor_anual_estimado: float | None = None
    processo_sei: str | None = None

    @model_validator(mode="after")
    def validar_vigencia(self):
        if self.vigencia_inicio and self.vigencia_fim:
            if self.vigencia_fim < self.vigencia_inicio:
                raise ValueError("vigencia_fim não pode ser anterior a vigencia_inicio")
        return self


class ContratoVinculo(ContratoBase):
    vinculos: list[Vinculo] = Field(default_factory=list)


class ContratoCreate(ContratoBase):
    pass


class ContratoUpdate(BaseModel):
    numero: Optional[int] = Field(default=None, gt=0)
    ano: Optional[int] = Field(default=None, gt=0, le=date.today().year)
    fornecedor: Optional[str] = None
    vigencia_inicio: Optional[date] = None
    vigencia_fim: Optional[date] = None
    valor_anual_estimado: Optional[float] = Field(default=None, ge=0)
    processo_sei: Optional[str] = None


class ContratoResponse(ContratoVinculo):
    element_id: str
    
    @computed_field
    @property
    def numero_ano(self) -> str | None:
        if self.numero and self.ano:
            return f"{self.numero}/{self.ano}"
        return None
    
    model_config = {"from_attributes": True}