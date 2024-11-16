"""default_users

Revision ID: 2152d60aa2a1
Revises: e8ce41d90551
Create Date: 2024-03-26 11:19:20.093271

"""
from argon2 import PasswordHasher
from os import environ
from pixelperfect.db.models import User
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2152d60aa2a1'
down_revision: Union[str, None] = 'e8ce41d90551'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(User.__table__, [
        {
            'username': 'admin',
            'password': PasswordHasher().hash(environ.get('INITIAL_PASSWORD_ADMIN', 'pixelperfect')),
            'is_admin': 1
        },
        {
            'username': 'viewer',
            'password': PasswordHasher().hash(environ.get('INITIAL_PASSWORD_VIEWER', 'pixelperfect')),
            'is_admin': 0
        }
    ])


def downgrade() -> None:
    pass
