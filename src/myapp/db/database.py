from contextlib import contextmanager
from firebird.driver import connect
from firebird.driver import driver_config
from myapp.schemas.ConexaoSchema import ConexaoSchema
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from fastapi import HTTPException, status


@contextmanager
def database_session(infos_con : ConexaoSchema):
    conexao_db = None
    
    try:
        driver_config.server_defaults.host.value = infos_con.host
        driver_config.server_defaults.port.value = infos_con.port
        conexao_db = connect(infos_con.database, user = infos_con.user, password = infos_con.password, charset="ISO8859_1")
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
    try:
        Session = sessionmaker(bind=engine_sqlAlchemy)
        return Session()
    except Exception as e:
        raise Exception("Erro ao conectar com o banco de dados.")

class Base (DeclarativeBase):
    pass
