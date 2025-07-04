from sqlalchemy.orm import Session
from sqlalchemy import update, select, or_
from src.myapp.models.Usuario import Usuario
from src.myapp.schemas.UsuarioSchema import UsuarioSchemaPublic, UsuarioSchema, UsuarioAutenticadoSchema, UsuarioAtualizacaoSchema
from fastapi import HTTPException
from http import HTTPStatus
from src.myapp.security import get_password_hash, verify_password, create_access_token
from src.myapp.utils import selecionaFiliaisPermitidas, buscaUsuarioPorID

def readUsuarios(secao: Session):
    usuarios = secao.scalars(select(Usuario)).all()
    
    users_schema = [UsuarioSchemaPublic(id=user.id,
                                        cpf=user.cpf,
                                        nomeCompleto=user.nome,
                                        nomeUsuario=user.nomeUsuario,
                                        filiaisPermitidas=user.filiais,
                                        status=user.status) for user in usuarios]

    return users_schema

def createUsuario(cadastro: UsuarioSchema, secao : Session):

    statement = select(Usuario).where( or_(
        Usuario.cpf == cadastro.cpf)
    )

    db_usuario = secao.scalar(statement)

    if db_usuario:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="CPF já cadastrado")
    
    filiaisProcessadas = selecionaFiliaisPermitidas(cadastro.filiaisPermitidas)

    #Padrão 3 primeiros dígitos do cpf para senha.
    hash_senha = get_password_hash(cadastro.cpf[:3])

    db_usuario = Usuario(nome= cadastro.nomeCompleto ,nomeUsuario= cadastro.nomeUsuario, 
                         cpf= cadastro.cpf , senha= hash_senha, filiais= filiaisProcessadas)
    secao.add(db_usuario)
    secao.commit()
    secao.refresh(db_usuario)

def autenticacao(cpf: str, senha: str, session: Session):
    user = session.scalar(select(Usuario).where(Usuario.cpf == cpf))

    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="CPF ou senha inválidos")

    if not verify_password(senha, user.senha):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="CPF ou senha inválidos")
    
    data = {
        "username": cpf,
        "id": user.id
    }

    token = create_access_token(data)

    return UsuarioAutenticadoSchema(cpf= cpf,
                               nomeCompleto=user.nome,
                               nomeUsuario=user.nomeUsuario,
                               filiaisPermitidas=user.filiais,
                               access_token=token, 
                               token_type="Bearer")

def atualizarUsuario(dados: UsuarioAtualizacaoSchema, secao: Session) -> Usuario | None:
    usuario = buscaUsuarioPorID(dados.id, secao)

    if not usuario:
        return None

    if dados.cpf is not None:
        usuario.cpf = dados.cpf

    if dados.nomeCompleto is not None:
        usuario.nome = dados.nomeCompleto

    if dados.nomeUsuario is not None:
        usuario.nomeUsuario = dados.nomeUsuario

    if dados.filiaisPermitidas is not None:
        usuario.filiais =  selecionaFiliaisPermitidas(dados.filiaisPermitidas)


    secao.commit()
    
    secao.refresh(usuario)
    
    return UsuarioSchemaPublic(id=usuario.id, cpf=usuario.cpf, nomeCompleto=usuario.nome,
                               status=usuario.status, filiaisPermitidas=usuario.filiais, 
                               nomeUsuario=usuario.nomeUsuario)
    