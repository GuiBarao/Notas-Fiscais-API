from fastapi import APIRouter, status, Depends
<<<<<<< HEAD
from src.myapp.schemas.UsuarioSchema import UsuarioSchema, UsuarioAutenticadoSchema
=======
from src.myapp.schemas.UsuarioSchema import UsuarioSchema
from src.myapp.schemas.JWTSchema import JWTSchema
>>>>>>> 244a3b9a9e4c6d95bed5108f9cabb2c1d1969be0
from src.myapp.service.usuarios import readUsuarios, createUsuario, autenticacao
from http import HTTPStatus
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.myapp.db.database import get_session

usuarios_router = APIRouter(prefix='/users')

@usuarios_router.post("/", status_code= status.HTTP_201_CREATED)
async def cadastro (dadosCadastro: UsuarioSchema, secao: Session = Depends(get_session)):

    createUsuario(dadosCadastro, secao)

    return dadosCadastro

@usuarios_router.get("/", status_code=HTTPStatus.OK)
async def get_users(secao: Session = Depends(get_session)):
    return readUsuarios(secao)

<<<<<<< HEAD
@usuarios_router.post("/token", status_code=status.HTTP_202_ACCEPTED, response_model = UsuarioAutenticadoSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), secao: Session = Depends(get_session)):
    
    return autenticacao(cpf=form_data.username, senha=form_data.password, session=secao)
=======
@usuarios_router.post("/token", status_code=status.HTTP_202_ACCEPTED, response_model = JWTSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), secao: Session = Depends(get_session)):
    
    return autenticacao(cpf=form_data.username, senha=form_data.password, secao=secao)
>>>>>>> 244a3b9a9e4c6d95bed5108f9cabb2c1d1969be0
