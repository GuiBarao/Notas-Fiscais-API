from app.services.filialService import getFiliais, setValorTeto, getNotas
from app.schemas.filial_schema import AtualizarTetoSchema
from database import database_session
from fastapi import APIRouter, status
from app.utils.get_infosDB import get_infosDB

filiais_router = APIRouter(prefix="/filiais")

@filiais_router.get("/")
async def filiais():
    return getFiliais()
        

@filiais_router.put('/valor_teto')
async def mudar_valor_teto(request : AtualizarTetoSchema):
    setValorTeto(request.nomeFilial, request.valorTeto)
    return status.HTTP_201_CREATED

@filiais_router.get("/{filial}/notas")
async def notas_filial(filial:str):
    
    with database_session(get_infosDB(filial)) as con:
        return getNotas(con)
    
        


