from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

SECRET_KEY = os.getenv("SECRET_KEY")  # Obtém o valor da variável
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from auth_routes import  auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)


# para executar o servidor use o comando: uvicorn main:app --reload