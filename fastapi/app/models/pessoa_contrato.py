from enum import Enum
from app.models.vinculo import Vinculo
from app.models.contrato import ContratoBase
from app.models.pessoa import PessoaBase


class VinculoPessoaContrato(str, Enum):
    FISCALIZA = "FISCALIZA"
    SUPLENTE_FISCAL = "SUPLENTE_FISCAL"
    GESTOR_CONTRATO = "GESTOR_CONTRATO"


class PessoaContrato(Vinculo):
    descricao_vinculo: VinculoPessoaContrato
    no: ContratoBase


class ContratoPessoa(Vinculo):
    descricao_vinculo: VinculoPessoaContrato
    no: PessoaBase
