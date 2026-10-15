"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-10-15
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_username", "users", ["username"])

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.String(length=100), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("expected_qty", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("order_id"),
    )
    op.create_index("ix_orders_order_id", "orders", ["order_id"])
    op.create_index("ix_orders_sku", "orders", ["sku"])

    op.create_table(
        "warehouse_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.String(length=100), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("actual_qty", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("order_id", "sku", name="uq_warehouse_order_sku"),
    )
    op.create_index("ix_warehouse_records_order_id", "warehouse_records", ["order_id"])
    op.create_index("ix_warehouse_records_sku", "warehouse_records", ["sku"])

    op.create_table(
        "exceptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.String(length=100), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("expected_qty", sa.Integer(), nullable=False),
        sa.Column("actual_qty", sa.Integer(), nullable=False),
        sa.Column("difference", sa.Integer(), nullable=False),
        sa.Column("exception_type", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("resolution_note", sa.Text(), nullable=True),
        sa.Column("acknowledged_by", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("order_id", "sku", name="uq_exception_order_sku"),
    )
    op.create_index("ix_exceptions_order_id", "exceptions", ["order_id"])
    op.create_index("ix_exceptions_sku", "exceptions", ["sku"])
    op.create_index("ix_exceptions_exception_type", "exceptions", ["exception_type"])
    op.create_index("ix_exceptions_severity", "exceptions", ["severity"])
    op.create_index("ix_exceptions_status", "exceptions", ["status"])

    op.create_table(
        "triage_decisions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("exception_id", sa.Integer(), sa.ForeignKey("exceptions.id"), nullable=False),
        sa.Column("source", sa.String(length=30), nullable=False),
        sa.Column("classification", sa.String(length=100), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("recommended_action", sa.Text(), nullable=False),
        sa.Column("requires_human_review", sa.Boolean(), nullable=False),
        sa.Column("approved", sa.Boolean(), nullable=True),
        sa.Column("approved_by", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_triage_decisions_exception_id", "triage_decisions", ["exception_id"])

    op.create_table(
        "automation_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_job_id", sa.String(length=100), nullable=False),
        sa.Column("exception_id", sa.Integer(), sa.ForeignKey("exceptions.id"), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("portal_status", sa.String(length=100), nullable=True),
        sa.Column("portal_quantity", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("external_job_id"),
    )
    op.create_index("ix_automation_jobs_external_job_id", "automation_jobs", ["external_job_id"])
    op.create_index("ix_automation_jobs_exception_id", "automation_jobs", ["exception_id"])
    op.create_index("ix_automation_jobs_status", "automation_jobs", ["status"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("actor", sa.String(length=100), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_audit_logs_entity_type", "audit_logs", ["entity_type"])
    op.create_index("ix_audit_logs_entity_id", "audit_logs", ["entity_id"])

    op.create_table(
        "idempotency_keys",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(length=200), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("key"),
    )
    op.create_index("ix_idempotency_keys_key", "idempotency_keys", ["key"])


def downgrade() -> None:
    op.drop_table("idempotency_keys")
    op.drop_table("audit_logs")
    op.drop_table("automation_jobs")
    op.drop_table("triage_decisions")
    op.drop_table("exceptions")
    op.drop_table("warehouse_records")
    op.drop_table("orders")
    op.drop_table("users")
