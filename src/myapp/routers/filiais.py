from fastapi import APIRouter, status
from ..crud.filiais import readFiliais, updateValorTeto
from ..crud.notas import readNotas
from ..schemas.FilialSchema import FilialSchema
from ..db.database import database_session
from ..utils.get_infosDB import get_infosDB

filiais_router = APIRouter(prefix="/filiais")

@filiais_router.get("/")
async def filiais():
    return readFiliais()
        

@filiais_router.put('/valor_teto')
async def mudar_valor_teto(request : FilialSchema):
    updateValorTeto(request.nomeFilial, request.valorTeto)
    return status.HTTP_201_CREATED

@filiais_router.get("/{filial}/notas")
async def notas_filial(filial:str):
    
    with database_session(get_infosDB(filial)) as con:
        return readNotas(con)
    
        


