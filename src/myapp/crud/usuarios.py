from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from src.myapp.models.Usuario import Usuario
from src.myapp.schemas.UsuarioSchema import UsuarioSchemaPublic
from src.myapp.db.database import engine_sqlAlchemy

def readUsuarios():
    Session = sessionmaker(bind=engine_sqlAlchemy)
    secao = Session()

    usuarios = secao.scalars(select(Usuario)).all()
    
    users_schema = [UsuarioSchemaPublic(id=user.id,cpf=user.cpf,nomeCompleto=user.nome,nomeUsuario=user.nomeUsuario,filiaisPermitidas=user.filiais) for user in usuarios]
    return users_schema
