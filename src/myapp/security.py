from pwdlib import PasswordHash
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode, decode
from fastapi import HTTPException, status, Header

load_dotenv()
API_KEY = os.getenv("API_SECRET_KEY")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

__pwd_context = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return __pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return __pwd_context.verify(password, hashed_password)

def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({'exp' : expire})

    encoded_jwt = encode(payload, API_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str) -> dict:
    try:
        dados = decode(token, algorithms=[ALGORITHM], key=API_KEY)
        return dados
    except:
        return False
    
def auth_validation(authorization: str = Header(...)):
    if(not authorization.startswith('Bearer ')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de autorização mal formatado")
    token = authorization.split()[1]
    if(not verify_access_token(token)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token não autorizado")
    
    return token


def getPayload(token:str):
    return decode(token, API_KEY, ALGORITHM)