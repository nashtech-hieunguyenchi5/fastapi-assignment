"""create task table

Revision ID: 99023e4883bc
Revises: 265a0719faed
Create Date: 2024-09-04 18:03:58.760790

"""
from alembic import op
import sqlalchemy as sa
from entities.task import TaskStatus, TaskPriority

# revision identifiers, used by Alembic.
revision = '99023e4883bc'
down_revision = '265a0719faed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Task Table
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("summary", sa.String, nullable=False),
        sa.Column("description", sa.String),
        sa.Column('status', sa.Enum(TaskStatus, name="taskstatus"), nullable=False, server_default=TaskStatus.OPEN.name),
        sa.Column('priority', sa.Enum(TaskPriority, name="taskpriority"), nullable=False, server_default=TaskPriority.NORMAL.name),
        sa.Column('user_id', sa.UUID, sa.ForeignKey('users.id'), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    op.create_foreign_key('fk_task_user', 'tasks', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_table('tasks')
    op.execute("DROP TYPE taskstatus;")
    op.execute("DROP TYPE taskpriority;")
