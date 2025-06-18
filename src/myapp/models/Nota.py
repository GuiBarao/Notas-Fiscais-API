from pydantic import BaseModel, model_validator
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

    @model_validator(mode='after')
    def valida_erro(self):
        if(self.status):
            self.erro = None
        return self
    
        

    
