import json
from models.Filial import Filial

json_conexao = 'conexao.json'
def ler_json():
    with open(json_conexao, "r", encoding='utf-8') as con_json:
        return json.load(con_json)
    
def salvar_json(conteudo):
    with open(json_conexao, "w", encoding='utf-8') as con_json:
        json.dump(conteudo, con_json, indent=4, ensure_ascii=False)

def filiais_disponiveis():
    conexoes = ler_json()
    return [con['nome'] for con in conexoes if con['status']]

def alterar_valor_teto(filial: str, novo_valor: float):
    conexoes = ler_json()
    for con in conexoes:
        if str(con['nome']).capitalize() == filial.capitalize():
            con['limite'] = novo_valor
            break

    salvar_json(conexoes)


def nfse_filial(filial):
    conexoes = ler_json()
    for con in conexoes:
        if str(con['nome']).capitalize() == filial.capitalize():
            filial = Filial(con)
            resultado = filial.buscar_notas()
            return {"filial": filial.nome.capitalize(), "valor_teto" : str(filial.valor_teto),  "nota" : format_nota_response(resultado)}
            
 
def format_nota_response(result_query:list):
    labels = ["numero", "cpf", "titular", "data", "valor", "status", "erro"]
    resultado_format = []
    for view in result_query:

        dict_view = {}
        for i in range(len(labels)):

            chave = labels[i]
            valor = view[i]

            if(chave == "status"):
                dict_view[chave] = valor
            elif(chave == "erro" and not dict_view['status']):
                dict_view[chave] = {"mensagem" : view[i].decode('utf-8'), "erro": view[i+1].decode('utf-8')}
            else:
                dict_view[chave] = str(valor)


        if(dict_view['status']):
            dict_view.pop('erro')
            
        resultado_format.append(dict_view)

    return resultado_format
    



