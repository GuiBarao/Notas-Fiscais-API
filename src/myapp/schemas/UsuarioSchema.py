from pydantic import BaseModel, field_validator, BeforeValidator
from typing import List, Annotated, Optional
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

    @field_validator("cpf", mode="before")
    def numerico(cls, v:str):
        if v.isnumeric():
            return v
        raise ValueError("Campo de CPF suporta apenas caracteres numéricos")        


class UsuarioSchemaPublic(UsuarioSchema):
    id:int
    status: bool

    @field_validator("status", mode = "before")
    def status_to_bool(cls, v):
        return v == Status.ATIVO
    
class UsuarioAutenticadoSchema(UsuarioSchema):
    access_token : str
    token_type: str

class UsuarioAtualizacaoSchema(BaseModel):
    id: int
    cpf: Annotated[Optional[str], BeforeValidator(isEmpty)] = None
    nomeCompleto: Annotated[Optional[str], BeforeValidator(isEmpty)] = None
    nomeUsuario: Annotated[Optional[str], BeforeValidator(isEmpty)] = None
    senha: Annotated[Optional[str], BeforeValidator(isEmpty)] = None
    filiaisPermitidas: Optional[List[str]] = None
    status: Optional[bool] = None

