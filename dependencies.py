from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError

from main import oauth2_scheme, SECRET_KEY, ALGORITHM
from models import db, Usuario


SessionLocal = sessionmaker(bind=db)


def pegar_sessao():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def verificar_token(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(pegar_sessao)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(payload.get("sub"))
        if not usuario_id:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario
