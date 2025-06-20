from typing import Union

from fastapi import FastAPI, status

from fastapi.middleware.cors import CORSMiddleware

from .routers.filiais import filiais_router
from .routers.usuarios import usuarios_router

from myapp.config.settings import url_front

app = FastAPI()

origins = [
    url_front
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(filiais_router)
app.include_router(usuarios_router)


