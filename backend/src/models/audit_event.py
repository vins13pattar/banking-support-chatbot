"""Audit event model."""

import uuid
from datetime import datetime, timezone

from sqlmodel import Column, Field, SQLModel
from sqlalchemy import JSON


class AuditEvent(SQLModel, table=True):
    """Immutable audit log for sensitive operations."""

    __tablename__ = "audit_events"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    thread_id: str = Field(index=True, max_length=100)
    actor_type: str = Field(max_length=20)  # agent, reviewer, system
    actor_id: str = Field(max_length=100)
    event_type: str = Field(max_length=50)  # approval_requested, approved, rejected, action_executed, escalated
    event_payload: dict = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
