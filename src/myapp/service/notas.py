from enum import Enum
from firebird.driver import Connection
from src.myapp.models.Nota import Cliente, Erro, Nota
from src.myapp.db.queries.nfse import get_nfse_cliente
from datetime import date
from sqlalchemy.orm import Session
from src.myapp.service.usuarios import buscaUsuarioPorID
from fastapi import HTTPException, status

#Mapeia os indices dos dados na lista que a query "get_nfse_cliente" retorna
class MapaQuery(Enum):
            NOTA_ID = 0     
            DATA = 1
            VALOR = 2
            STATUS =  3
            CPF_CNPJ = 4
            NOME = 5

def usuarioPermitido(idUsuario: int, filialRequest: str, secao: Session) -> bool:
    usuario = buscaUsuarioPorID(idUsuario, secao)
    listaFiliaisNormalizada = [filial.lower() for filial in usuario.filiais]

    return filialRequest in listaFiliaisNormalizada
      

def instanciaNota(nfse : tuple) -> Nota :

    cliente = Cliente(cpf_cnpj=nfse[MapaQuery.CPF_CNPJ.value], 
                        nome=nfse[MapaQuery.NOME.value])

    erro = Erro(mensagem="mensagem", 
                log="log")
    
    return Nota(id=nfse[MapaQuery.NOTA_ID.value], 
                data_cadastro=nfse[MapaQuery.DATA.value], 
                valor= nfse[MapaQuery.VALOR.value], 
                status= nfse[MapaQuery.STATUS.value],
                erro=erro,
                cliente=cliente).model_dump(exclude_none=True)

def readNotas(con: Connection, idUsuario: int, dataInicial : date, dataFinal: date, secao: Session, filial: str):

    if not usuarioPermitido(idUsuario, filial, secao):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Filial não autorizada para o usuário")

    tuplas_bd = get_nfse_cliente(con, dataInicial, dataFinal)
    notas = list(map(instanciaNota, tuplas_bd))

    return notas