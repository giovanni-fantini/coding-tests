"""Initial migration

Revision ID: 767efaa6b483
Revises: 
Create Date: 2024-06-17 05:41:00.458114

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '767efaa6b483'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""
    CREATE TABLE people (
        id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
        name VARCHAR(255)
    )
    WITH SYSTEM VERSIONING
    """)
    op.create_index(op.f('ix_people_name'), 'people', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_people_name'), table_name='people')
    op.execute("DROP TABLE people")
    # ### end Alembic commands ###