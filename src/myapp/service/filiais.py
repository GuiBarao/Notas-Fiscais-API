import json
from src.myapp.schemas.FilialSchema import FilialSchema
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.myapp.models.Usuario import Usuario
from typing import List
from src.myapp.schemas.ConexaoSchema import ConexaoSchema
import os
from dotenv import load_dotenv

load_dotenv()
conexaoFirebirdJSON = os.getenv("PATH_JSON_CONEXOES_FIREBIRD")
    

def get_infosDB(filial:str) -> ConexaoSchema:
    with open(conexaoFirebirdJSON, "r", encoding='utf-8') as json_read:
        conexoes = json.load(json_read)

        for con in conexoes:
            if con["nome"].capitalize() == filial.capitalize():
                return ConexaoSchema(database=con["db_database"], user=con["db_user"],
                                      password=con["db_password"], host=con["host"], port=str(con["port"])) 
        
        raise ValueError(f"Filial {filial} não encontrada.")


def filiaisJsonToSchema(idUsuario, secao) -> List[FilialSchema]:

    filiaisPermitidas = getFiliaisPermitidas(idUsuario, secao)

    with open(conexaoFirebirdJSON, "r", encoding='utf-8') as arq_json:
        conexoes = json.load(arq_json)

    return [FilialSchema(nomeFilial=con["nome"], valorTeto=con["limite"], filialPermitida=con["nome"] in filiaisPermitidas) 
            for con in conexoes 
            if con['status']]


def getFiliaisPermitidas(idUsuario: int, secao: Session) -> list:
    usuario = secao.scalar(select(Usuario).where(Usuario.id == idUsuario))

    if usuario is None:
        return None

    return usuario.filiais

def readFiliais(idUsuario: int, secao: Session) -> List[FilialSchema]:

    filiaisDisponiveis = filiaisJsonToSchema(idUsuario, secao)

    return filiaisDisponiveis


def updateValorTeto(nome_filial, novo_valor):
    with open(conexaoFirebirdJSON, "r", encoding='utf-8') as json_read:
        conexoes = json.load(json_read)

        for con in conexoes:
            if con["nome"].capitalize() == nome_filial.capitalize():
                con["limite"] = novo_valor 
                break
        
        with open(conexaoFirebirdJSON, "w", encoding='utf-8') as json_write:
            json.dump(conexoes, json_write, ensure_ascii=False, indent=4)