from pydantic import BaseModel

class AtualizarTetoRequest(BaseModel):
    filial : str
    novo_valor : float