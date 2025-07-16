from pydantic import BaseModel, model_validator, field_validator
from typing import Optional
from datetime import date

class Cliente(BaseModel):
    cpf_cnpj: str
    nome: str

class Erro(BaseModel):
    mensagem: Optional[str] = None
    log: Optional[str] = None

class Nota(BaseModel):
    
    id: int
    data_cadastro: date
    valor: float
    status: bool
    erro: Optional[Erro] = None
    cliente: Cliente

    #Se status for true, a nota não tem erro
    @model_validator(mode='after')
    def valida_erro(self):
        if(self.status):
            self.erro = None
        return self
    
    #Status retorna '0' ou '1' do banco. '0' para false e '1' pra true
    @field_validator("status", mode = "before")
    def status_to_bool(cls, v):
        return v == '1'
