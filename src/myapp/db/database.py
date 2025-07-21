from contextlib import contextmanager
from firebird.driver import connect
from firebird.driver import driver_config
from myapp.schemas.ConexaoSchema import ConexaoSchema
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from fastapi import HTTPException, status

def get_caminhoAbsoluto(caminho_relativo: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    projeto_root = os.path.abspath(os.path.join(base_dir, "..", "..", ".."))
    return os.path.join(projeto_root, caminho_relativo)

@contextmanager
def database_session(infos_con : ConexaoSchema):
    conexao_db = None
    caminho_absoluto = get_caminhoAbsoluto(infos_con.database)
    try:
        driver_config.server_defaults.host.value = infos_con.host
        driver_config.server_defaults.port.value = infos_con.port
        conexao_db = connect(caminho_absoluto, user = infos_con.user, password = infos_con.password, charset="ISO8859_1")
        yield conexao_db
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
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
