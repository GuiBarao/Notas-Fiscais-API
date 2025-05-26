from firebird.driver import connect
from firebird.driver import driver_config

class Conexao:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = str(port)

        self.conexao_db = False

    def conectar(self):

        try:
            driver_config.server_defaults.host.value = self.host
            driver_config.server_defaults.port.value = self.port
            self.conexao_db = connect(self.database, user = self.user, password = self.password, charset="UTF8")
        except Exception as e:
            raise Exception("Falha ao conectar no banco de dados.")

    def executa_query(self, query : str):
        cursor_db = self.conexao_db.cursor()

        try:
            cursor_db.execute(query)
            resultado = cursor_db.fetchall()
            return resultado
        finally:
            cursor_db.close()

    
    def fechar_conexao(self):
        
        self.conexao_db.close()



