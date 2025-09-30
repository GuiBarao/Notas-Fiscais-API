import json
from src.myapp.schemas.FilialSchema import FilialSchema
from sqlalchemy.orm import Session
from typing import List
from src.myapp.schemas.ConexaoSchema import ConexaoSchema
from pathlib import Path
from fastapi import HTTPException, status

#Pega o caminho pro json de conexões firebird
raizProjeto = Path(__file__).resolve().parent.parent
PATH_JSON_CONEXOES_FIREBIRD = raizProjeto / "config" / "conexao.json"

def get_infosDB(filial:str) -> ConexaoSchema:
    with open(PATH_JSON_CONEXOES_FIREBIRD, "r", encoding='utf-8') as json_read:
        conexoes = json.load(json_read)

        for con in conexoes:
            if con["nome"].capitalize() == filial.capitalize():
                return ConexaoSchema(database=con["db_database"], user=con["db_user"],
                                      password=con["db_password"], host=con["db_host"], port=str(con["db_port"])) 
        
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Filial {filial} não encontrada.")


def filiaisJsonToSchema() -> List[FilialSchema]:

    with open(PATH_JSON_CONEXOES_FIREBIRD, "r", encoding='utf-8') as arq_json:
        conexoes = json.load(arq_json)
        
    return [FilialSchema(nomeFilial=con["nome"], valorTeto=con["limite"], filialPermitida=con["nome"]) 
            for con in conexoes 
            if con['status']]


def readFiliais() -> List[FilialSchema]:

    filiaisDisponiveis = filiaisJsonToSchema()

    return filiaisDisponiveis


def updateValorTeto(nome_filial, novo_valor):
    with open(PATH_JSON_CONEXOES_FIREBIRD, "r", encoding='utf-8') as json_read:
        conexoes = json.load(json_read)

        for con in conexoes:
            if con["nome"].capitalize() == nome_filial.capitalize():
                con["limite"] = novo_valor 
                break
        
        with open(PATH_JSON_CONEXOES_FIREBIRD, "w", encoding='utf-8') as json_write:
            json.dump(conexoes, json_write, ensure_ascii=False, indent=4)