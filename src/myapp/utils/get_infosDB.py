import json
from ..schemas.ConexaoSchema import ConexaoSchema
<<<<<<< HEAD
json_caminho = "src\myapp\config\conexao.json"
=======
json_caminho = "config\conexao.json"
>>>>>>> 244a3b9a9e4c6d95bed5108f9cabb2c1d1969be0

def get_infosDB(filial:str) -> ConexaoSchema:
    with open(json_caminho, "r", encoding='utf-8') as json_read:
        conexoes = json.load(json_read)

        for con in conexoes:
            if con["nome"].capitalize() == filial.capitalize():
                return ConexaoSchema(database=con["db_database"], user=con["db_user"],
                                      password=con["db_password"], host=con["host"], port=str(con["port"])) 
        
        raise ValueError(f"Filial {filial} não encontrada.")
