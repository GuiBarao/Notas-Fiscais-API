from fastapi import APIRouter, status, Depends
from src.myapp.schemas.UsuarioSchema import UsuarioSchema, UsuarioAutenticadoSchema, UsuarioSchemaPublic, UsuarioAtualizacaoSchema
from src.myapp.service.usuarios import readUsuarios, createUsuario, autenticacao, atualizarUsuario
from http import HTTPStatus
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.myapp.db.database import get_session
from src.myapp.security import auth_validation
from typing import List

usuarios_router = APIRouter(prefix='/users')

@usuarios_router.post("/", status_code= status.HTTP_201_CREATED)
async def cadastro (dadosCadastro: UsuarioSchema, secao: Session = Depends(get_session), _: str = Depends(auth_validation)):
    createUsuario(dadosCadastro, secao)
    return dadosCadastro

@usuarios_router.get("/", status_code=HTTPStatus.OK, response_model=List[UsuarioSchemaPublic])
async def get_users(secao: Session = Depends(get_session), _: str = Depends(auth_validation)):
    return readUsuarios(secao)

@usuarios_router.post("/token", status_code=status.HTTP_202_ACCEPTED, response_model = UsuarioAutenticadoSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), secao: Session = Depends(get_session)):
    
    return autenticacao(cpf=form_data.username, senha=form_data.password, session=secao)

@usuarios_router.put("/", status_code=HTTPStatus.OK, response_model=UsuarioSchemaPublic)
async def put_usuarios(request : UsuarioAtualizacaoSchema, 
                       secao: Session = Depends(get_session), 
                       _: str = Depends(auth_validation)):
    
    return atualizarUsuario(request, secao)
