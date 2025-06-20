from pydantic import BaseModel
from typing import List

class UsuarioSchema(BaseModel):
    cpf: str
    senha: str
    nomeCompleto: str
    nomeUsuario: str
    filiaisPermitidas: List[str]

class UsuarioDB(UsuarioSchema):
    id: int
    