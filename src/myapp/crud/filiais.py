import json
from ..schemas.FilialSchema import FilialSchema

json_caminho = 'config\conexao.json'

def readFiliais():
    with open(json_caminho, "r", encoding='utf-8') as arq_json:
        conexoes = json.load(arq_json)

        return [FilialSchema(nomeFilial=con["nome"], valorTeto=con["limite"]) for con in conexoes if con['status']]


def updateValorTeto(nome_filial, novo_valor):
    with open(json_caminho, "r", encoding='utf-8') as json_read:
        conexoes = json.load(json_read)

        for con in conexoes:
            if con["nome"].capitalize() == nome_filial.capitalize():
                con["limite"] = novo_valor 
                break
        
        with open(json_caminho, "w", encoding='utf-8') as json_write:
            json.dump(conexoes, json_write, ensure_ascii=False, indent=4)