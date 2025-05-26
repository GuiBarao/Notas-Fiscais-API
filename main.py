from typing import Union

from fastapi import FastAPI, status

from fastapi.middleware.cors import CORSMiddleware

from controllers.filialController import filiais_disponiveis, alterar_valor_teto, nfse_filial
from requests.AtualizarTetoRequest import AtualizarTetoRequest


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


@app.get("/filiais", status_code=status.HTTP_200_OK)
def filiais():
    return filiais_disponiveis()

@app.put('/filiais/valor-teto', status_code=status.HTTP_201_CREATED)
def mudar_valor_teto(request : AtualizarTetoRequest):
    alterar_valor_teto(request.filial, request.novo_valor)
    return "Atualizado!"

@app.get('/filiais/{filial}/notas', status_code=status.HTTP_200_OK)
def notas_filial(filial : str):
    return nfse_filial(filial)


