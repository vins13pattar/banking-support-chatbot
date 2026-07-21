"""Transaction service for querying and analyzing transactions."""

from typing import Any
from sqlalchemy import desc
from sqlmodel import Session, select

from src.database import engine
from src.models.transaction import Transaction
from src.services.account_service import get_customer_accounts


def get_recent_transactions(customer_id: str, limit: int = 10) -> list[dict[str, Any]]:
    """Retrieve recent transactions across all accounts for a customer."""
    with Session(engine) as session:
        # First get all account IDs for the customer
        accounts = get_customer_accounts(customer_id)
        account_ids = [acc.id for acc in accounts]
        
        if not account_ids:
            return []

        # Then query transactions for those accounts
        statement = (
            select(Transaction)
            .where(Transaction.account_id.in_(account_ids))
            .order_by(desc(Transaction.transaction_date))
            .limit(limit)
        )
        
        results = session.exec(statement).all()
        
        # Serialize to dict for the LLM
        return [
            {
                "transaction_reference": txn.transaction_reference,
                "transaction_type": txn.transaction_type,
                "amount": float(txn.amount),
                "currency": txn.currency,
                "merchant": txn.merchant,
                "description": txn.description,
                "status": txn.status,
                "transaction_date": txn.transaction_date.isoformat(),
            }
            for txn in results
        ]


def search_transactions(customer_id: str, merchant_query: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
    """Search transactions for a customer based on criteria."""
    with Session(engine) as session:
        accounts = get_customer_accounts(customer_id)
        account_ids = [acc.id for acc in accounts]
        
        if not account_ids:
            return []

        statement = select(Transaction).where(Transaction.account_id.in_(account_ids))
        
        if merchant_query:
            # Simple case-insensitive likeness match
            statement = statement.where(Transaction.merchant.ilike(f"%{merchant_query}%"))
            
        if status:
            statement = statement.where(Transaction.status == status)
            
        statement = statement.order_by(desc(Transaction.transaction_date)).limit(20)
        
        results = session.exec(statement).all()
        
        return [
            {
                "transaction_reference": txn.transaction_reference,
                "transaction_type": txn.transaction_type,
                "amount": float(txn.amount),
                "currency": txn.currency,
                "merchant": txn.merchant,
                "description": txn.description,
                "status": txn.status,
                "transaction_date": txn.transaction_date.isoformat(),
            }
            for txn in results
        ]


def get_transaction_details(transaction_reference: str, customer_id: str) -> dict[str, Any] | None:
    """Get details of a specific transaction by reference.

    Requires customer_id and verifies the transaction belongs to one of the
    customer's own accounts. Per PRD §13.7 ("Customer and thread ownership
    must be verified in application code") and §19.3 ("Reveal another
    customer's transactions" is an explicit attack to defend against):
    without this check, any authenticated customer could look up any other
    customer's transaction by reference alone.
    """
    with Session(engine) as session:
        accounts = get_customer_accounts(customer_id)
        account_ids = [acc.id for acc in accounts]
        if not account_ids:
            return None

        statement = select(Transaction).where(
            Transaction.transaction_reference == transaction_reference,
            Transaction.account_id.in_(account_ids),
        )
        txn = session.exec(statement).first()

        if txn:
            return {
                "transaction_reference": txn.transaction_reference,
                "transaction_type": txn.transaction_type,
                "amount": float(txn.amount),
                "currency": txn.currency,
                "merchant": txn.merchant,
                "description": txn.description,
                "status": txn.status,
                "transaction_date": txn.transaction_date.isoformat(),
            }
    return None
