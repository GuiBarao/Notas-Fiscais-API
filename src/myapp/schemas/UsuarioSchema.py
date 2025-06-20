from pydantic import BaseModel, field_validator
from typing import List
from src.myapp.models.Usuario import Status


class UsuarioSchema(BaseModel):
    cpf: str
    nomeCompleto: str
    nomeUsuario: str
    filiaisPermitidas: List[str]

class UsuarioSchemaPublic(UsuarioSchema):
    id:int
    status: bool

    @field_validator("status", mode = "before")
    def status_bool(cls, v):
        return v == Status.ATIVO
    
class UsuarioAutenticadoSchema(UsuarioSchema):
    access_token : str
    token_type: str