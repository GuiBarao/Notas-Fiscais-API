from sqlalchemy.orm import Session
from sqlalchemy import update, select, and_
from src.myapp.models.Usuario import Usuario
from src.myapp.schemas.UsuarioSchema import UsuarioSchemaPublic, UsuarioSchema, UsuarioAutenticadoSchema, UsuarioAtualizacaoSchema
from fastapi import HTTPException
from http import HTTPStatus
from src.myapp.security import get_password_hash, verify_password, create_access_token
from src.myapp.service.filiais import filiaisJsonToSchema
from src.myapp.models.Usuario import Status

def buscaUsuarioPorID(id: int, secao: Session) -> Usuario | None:
    try:
        return secao.scalar(select(Usuario).where(Usuario.id == id))
    except:
        raise Exception("Usuário não encontado")


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
    statement = select(Usuario).where(
        Usuario.cpf == cadastro.cpf
    )

    db_usuario = secao.scalar(statement)

    if db_usuario:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="CPF já cadastrado")

    #Se nenhuma filial for passada no cadastro, o sistema assume que deve permitir todas
    if len(cadastro.filiaisPermitidas) == 0:
        filiaisDisponiveis = filiaisJsonToSchema(secao)
        cadastro.filiaisPermitidas = [filial.nomeFilial for filial in filiaisDisponiveis]
    

    #Padrão 3 primeiros dígitos do cpf para senha.
    hash_senha = get_password_hash(cadastro.cpf[:3])

    db_usuario = Usuario(nome= cadastro.nomeCompleto ,nomeUsuario= cadastro.nomeUsuario, 
                         cpf= cadastro.cpf , senha= hash_senha, filiais= cadastro.filiaisPermitidas)
    secao.add(db_usuario)
    secao.commit()
    secao.refresh(db_usuario)

def autenticacao(cpf: str, senha: str, session: Session):
    user = session.scalar(select(Usuario).where(Usuario.cpf == cpf))
    
    if not user or not verify_password(senha, user.senha) or user.status == Status.INATIVO:
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
        statement = select(Usuario).where(and_(Usuario.cpf == dados.cpf, Usuario.id != dados.id))
        if secao.scalar(statement):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="CPF já cadastrado")

        usuario.cpf = dados.cpf

    if dados.nomeCompleto is not None:
        usuario.nome = dados.nomeCompleto

    if dados.nomeUsuario is not None:
        usuario.nomeUsuario = dados.nomeUsuario

    if dados.senha is not None:
        hash_senha = get_password_hash(dados.senha)
        usuario.senha = hash_senha

    if dados.filiaisPermitidas is not None:
        if len(dados.filiaisPermitidas) == 0:   
            filiaisDisponiveis = filiaisJsonToSchema(secao, dados.id)
            usuario.filiais = [filial.nomeFilial for filial in filiaisDisponiveis]
        else:
            usuario.filiais = dados.filiaisPermitidas

    if dados.status is not None:

        usuario.status = Status.ATIVO if dados.status else Status.INATIVO


    secao.commit()
    
    secao.refresh(usuario)
    
    return UsuarioSchemaPublic(id=usuario.id, cpf=usuario.cpf, nomeCompleto=usuario.nome,
                               status=usuario.status, filiaisPermitidas=usuario.filiais, 
                               nomeUsuario=usuario.nomeUsuario)
    