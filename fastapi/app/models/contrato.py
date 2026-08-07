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