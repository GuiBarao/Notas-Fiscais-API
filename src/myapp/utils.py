from sqlalchemy.orm import Session
from sqlalchemy import select
from src.myapp.models.Usuario import Usuario
import json
from src.myapp.schemas.ConexaoSchema import ConexaoSchema
from src.myapp.schemas.FilialSchema import FilialSchema
from typing import List

conexaoFirebirdJSON = "src\myapp\config\conexao.json"

def selecionaFiliaisPermitidas(filiais: list):
    '''Quando a requisição de cadastro não especificar as filiais, o sistema assume que são todas.'''

    if len(filiais) > 0:
        return filiais
    
    return getFiliaisJSON()



def buscaUsuarioPorID(id: int, secao: Session) -> Usuario | None:
    try:
        return secao.scalar(select(Usuario).where(Usuario.id == id))
    except:
        raise Exception("Usuário não encontado")
    



def get_infosDB(filial:str) -> ConexaoSchema:
    with open(conexaoFirebirdJSON, "r", encoding='utf-8') as json_read:
        conexoes = json.load(json_read)

        for con in conexoes:
            if con["nome"].capitalize() == filial.capitalize():
                return ConexaoSchema(database=con["db_database"], user=con["db_user"],
                                      password=con["db_password"], host=con["host"], port=str(con["port"])) 
        
        raise ValueError(f"Filial {filial} não encontrada.")


def getFiliaisJSON() -> List[FilialSchema]:
    with open(conexaoFirebirdJSON, "r", encoding='utf-8') as arq_json:
        conexoes = json.load(arq_json)

    return [FilialSchema(nomeFilial=con["nome"], valorTeto=con["limite"]) 
            for con in conexoes 
            if con['status']]