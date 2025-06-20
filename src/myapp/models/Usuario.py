from sqlalchemy.orm import Mapped, registry, mapped_column
from ..crud.filiais import readFiliais
from typing import List

def filiais():
    tuplas_filiais = readFiliais()
    return [filial for filial, valor_teto in tuplas_filiais]

table_registry = registry()

@table_registry.mapped_as_dataclass
class Usuario:
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str]
    nome_usuario: Mapped[str] = mapped_column(unique=True)
    cpf: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    filais: Mapped[List[str]]