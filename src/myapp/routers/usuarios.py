from fastapi import APIRouter, status, HTTPException, Depends

from src.myapp.schemas.UsuarioSchema import UsuarioSchemaDB
from src.myapp.schemas.JWTSchema import JWTSchema

from myapp.db.database import get_session
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from src.myapp.models.Usuario import Usuario
from src.myapp.security import get_password_hash, verify_password, create_access_token
from src.myapp.crud.usuarios import readUsuarios
from http import HTTPStatus
from fastapi.security import OAuth2PasswordRequestForm

usuarios_router = APIRouter(prefix='/users')

@usuarios_router.post("/", status_code= status.HTTP_201_CREATED)
async def create_user (cadastro: UsuarioSchemaDB, session : Session = Depends(get_session)):

    secao = get_session()

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

@usuarios_router.post("/token", status_code=status.HTTP_202_ACCEPTED, response_model = JWTSchema)
async def login(    form_data: OAuth2PasswordRequestForm = Depends(),
                    session: Session = Depends(get_session)):
    
    user = session.scalar(select(Usuario).where(Usuario.cpf == form_data.username))

    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="CPF ou senha inválidos")

    if not verify_password(form_data.password, user.senha):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="CPF ou senha inválidos")
    
    data = {
        "username": form_data.username
    }

    token = create_access_token(data)

    return JWTSchema(access_token=token, token_type="Bearer")