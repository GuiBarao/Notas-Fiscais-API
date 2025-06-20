from pwdlib import PasswordHash
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode

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