from pydantic import BaseModel, model_validator
from datetime import date
from fastapi import HTTPException, status

class NotasRequestSchema(BaseModel):
    dataInicial: date
    dataFinal: date
    nomeFilial: str

    @model_validator(mode='after')
    def limiteIntervaloDatas(self):
        diferenca = (self.dataFinal - self.dataInicial).days
        if(diferenca > 31):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="O intervalo de dias entres as datas não devem " \
                                "ser maior do que um mês")
        if(diferenca < 0):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="A data final não deve ser anterior à data inicial")
        
        return self
