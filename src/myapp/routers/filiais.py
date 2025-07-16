from fastapi import APIRouter, status, Query, Depends
from src.myapp.service.filiais import readFiliais, updateValorTeto
from src.myapp.service.notas import readNotas
from src.myapp.schemas.FilialSchema import FilialSchema
from src.myapp.schemas.NotasRequestSchema import NotasRequestSchema
from src.myapp.db.database import database_session
from src.myapp.service.filiais import get_infosDB
from src.myapp.security import auth_validation, getPayload
from sqlalchemy.orm import Session
from src.myapp.db.database import get_session
from typing import List, Annotated
import asyncio

filiais_router = APIRouter(prefix="/filiais")

@filiais_router.get("/", response_model= List[FilialSchema], status_code= status.HTTP_200_OK)
async def filiais(token: str = Depends(auth_validation), 
                  secao: Session = Depends(get_session)):
    await asyncio.sleep(5)
    payload = getPayload(token)
    loggedUserID = payload["id"]
    return readFiliais(loggedUserID, secao)

@filiais_router.put('/valor_teto')
async def mudar_valor_teto(request : FilialSchema, _: str = Depends(auth_validation)):

    updateValorTeto(request.nomeFilial, request.valorTeto)
    return status.HTTP_201_CREATED

@filiais_router.get("/notas")
async def notas_filial(request: Annotated[NotasRequestSchema, Query()], _: str = Depends(auth_validation)):
    with database_session(get_infosDB(request.nomeFilial)) as con:
        return readNotas(con, dataInicial = request.dataInicial, dataFinal=request.dataFinal)
    
        


