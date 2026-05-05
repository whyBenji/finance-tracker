"""create transactions table

Revision ID: 20260505_01
Revises:
Create Date: 2026-05-05 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260505_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("is_subscription", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_transactions_category", "transactions", ["category"])
    op.create_index("ix_transactions_date", "transactions", ["date"])


def downgrade() -> None:
    op.drop_index("ix_transactions_date", table_name="transactions")
    op.drop_index("ix_transactions_category", table_name="transactions")
    op.drop_table("transactions")
