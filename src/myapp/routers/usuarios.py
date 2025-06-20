from fastapi import APIRouter, status
from ..schemas.UsuarioSchema import UsuarioSchema

from ..db.database import engine_mySQL
from sqlalchemy import select, or_
from sqlalchemy.orm import sessionmaker
from ..models.Usuario import Usuario

from http import HTTPStatus

usuarios_router = APIRouter(prefix='/users')

@usuarios_router.post("/", status_code= status.HTTP_201_CREATED)
async def create_user(cadastro: UsuarioSchema):
    engine = engine_mySQL()
    Session = sessionmaker(bind=engine)
    secao = Session()

    statement = select(Usuario).where( or_(
        Usuario.nomeUsuario == cadastro.nomeUsuario,
        Usuario.cpf == cadastro.cpf)
    )

    db_usuario = secao.scalar(statement)

    if db_usuario:
        return HTTPStatus.CONFLICT
    
    db_usuario = Usuario(nome= cadastro.nomeCompleto ,nomeUsuario= cadastro.nomeUsuario, 
                         cpf= cadastro.cpf , senha= cadastro.senha , filais= cadastro.filiaisPermitidas)
    
    secao.add(db_usuario)
    secao.refresh(db_usuario)
    return db_usuario