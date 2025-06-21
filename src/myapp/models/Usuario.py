from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, String
from src.myapp.db.database import Base
from typing import List

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(200))
    nomeUsuario: Mapped[str] = mapped_column(String(100), unique=True)
    cpf: Mapped[str] = mapped_column(String(11), unique=True)
    senha: Mapped[str] = mapped_column(String(200))
    filais: Mapped[List[str]] = mapped_column(JSON, default=list)