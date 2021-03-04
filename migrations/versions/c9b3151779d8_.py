"""empty message

Revision ID: c9b3151779d8
Revises: 
Create Date: 2021-03-03 19:24:49.615258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9b3151779d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('race', sa.String(), nullable=True),
    sa.Column('player_character', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_characters_name'), 'characters', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_characters_name'), table_name='characters')
    op.drop_table('characters')
    # ### end Alembic commands ###