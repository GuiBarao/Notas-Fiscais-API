from pydantic import BaseModel

class FilialSchema(BaseModel):
    nomeFilial: str
    valorTeto: float
    filialPermitida: bool