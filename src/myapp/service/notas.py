from enum import Enum
from firebird.driver import Connection
from src.myapp.models.Nota import Cliente, Erro, Nota
from src.myapp.db.queries.nfse import get_nfse_cliente
from datetime import date

#Mapeia os indices dos dados na lista que a query "get_nfse_cliente" retorna
class MapaQuery(Enum):
            NOTA_ID = 0     
            DATA = 1
            VALOR = 2
            STATUS =  3
            CPF_CNPJ = 4
            NOME = 5


def readNotas(con: Connection, dataInicial : date, dataFinal: date):

    def instanciaNota(nfse : tuple) -> Nota :

        cliente = Cliente(cpf_cnpj=nfse[MapaQuery.CPF_CNPJ.value], 
                          nome=nfse[MapaQuery.NOME.value])
        
        #erro = Erro(mensagem=nfse[Mapa.MENSAGEM.value], 
        #            log=nfse[Mapa.LOG.value])

        erro = Erro(mensagem="mensagem", 
                    log="log")
                    
        return Nota(id=nfse[MapaQuery.NOTA_ID.value], 
                    data_cadastro=nfse[MapaQuery.DATA.value], 
                    valor=nfse[MapaQuery.VALOR.value], 
                    status=nfse[MapaQuery.STATUS.value],
                    erro=erro,
                    cliente=cliente).model_dump(exclude_none=True)
        
        
    tuplas_bd = get_nfse_cliente(con, dataInicial, dataFinal)
    notas = list(map(instanciaNota, tuplas_bd))

    return notas