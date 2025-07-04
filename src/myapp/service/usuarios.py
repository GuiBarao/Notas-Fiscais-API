from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from src.myapp.models.Usuario import Usuario
from src.myapp.schemas.UsuarioSchema import UsuarioSchemaPublic, UsuarioSchema, UsuarioAutenticadoSchema
from fastapi import HTTPException
from http import HTTPStatus
from src.myapp.security import get_password_hash, verify_password, create_access_token
from src.myapp.service.filiais import readFiliais

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
    
    #Quando a requisição de cadastro não espeicifcas as filiais, o sistema assume que são todas.
    if(len(cadastro.filiaisPermitidas) == 0):
        filiaisDisponiveis = readFiliais()
        cadastro.filiaisPermitidas = [filialSchema.nomeFilial for filialSchema in filiaisDisponiveis]

    #Padrão 3 primeiros dígitos do cpf para senha.
    hash_senha = get_password_hash(cadastro.cpf[:3])

    filiaisUpper = [filial.upper() for filial in cadastro.filiaisPermitidas]

    db_usuario = Usuario(nome= cadastro.nomeCompleto ,nomeUsuario= cadastro.nomeUsuario, 
                         cpf= cadastro.cpf , senha= hash_senha, filiais= filiaisUpper)
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
        "username": cpf
    }

    token = create_access_token(data)

    return UsuarioAutenticadoSchema(cpf= cpf,
                               nomeCompleto=user.nome,
                               nomeUsuario=user.nomeUsuario,
                               filiaisPermitidas=user.filiais,
                               access_token=token, 
                               token_type="Bearer")