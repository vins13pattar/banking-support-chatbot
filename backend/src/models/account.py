"""Account model."""

import uuid
from decimal import Decimal

from sqlmodel import Field, SQLModel


class Account(SQLModel, table=True):
    """Mock bank account linked to a customer."""

    __tablename__ = "accounts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID = Field(index=True, foreign_key="customers.id")
    account_number_masked: str = Field(max_length=20)  # e.g. "XXXX-XXXX-1234"
    account_type: str = Field(max_length=20)  # savings, current, fixed_deposit
    available_balance: Decimal = Field(default=Decimal("0.00"), max_digits=15, decimal_places=2)
    currency: str = Field(default="INR", max_length=5)
    status: str = Field(default="active", max_length=20)  # active, dormant, closed, frozen
