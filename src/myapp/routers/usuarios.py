from fastapi import APIRouter, status, HTTPException
from ..schemas.UsuarioSchema import UsuarioSchemaDB

from myapp.db.database import engine_sqlAlchemy
from sqlalchemy import select, or_
from sqlalchemy.orm import sessionmaker
from src.myapp.models.Usuario import Usuario
from src.myapp.security import get_password_hash
from src.myapp.crud.usuarios import readUsuarios


from http import HTTPStatus

usuarios_router = APIRouter(prefix='/users')

@usuarios_router.post("/", status_code= status.HTTP_201_CREATED)
async def create_user(cadastro: UsuarioSchemaDB):
    engine = engine_sqlAlchemy
    Session = sessionmaker(bind=engine)
    secao = Session()

    statement = select(Usuario).where( or_(
        Usuario.nomeUsuario == cadastro.nomeUsuario,
        Usuario.cpf == cadastro.cpf)
    )

    db_usuario = secao.scalar(statement)

    if db_usuario:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Nome de usuário ou CPF já cadastrado")
    
    hash_senha = get_password_hash(cadastro.senha)

    db_usuario = Usuario(nome= cadastro.nomeCompleto ,nomeUsuario= cadastro.nomeUsuario, 
                         cpf= cadastro.cpf , senha= hash_senha, filiais= cadastro.filiaisPermitidas)
    secao.add(db_usuario)
    secao.commit()
    secao.refresh(db_usuario)
    return db_usuario

@usuarios_router.get("/", status_code=HTTPStatus.OK)
async def get_users():
    return readUsuarios()