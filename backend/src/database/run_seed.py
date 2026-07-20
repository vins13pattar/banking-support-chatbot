"""Seed the database with initial mock data."""

import logging
from sqlalchemy import select
from sqlmodel import Session

from src.database import engine
from src.models import (
    Account,
    Customer,
    KnowledgeDocument,
    Transaction,
)

# Important: adjust pythonpath if needed, but assuming run from backend/
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from database.seed.seed_customers import CUSTOMERS
from database.seed.seed_accounts import ACCOUNTS
from database.seed.seed_transactions import TRANSACTIONS
from database.seed.seed_knowledge import KNOWLEDGE_DOCUMENTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_database() -> None:
    """Insert all seed data into the database if not already present."""
    logger.info("Starting database seed process...")
    
    with Session(engine) as session:
        # Seed Customers
        for cust_data in CUSTOMERS:
            # Check if exists
            existing = session.exec(select(Customer).where(Customer.id == cust_data["id"])).first()
            if not existing:
                customer = Customer(**cust_data)
                session.add(customer)
        session.commit()
        logger.info(f"Seeded customers.")

        # Seed Accounts
        for acc_data in ACCOUNTS:
            existing = session.exec(select(Account).where(Account.id == acc_data["id"])).first()
            if not existing:
                account = Account(**acc_data)
                session.add(account)
        session.commit()
        logger.info(f"Seeded accounts.")

        # Seed Transactions
        for txn_data in TRANSACTIONS:
            existing = session.exec(select(Transaction).where(Transaction.id == txn_data["id"])).first()
            if not existing:
                transaction = Transaction(**txn_data)
                session.add(transaction)
        session.commit()
        logger.info(f"Seeded transactions.")
        
        # Seed Knowledge Documents
        for doc_data in KNOWLEDGE_DOCUMENTS:
            existing = session.exec(select(KnowledgeDocument).where(KnowledgeDocument.id == doc_data["id"])).first()
            if not existing:
                doc = KnowledgeDocument(**doc_data)
                session.add(doc)
        session.commit()
        logger.info(f"Seeded knowledge documents.")
        
    logger.info("Database seeding complete!")


if __name__ == "__main__":
    seed_database()
