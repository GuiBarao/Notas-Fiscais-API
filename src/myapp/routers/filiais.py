from fastapi import APIRouter, status, Header, HTTPException, Depends
from src.myapp.service.filiais import readFiliais, updateValorTeto
from src.myapp.service.notas import readNotas
from src.myapp.schemas.FilialSchema import FilialSchema
from src.myapp.db.database import database_session
from src.myapp.utils import get_infosDB
from src.myapp.security import auth_validation, getPayload
from sqlalchemy.orm import Session
from src.myapp.db.database import get_session

filiais_router = APIRouter(prefix="/filiais")

@filiais_router.get("/")
async def filiais(token: str = Depends(auth_validation), secao: Session = Depends(get_session)):
    payload = getPayload(token)
    loggedUserID = payload["id"]
    return readFiliais(loggedUserID, secao)

@filiais_router.put('/valor_teto')
async def mudar_valor_teto(request : FilialSchema, _: str = Depends(auth_validation)):

    updateValorTeto(request.nomeFilial, request.valorTeto)
    return status.HTTP_201_CREATED

@filiais_router.get("/{filial}/notas")
async def notas_filial(filial:str, _: str = Depends(auth_validation)):
    
    with database_session(get_infosDB(filial)) as con:
        return readNotas(con)
    
        


