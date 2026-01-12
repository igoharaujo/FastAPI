from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

# engine (banco)
db = create_engine(
    "sqlite:///banco.db",
    connect_args={"check_same_thread": False}
)

Base = declarative_base()


# ======================
# TABELA USUARIOS
# ======================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    senha = Column(String)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    def __init__(self, nome: str, email: str, senha: str, ativo: bool = True, admin: bool = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


# ======================
# TABELA PEDIDOS
# ======================
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    status = Column(String, default="pendente")
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    total = Column(Float, nullable=False)

    def __init__(self, usuario_id: int, status: str = "pendente", total: float = 0.0):
        self.status = status
        self.usuario_id = usuario_id
        self.total = total


# ======================
# TABELA ITENS_PEDIDO
# ======================
class ItensPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    sabor = Column(String, nullable=True)
    tamanho = Column(String, nullable=True)
    preco_unitario = Column(Float, nullable=False)

    def __init__(self, pedido_id: int, sabor: str, quantidade: int, tamanho: str, preco_unitario: float):
        self.pedido_id = pedido_id
        self.sabor = sabor
        self.quantidade = quantidade
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario


