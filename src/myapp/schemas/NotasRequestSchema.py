from pydantic import BaseModel
from datetime import date

class NotasRequestSchema(BaseModel):
    dataInicial: date
    dataFinal: date
    nomeFilial: str