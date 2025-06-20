from contextlib import contextmanager
from firebird.driver import connect
from firebird.driver import driver_config
from myapp.schemas.ConexaoSchema import ConexaoSchema
from myapp.config.settings import driver, user, password, port, host, database
from sqlalchemy import create_engine


@contextmanager
def database_session(infos_con : ConexaoSchema):
    conexao_db = None
    try:
        driver_config.server_defaults.host.value = infos_con.host
        driver_config.server_defaults.port.value = infos_con.port
        conexao_db = connect(infos_con.database, user = infos_con.user, password = infos_con.password, charset="UTF8")
        yield conexao_db
    except Exception as e:
        raise Exception("Falha ao conectar no banco de dados.") from e
    finally:
        if conexao_db:
            conexao_db.close()


def engine_mySQL():
    conexao_str = f"mysql+{driver}://{user}:{password}@{host}:{port}/{database}"

    engine = create_engine(conexao_str)
    return engine
