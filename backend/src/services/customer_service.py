"""Customer service for looking up and verifying customers."""

from sqlmodel import Session, select

from src.database import engine
from src.models.customer import Customer


def get_customer_by_number(customer_number: str) -> Customer | None:
    """Look up a customer by their customer number."""
    with Session(engine) as session:
        statement = select(Customer).where(Customer.customer_number == customer_number)
        return session.exec(statement).first()


def verify_customer(customer_number: str, dob: str, last_4_phone: str) -> Customer | None:
    """Verify a customer's identity using mock verification details."""
    customer = get_customer_by_number(customer_number)
    if not customer:
        return None
    
    # Mock verification: check DOB and last 4 digits of phone
    if customer.date_of_birth == dob and customer.verification_answer == last_4_phone:
        # Update verification status in db (mocking real-world auth flow)
        with Session(engine) as session:
            db_customer = session.exec(select(Customer).where(Customer.id == customer.id)).first()
            if db_customer:
                db_customer.verification_status = "verified"
                session.add(db_customer)
                session.commit()
                session.refresh(db_customer)
                return db_customer
                
    return None
