from enum import Enum
from app.models.vinculo import Vinculo
from app.models.servico import ServicoBase
from app.models.contrato import ContratoBase

class VinculoContratoServico(str, Enum):
    FORNECE = "FORNECE",
    FORNECIDO = "FORNECIDO"

class ContratoServico(Vinculo):
    descricao_vinculo: VinculoContratoServico
    no: ServicoBase

class ServicoContrato(Vinculo):
    descricao_vinculo: VinculoContratoServico
    no: ContratoBase