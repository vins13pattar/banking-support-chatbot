"""Support ticket model."""

import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class SupportTicket(SQLModel, table=True):
    """Customer support ticket created by agents or escalation."""

    __tablename__ = "support_tickets"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID = Field(index=True, foreign_key="customers.id")
    thread_id: str = Field(index=True, max_length=100)
    category: str = Field(max_length=50)  # dispute, card_issue, escalation, general
    description: str = Field(default="")
    priority: str = Field(default="medium", max_length=20)  # low, medium, high, critical
    status: str = Field(default="open", max_length=20)  # open, in_progress, resolved, closed
    assigned_to: str = Field(default="", max_length=100)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
