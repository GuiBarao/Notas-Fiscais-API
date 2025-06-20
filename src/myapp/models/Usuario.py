from sqlalchemy.orm import Mapped, registry, mapped_column
from sqlalchemy import JSON
from typing import List

table_registry = registry()

@table_registry.mapped_as_dataclass
class Usuario:
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str]
    nomeUsuario: Mapped[str] = mapped_column(unique=True)
    cpf: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    filais: Mapped[List[str]] = mapped_column(JSON, default=list)