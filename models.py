from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
#from sqlalchemy_utils.types import ChoiceType


db = create_engine("sqlite:///banco.db")

Base = declarative_base()


# criar as classes/tabelas do banco

# usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, nullable=False, primary_key=True, autoincrement=True, index=True)
    nome = Column("nome", String, index=True)
    email = Column("email", String, nullable=False,  unique=True, index=True)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome: str, email: str, senha: str, ativo: bool = True, admin: bool = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

# Pedido

class Pedido(Base):
    __tablename__ = "pedidos"

    #STATUS_PEDIDOS = (
    #    ("pendente", "Pendente"),
    #    ("cancelado", "Cancelado"),
    #    ("concluido", "Concluído"),
    #)

    id = Column("id", Integer, nullable=False, primary_key=True, autoincrement=True, index=True)
    status = Column("status", String, default="pendente")
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    total = Column("total", Float, nullable=False)

    def __init__(self, usuario_id: int,  status: str = "pendente", total: float = 0.0):
        self.status = status
        self.usuario_id = usuario_id
        self.total = total

# ItensPedido
class ItensPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, nullable=False, primary_key=True, autoincrement=True, index=True)
    pedido_id = Column("pedido_id", Integer, ForeignKey("pedidos.id"), nullable=False)
    quantidade = Column("quantidade", Integer, nullable=False)
    sabor = Column("sabor", String, nullable=True)
    tamanho = Column("tamanho", String, nullable=True)
    preco_unitario = Column("preco_unitario", Float, nullable=False)

    def __init__(self, pedido_id: int, sabor: str, quantidade: int, tamanho: str, preco_unitario: float):
        self.pedido_id = pedido_id
        self.sabor = sabor
        self.quantidade = quantidade
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario