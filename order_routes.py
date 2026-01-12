from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    return {"message": "Lista de pedidos"}


@order_router.post("/")
async def criar_pedido(
    pedido_schema: PedidoSchema,
    session: Session = Depends(pegar_sessao)
   ):
    novo_pedido = Pedido(
        pedido_schema.usuario_id
    )

    session.add(novo_pedido)
    session.commit()

    return {"message": f"Pedido criado com sucesso id do pedido: {novo_pedido.id}"}