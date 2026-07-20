"""Customer model."""

import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Customer(SQLModel, table=True):
    """Mock bank customer."""

    __tablename__ = "customers"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_number: str = Field(index=True, unique=True, max_length=20)
    full_name: str = Field(max_length=200)
    email: str = Field(max_length=200)
    phone_masked: str = Field(max_length=20)
    date_of_birth: str = Field(max_length=10, default="")  # YYYY-MM-DD for mock verification
    verification_answer: str = Field(max_length=10, default="")  # last 4 digits of phone for mock
    verification_status: str = Field(default="unverified", max_length=20)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
