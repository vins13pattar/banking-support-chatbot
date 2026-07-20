"""Ticket service for creating and updating support tickets."""

import uuid
from typing import Any
from sqlmodel import Session, select

from src.database import engine
from src.models.support_ticket import SupportTicket


def create_support_ticket(
    customer_id: str,
    thread_id: str,
    category: str,
    description: str,
    priority: str = "medium"
) -> dict[str, Any]:
    """Create a new support ticket."""
    with Session(engine) as session:
        ticket = SupportTicket(
            customer_id=uuid.UUID(customer_id) if customer_id else None,
            thread_id=thread_id,
            category=category,
            description=description,
            priority=priority,
            status="open"
        )
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        
        return {
            "ticket_id": str(ticket.id),
            "category": ticket.category,
            "status": ticket.status,
            "priority": ticket.priority,
        }


def get_ticket_status(ticket_id: str) -> dict[str, Any] | None:
    """Get the status and details of a support ticket."""
    with Session(engine) as session:
        statement = select(SupportTicket).where(SupportTicket.id == uuid.UUID(ticket_id))
        ticket = session.exec(statement).first()
        
        if ticket:
            return {
                "ticket_id": str(ticket.id),
                "category": ticket.category,
                "status": ticket.status,
                "priority": ticket.priority,
                "description": ticket.description,
                "created_at": ticket.created_at.isoformat(),
            }
    return None
