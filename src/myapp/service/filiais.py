import json
from src.myapp.schemas.FilialSchema import FilialSchema
from src.myapp.utils import conexaoFirebirdJSON, getFiliaisJSON
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.myapp.models.Usuario import Usuario

def getFiliaisPermitidas(idUsuario: int, secao: Session) -> list:
    usuario = secao.scalar(select(Usuario).where(Usuario.id == idUsuario))

    if usuario is None:
        return None

    return usuario.filiais

def readFiliais(idUsuario: int, secao: Session):

    filiaisDisponiveis = getFiliaisJSON()

    filiaisPermitidas = getFiliaisPermitidas(idUsuario, secao)
 
    return list(filter(lambda x : x.nomeFilial in filiaisPermitidas, filiaisDisponiveis))


def updateValorTeto(nome_filial, novo_valor):
    with open(conexaoFirebirdJSON, "r", encoding='utf-8') as json_read:
        conexoes = json.load(json_read)

        for con in conexoes:
            if con["nome"].capitalize() == nome_filial.capitalize():
                con["limite"] = novo_valor 
                break
        
        with open(conexaoFirebirdJSON, "w", encoding='utf-8') as json_write:
            json.dump(conexoes, json_write, ensure_ascii=False, indent=4)