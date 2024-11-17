"""initial

Revision ID: e8ce41d90551
Revises:
Create Date: 2024-03-26 11:15:43.988656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e8ce41d90551'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('albums',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('cover_photo_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_albums_date_created'), 'albums', ['date_created'], unique=False)
    op.create_index(op.f('ix_albums_name'), 'albums', ['name'], unique=False)
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('date_taken', sa.DateTime(), nullable=False),
    sa.Column('file_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('format', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('mode', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('width', sa.Integer(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('exif_data', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['album_id'], ['albums.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, source_table='albums', local_cols=['cover_photo_id'], referent_table='photos', remote_cols=['id'])
    op.create_index(op.f('ix_photos_date_created'), 'photos', ['date_created'], unique=False)
    op.create_index(op.f('ix_photos_date_taken'), 'photos', ['date_taken'], unique=False)
    op.create_index(op.f('ix_photos_name'), 'photos', ['name'], unique=False)
    op.create_table('users',
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_index(op.f('ix_photos_name'), table_name='photos')
    op.drop_index(op.f('ix_photos_date_taken'), table_name='photos')
    op.drop_index(op.f('ix_photos_date_created'), table_name='photos')
    op.drop_table('photos')
    op.drop_index(op.f('ix_albums_name'), table_name='albums')
    op.drop_index(op.f('ix_albums_date_created'), table_name='albums')
    op.drop_table('albums')
    # ### end Alembic commands ###
