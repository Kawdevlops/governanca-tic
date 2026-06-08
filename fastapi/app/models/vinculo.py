from enum import Enum
from pydantic import BaseModel, SerializeAsAny

class Vinculo(BaseModel):
    descricao_vinculo: Enum
    no: SerializeAsAny[BaseModel]

    def obter_vinculo(self):
        return self.descricao_vinculo
    