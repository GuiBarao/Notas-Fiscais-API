"""Cria usuário inicial

Revision ID: e51c93ab6640
Revises: 195ebc81393a
Create Date: 2025-07-26 10:45:09.233793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.myapp.security import get_password_hash
import json

# revision identifiers, used by Alembic.
revision: str = 'e51c93ab6640'
down_revision: Union[str, Sequence[str], None] = '195ebc81393a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    senha = get_password_hash("000")

    filiais = json.dumps(['AMAMBAI','DOURADOS','GUAIRA'])

    op.execute("INSERT INTO usuarios (nome, nomeUsuario, cpf, senha, filiais)" + \
                f"VALUES ('Convidado', 'Convidado', '00000000000', '{senha}', {filiais})")


def downgrade() -> None:
    """Downgrade schema."""
    
    op.execute("DELETE FROM usuarios WHERE cpf = '00000000000'")
