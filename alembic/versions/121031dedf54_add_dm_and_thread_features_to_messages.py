"""add_dm_and_thread_features_to_messages

Revision ID: 121031dedf54
Revises: 1bfb035d8cc6
Create Date: 2025-06-09 13:54:03.843598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '121031dedf54'
down_revision: Union[str, None] = '1bfb035d8cc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # messagesテーブルに新しいカラムを追加
    op.add_column('messages', sa.Column('recipient_id', sa.Integer(), nullable=True))
    op.add_column('messages', sa.Column('is_read', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('messages', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('messages', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
    
    # 外部キー制約を追加
    op.create_foreign_key('fk_messages_recipient_id', 'messages', 'users', ['recipient_id'], ['id'])
    
    # project_idをnullable=Trueに変更
    op.alter_column('messages', 'project_id', nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # 外部キー制約を削除
    op.drop_constraint('fk_messages_recipient_id', 'messages', type_='foreignkey')
    
    # 追加したカラムを削除
    op.drop_column('messages', 'updated_at')
    op.drop_column('messages', 'is_deleted')
    op.drop_column('messages', 'is_read')
    op.drop_column('messages', 'recipient_id')
    
    # project_idをnullable=Falseに戻す
    op.alter_column('messages', 'project_id', nullable=False)
