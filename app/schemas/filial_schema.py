from pydantic import BaseModel

class AtualizarTetoSchema(BaseModel):
    nomeFilial: str
    valorTeto: float