from typing import Union

from fastapi import FastAPI, status

from fastapi.middleware.cors import CORSMiddleware

from app.routers.filiais import filiais_router

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(filiais_router)


