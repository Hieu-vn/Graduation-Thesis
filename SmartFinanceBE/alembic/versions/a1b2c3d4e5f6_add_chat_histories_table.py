"""add chat_histories table

Revision ID: a1b2c3d4e5f6
Revises: 4e04968d99fc
Create Date: 2026-02-27 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '4e04968d99fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'chat_histories',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_id', sa.String(36), nullable=False, index=True),
        sa.Column('role', sa.Enum('user', 'assistant', name='chat_role'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_chat_histories_user_session', 'chat_histories', ['user_id', 'session_id'])


def downgrade() -> None:
    op.drop_index('ix_chat_histories_user_session', table_name='chat_histories')
    op.drop_table('chat_histories')
    op.execute("DROP TYPE IF EXISTS chat_role")
