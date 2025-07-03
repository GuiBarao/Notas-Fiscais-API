from fastapi import APIRouter, status, Header, HTTPException, Depends
from src.myapp.service.filiais import readFiliais, updateValorTeto
from src.myapp.service.notas import readNotas
from src.myapp.schemas.FilialSchema import FilialSchema
from src.myapp.db.database import database_session
from src.myapp.utils.get_infosDB import get_infosDB
from src.myapp.security import auth_validation


filiais_router = APIRouter(prefix="/filiais")

@filiais_router.get("/")
async def filiais(_: str = Depends(auth_validation)):
    return readFiliais()

@filiais_router.put('/valor_teto')
async def mudar_valor_teto(request : FilialSchema, _: str = Depends(auth_validation)):

    updateValorTeto(request.nomeFilial, request.valorTeto)
    return status.HTTP_201_CREATED

@filiais_router.get("/{filial}/notas")
async def notas_filial(filial:str, _: str = Depends(auth_validation)):
    
    with database_session(get_infosDB(filial)) as con:
        return readNotas(con)
    
        


