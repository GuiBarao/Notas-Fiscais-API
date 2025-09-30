from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from src.myapp.routers.filiais import filiais_router

import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
origins = [
    os.getenv("URL_FRONT")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(filiais_router)


