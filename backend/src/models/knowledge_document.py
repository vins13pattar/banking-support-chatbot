"""Knowledge document model."""

import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class KnowledgeDocument(SQLModel, table=True):
    """Banking knowledge base entry for FAQ agent."""

    __tablename__ = "knowledge_documents"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=300, index=True)
    category: str = Field(max_length=50, index=True)  # general, accounts, cards, loans, fees, policies
    version: str = Field(default="1.0", max_length=10)
    content: str = Field(default="")
    active: bool = Field(default=True)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
