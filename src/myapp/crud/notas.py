from enum import Enum
from firebird.driver import Connection
from ..models.Nota import Cliente, Erro, Nota
from ..database.queries.nfse import get_nfse_cliente

json_caminho = 'config\conexao.json'


class Mapa(Enum):
            NOTA_ID = 0     
            DATA = 1
            VALOR = 2
            STATUS =  3
            MENSAGEM =  4
            LOG = 5
            CPF_CNPJ = 6
            NOME = 7



def readNotas(con: Connection):

    def instanciaNota(nfse : tuple) -> Nota :

        cliente = Cliente(cpf_cnpj=nfse[Mapa.CPF_CNPJ.value], 
                          nome=nfse[Mapa.NOME.value])
        
        erro = Erro(mensagem=nfse[Mapa.MENSAGEM.value], 
                    log=nfse[Mapa.LOG.value])

        return Nota(id=nfse[Mapa.NOTA_ID.value], 
                    data_cadastro=nfse[Mapa.DATA.value], 
                    valor=nfse[Mapa.VALOR.value], 
                    status=nfse[Mapa.STATUS.value], 
                    erro=erro,
                    cliente=cliente).model_dump(exclude_none=True)
        
        
    tuplas_bd = get_nfse_cliente(con)
    notas = list(map(instanciaNota, tuplas_bd))

    return notas