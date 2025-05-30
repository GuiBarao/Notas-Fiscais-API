import json
from firebird.driver import Connection
from app.clients.database.consultas import get_nfse_cliente
from app.schemas.filial_schema import FilialSchema
from app.models.Nota import Cliente, Erro, Nota
from enum import Enum


json_caminho = 'conexao.json'

def getFiliais():
    with open(json_caminho, "r", encoding='utf-8') as arq_json:
        conexoes = json.load(arq_json)
        return [FilialSchema(nomeFilial=con["nome"], valorTeto=con["limite"]) for con in conexoes if con['status']]
    

def setValorTeto(nome_filial, novo_valor):
    with open(json_caminho, "r", encoding='utf-8') as json_read:
        conexoes = json.load(json_read)

        for con in conexoes:
            if con["nome"].capitalize() == nome_filial.capitalize():
                con["limite"] = novo_valor 
                break
        
        with open(json_caminho, "w", encoding='utf-8') as json_write:
            json.dump(conexoes, json_write, ensure_ascii=False, indent=4)


class Mapa(Enum):
            NOTA_ID = 0     
            DATA = 1
            VALOR = 2
            STATUS =  3
            MENSAGEM =  4
            LOG = 5
            CPF_CNPJ = 6
            NOME = 7



def getNotas(con: Connection):

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