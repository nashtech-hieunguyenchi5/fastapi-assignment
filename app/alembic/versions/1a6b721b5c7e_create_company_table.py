"""create company table

Revision ID: 1a6b721b5c7e
Revises: 265a0719faed
Create Date: 2024-09-04 17:48:12.126378

"""
from uuid import uuid4
from datetime import datetime, timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a6b721b5c7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Company Table
    company_table = op.create_table(
        "companies",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, index=True),
        sa.Column("description", sa.String),
        sa.Column("mode", sa.String),
        sa.Column("rating", sa.Integer),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    op.bulk_insert(company_table, [
        {
            "name": "Test Company A", 
            "description": "This is the company for Test - A"
        }

    ])


def downgrade() -> None:
    # Rollback foreign key
    op.drop_table("companies")
