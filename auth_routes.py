from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(usuario_id: int, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(usuario_id), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

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
    usuario = autenticar_usuario(
        login_schema.email,
        login_schema.senha,
        session
    )
    if not usuario:
        raise HTTPException(status_code=400, detail="Email não cadastrado ou senha incorreta")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
              }



@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(
        dados_formulario.username,
        dados_formulario.password,
        session
    )
    if not usuario:
        raise HTTPException(status_code=400, detail="Email não cadastrado ou senha incorreta")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "bearer"
              }




@auth_router.post("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(Usuario.id)
    return {
            "access_token": access_token,
            "token_type": "bearer"
              }