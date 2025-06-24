from pydantic import BaseModel
from typing import List


class UsuarioSchema(BaseModel):
    cpf: str
    nomeCompleto: str
    nomeUsuario: str
    filiaisPermitidas: List[str]

class UsuarioSchemaPublic(UsuarioSchema):
    id:int