from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])
def criar_token(usuario_id: int):
    token = f"fnsyubf7s8f9{usuario_id}"
    return token

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


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Email não cadastrado")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token, "token_type": "bearer"}

