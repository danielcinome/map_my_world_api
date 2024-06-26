"""Added tables

Revision ID: 92662d10efce
Revises: 
Create Date: 2024-04-10 11:11:56.793617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import app


# revision identifiers, used by Alembic.
revision: str = '92662d10efce'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('uuid', app.db.utils.dialect_translator.GUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('location',
    sa.Column('uuid', app.db.utils.dialect_translator.GUID(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('user',
    sa.Column('uuid', app.db.utils.dialect_translator.GUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('location_category_reviewed',
    sa.Column('location_uuid', app.db.utils.dialect_translator.GUID(), nullable=False),
    sa.Column('category_uuid', app.db.utils.dialect_translator.GUID(), nullable=False),
    sa.Column('last_reviewed_date', app.db.utils.dialect_translator.CustomDateTime(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_uuid'], ['category.uuid'], ),
    sa.ForeignKeyConstraint(['location_uuid'], ['location.uuid'], ),
    sa.PrimaryKeyConstraint('location_uuid', 'category_uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('location_category_reviewed')
    op.drop_table('user')
    op.drop_table('location')
    op.drop_table('category')
    # ### end Alembic commands ###
