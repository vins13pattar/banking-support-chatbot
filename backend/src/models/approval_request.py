"""Approval request model."""

import uuid
from datetime import datetime, timezone

from sqlmodel import Column, Field, SQLModel
from sqlalchemy import JSON


class ApprovalRequest(SQLModel, table=True):
    """HITL approval request for sensitive actions."""

    __tablename__ = "approval_requests"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    thread_id: str = Field(index=True, max_length=100)
    customer_id: uuid.UUID = Field(foreign_key="customers.id")
    action_type: str = Field(max_length=50)  # CREATE_DISPUTE, BLOCK_CARD, REPLACE_CARD, etc.
    action_summary: str = Field(default="", max_length=500)
    proposed_payload: dict = Field(default_factory=dict, sa_column=Column(JSON))
    risk_level: str = Field(max_length=20)  # low, medium, high, critical
    status: str = Field(default="pending", max_length=20)  # pending, approved, rejected, modified
    reviewer: str = Field(default="", max_length=100)
    reviewer_comment: str = Field(default="")
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewed_at: datetime | None = Field(default=None)
