from contextlib import contextmanager
from firebird.driver import connect
from firebird.driver import driver_config
from myapp.schemas.ConexaoSchema import ConexaoSchema
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker



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



load_dotenv()
__conexao_str = os.getenv("CONEXAO_DB")
engine_sqlAlchemy = create_engine(__conexao_str)

def get_session():
    Session = sessionmaker(bind=engine_sqlAlchemy)
    return Session()

class Base (DeclarativeBase):
    pass
