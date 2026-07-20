"""Support ticket tools."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.services.ticket_service import create_support_ticket, get_ticket_status


class CreateSupportTicketInput(BaseModel):
    customer_id: str | None = Field(default=None, description="The customer UUID if authenticated")
    thread_id: str = Field(description="The LangGraph conversation thread ID")
    category: str = Field(description="Ticket category (dispute, card_issue, escalation, general)")
    description: str = Field(description="Detailed description of the issue")
    priority: str = Field(default="medium", description="Ticket priority (low, medium, high, critical)")


@tool("create_support_ticket", args_schema=CreateSupportTicketInput)
def create_support_ticket_tool(
    thread_id: str,
    category: str,
    description: str,
    customer_id: str | None = None,
    priority: str = "medium"
) -> dict:
    """Create a new customer support ticket.
    Returns the ticket_id which should be provided to the customer.
    """
    ticket = create_support_ticket(
        customer_id=customer_id,
        thread_id=thread_id,
        category=category,
        description=description,
        priority=priority
    )
    return {"status": "success", "ticket": ticket}


class GetTicketStatusInput(BaseModel):
    ticket_id: str = Field(description="The unique ticket UUID")


@tool("get_ticket_status", args_schema=GetTicketStatusInput)
def get_ticket_status_tool(ticket_id: str) -> dict:
    """Check the status of an existing support ticket."""
    try:
        status = get_ticket_status(ticket_id)
        if status:
            return {"status": "success", "data": status}
        return {"status": "error", "message": "Ticket not found."}
    except ValueError:
        return {"status": "error", "message": "Invalid ticket ID format."}
