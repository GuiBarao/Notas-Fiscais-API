from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, String, Enum as sqlAlchemy_Enum
from src.myapp.db.database import Base
from typing import List
from enum import Enum

class Status(Enum):
    INATIVO = 0
    ATIVO = 1

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(200))
    nomeUsuario: Mapped[str] = mapped_column(String(100), unique=True)
    cpf: Mapped[str] = mapped_column(String(11), unique=True)
    senha: Mapped[str] = mapped_column(String(200))
    filiais: Mapped[List[str]] = mapped_column(JSON, default=list)
    status: Mapped[Status] = mapped_column(sqlAlchemy_Enum(Status, native_enum=False), default=Status.ATIVO)

