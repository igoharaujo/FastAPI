from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def home():
    return {"message": "Autenticação bem-sucedida"}


@auth_router.post("/criar_conta")
async def criar_conta(
   
   usuario_schmea: UsuarioSchema,
    session: Session = Depends(pegar_sessao)
):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schmea.email).first()

    if usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    senha_criptografada = bcrypt_context.hash(usuario_schmea.senha)

    novo_usuario = Usuario(
        usuario_schmea.nome,
        usuario_schmea.email,
        senha_criptografada,
        usuario_schmea.ativo,
        usuario_schmea.admin
    )

    session.add(novo_usuario)
    session.commit()

    return {"message": f"Conta criada com sucesso para o email {usuario_schmea.email}"}
