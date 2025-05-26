from models.Conexao import Conexao

class Filial:
    def __init__(self, conexao_json):
        self.nome = conexao_json['nome']

        self.valor_teto = conexao_json['limite']

        self.conexao = Conexao(conexao_json['db_database'], conexao_json['db_user'], 
                               conexao_json['db_password'], conexao_json['host'], conexao_json['port'])
    
    def __conectar(self):
        self.conexao.conectar()

    def buscar_notas(self):

        self.__conectar()

        query ='''  SELECT nfse_item_id, cpf_cnpj, nome, data_cadastro, 
                    valor, status, mensagem, log 
                    FROM nfse_item, cliente 
                    WHERE nfse_cliente_id = idcliente;'''
        
        resultado = self.conexao.executa_query(query)
    
        self.__fechar_conexao()

        return resultado

    def __fechar_conexao(self):
        self.conexao.fechar_conexao()