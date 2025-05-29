from contextlib import contextmanager
from firebird.driver import connect
from firebird.driver import driver_config


@contextmanager
def database_session(database:str, user:str, password:str, host:str, port:str):
    conexao_db = None
    try:
        try:
            driver_config.server_defaults.host.value = host
            driver_config.server_defaults.port.value = port
            conexao_db = connect(database, user = user, password = password, charset="UTF8")
            yield conexao_db
        except Exception as e:
            raise Exception("Falha ao conectar no banco de dados.") from e
    finally:
        if conexao_db:
            conexao_db.close()
