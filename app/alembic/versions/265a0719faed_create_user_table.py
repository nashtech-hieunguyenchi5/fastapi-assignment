"""create user table

Revision ID: 265a0719faed
Revises: 
Create Date: 2024-09-04 17:27:03.675913

"""
from uuid import uuid4
from datetime import datetime, timezone
from alembic import op
import sqlalchemy as sa

from entities.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD

# revision identifiers, used by Alembic.
revision = '265a0719faed'
down_revision = '1a6b721b5c7e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # User Table
    user_table = op.create_table(
        "users",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("hashed_password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column("company_id", sa.Integer),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    op.create_foreign_key('fk_user_company', 'users', 'companies', ['company_id'], ['id'])

    op.bulk_insert(user_table, [
        {
            "id": uuid4(),
            "email": "admin@sample.com", 
            "username": "admin",
            "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "first_name": "Admin",
            "last_name": "Test",
            "is_active": True,
            "is_admin": True,
            "company_id": 1
        }, 
        {
            "id": uuid4(),
            "email": "user@sample.com", 
            "username": "user",
            "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "first_name": "User",
            "last_name": "Test",
            "is_active": True,
            "is_admin": False,
            "company_id": 1
        }, 

    ])


def downgrade() -> None:
    # Rollback foreign key
    op.drop_constraint('fk_user_company', 'users', type_='foreignkey')
    op.drop_table("users")
