import os
from dotenv import load_dotenv

load_dotenv()

url_front = os.getenv("URL_FRONT")
driver = os.getenv("DRIVER_MYSQL")
user = os.getenv("USER_MYSQL")
password = os.getenv("PASSWORD_MYSQL")
host = os.getenv("HOST_MYSQL")
port = os.getenv("PORT_MYSQL")
database = os.getenv("DATABASE_MYSQL")