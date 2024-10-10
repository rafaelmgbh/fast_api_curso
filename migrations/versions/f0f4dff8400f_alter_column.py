"""alter column

Revision ID: f0f4dff8400f
Revises: 9dad6c5eac8e
Create Date: 2024-10-10 10:28:29.450241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = 'f0f4dff8400f'
down_revision: Union[str, None] = '9dad6c5eac8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Remover as colunas antigas
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'updated_at')

    # Criar as colunas novamente com as configurações desejadas
    op.add_column('users', sa.Column('created_at', sa.DateTime(), server_default=func.now(), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), server_default=func.now(), onupdate=func.now(),
                                     nullable=False))


def downgrade():
    # Remover as colunas novas
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'updated_at')

    # Restaurar as colunas antigas (se necessário, ajuste conforme o caso anterior)
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=True))