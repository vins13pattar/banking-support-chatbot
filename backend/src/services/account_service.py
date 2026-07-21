"""Account service for retrieving account details and balances."""

from sqlmodel import Session, select

from src.database import engine
from src.models.account import Account


def get_customer_accounts(customer_id: str) -> list[Account]:
    """Retrieve all accounts for a verified customer."""
    with Session(engine) as session:
        statement = select(Account).where(Account.customer_id == customer_id)
        return list(session.exec(statement).all())


def get_account_summary(account_id: str, customer_id: str) -> Account | None:
    """Retrieve details for a specific account, ensuring it belongs to the customer."""
    with Session(engine) as session:
        statement = select(Account).where(
            Account.id == account_id,
            Account.customer_id == customer_id
        )
        return session.exec(statement).first()


def check_account_balance(account_id: str, customer_id: str) -> dict | None:
    """Get the available balance for a specific account."""
    account = get_account_summary(account_id, customer_id)
    if account:
        return {
            "account_number_masked": account.account_number_masked,
            "account_type": account.account_type,
            "available_balance": float(account.available_balance),
            "currency": account.currency,
            "status": account.status,
        }
    return None
