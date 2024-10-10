"""create available slots table

Revision ID: 4d6ccf3d9b89
Revises: 
Create Date: 2024-10-05 11:37:52.490822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d6ccf3d9b89'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('available_slots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(), nullable=False),
    sa.Column('court_id', sa.String(), nullable=False),
    sa.Column('available_hour', sa.Integer(), nullable=False),
    sa.Column('court_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'court_id', 'available_hour', name='unique_slot')
    )
    op.create_index(op.f('ix_available_slots_id'), 'available_slots', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('available_slots',
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('court_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('available_hour', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('court_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.UniqueConstraint('date', 'court_id', 'available_hour', name='unique_date_court_hour')
    )
    op.drop_index(op.f('ix_available_slots_id'), table_name='available_slots')
    op.drop_table('available_slots')
    # ### end Alembic commands ###