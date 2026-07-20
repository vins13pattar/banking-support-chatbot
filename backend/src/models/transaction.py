"""Transaction model."""

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    """Mock bank transaction."""

    __tablename__ = "transactions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    account_id: uuid.UUID = Field(index=True, foreign_key="accounts.id")
    transaction_reference: str = Field(max_length=30, unique=True)  # e.g. "TXN-7782"
    transaction_type: str = Field(max_length=20)  # upi, neft, imps, atm, pos, transfer
    amount: Decimal = Field(max_digits=15, decimal_places=2)
    currency: str = Field(default="INR", max_length=5)
    merchant: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=500)
    status: str = Field(max_length=20)  # completed, pending, failed, reversed
    transaction_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
