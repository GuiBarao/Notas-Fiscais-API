from fastapi import APIRouter, status
from ..schemas.UsuarioSchema import UsuarioSchema

usuarios_router = APIRouter(prefix='/users')

@usuarios_router.post("/", 
                      status_code= status.HTTP_201_CREATED)
async def create_user(cadastro: UsuarioSchema):
    pass
