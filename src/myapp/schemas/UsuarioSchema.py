from pydantic import BaseModel, field_validator, BeforeValidator
from typing import List, Annotated
from src.myapp.models.Usuario import Status

def isEmpty(value: str) -> str:
    if not value or not value.strip():
        raise ValueError("Campo obrigatório")
    
    return value



class UsuarioSchema(BaseModel):
    cpf: Annotated[str, BeforeValidator(isEmpty)]
    nomeCompleto: Annotated[str, BeforeValidator(isEmpty)]
    nomeUsuario: Annotated[str, BeforeValidator(isEmpty)]
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