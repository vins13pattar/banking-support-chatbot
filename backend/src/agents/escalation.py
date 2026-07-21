"""Escalation node."""

from src.services.ticket_service import create_support_ticket


async def escalation_node(state: dict) -> dict:
    """Handle escalation to human agents by creating a ticket."""
    
    # Check if we already have an escalation reason or if it's general
    reason = state.get("escalation_reason", "Customer requested human assistance or agent failed to resolve.")
    
    # Create the ticket
    ticket = create_support_ticket(
        customer_id=state.get("customer_id"),
        thread_id=state.get("thread_id", "unknown_thread"),
        category="escalation",
        description=reason,
        priority="high"
    )
    
    ticket_id = ticket.get("ticket_id")
    
    # Create a system message to inform the user
    message = f"I have escalated your request to a human agent. Your ticket reference number is {ticket_id}. Our team will review this shortly."
    
    from langchain_core.messages import AIMessage
    
    return {
        "messages": [AIMessage(content=message)],
        "escalation_required": False,  # Reset flag as it's been handled
        "active_agent": None
    }
