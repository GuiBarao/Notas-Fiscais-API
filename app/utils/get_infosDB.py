import json
from app.schemas.conexao_schema import ConexaoSchema
json_caminho = "conexao.json"

def get_infosDB(filial:str) -> ConexaoSchema:
    with open(json_caminho, "r", encoding='utf-8') as json_read:
        conexoes = json.load(json_read)

        for con in conexoes:
            if con["nome"].capitalize() == filial.capitalize():
                return ConexaoSchema(database=con["db_database"], user=con["db_user"],
                                      password=con["db_password"], host=con["host"], port=str(con["port"])) 
        
        raise ValueError(f"Filial '{filial}' não encontrada.")
