"""Action Executor node for approved sensitive actions."""

from langchain_core.messages import AIMessage
from src.services.audit_service import log_audit_event
from src.services.ticket_service import create_support_ticket

async def action_executor_node(state: dict) -> dict:
    """Executes the action after human approval."""
    
    proposed_action = state.get("proposed_action")
    if not proposed_action:
        return {"active_agent": None}
        
    action_type = proposed_action.get("action_type")
    payload = proposed_action.get("payload", {})
    
    # In a real system, this would call actual banking APIs.
    # For the prototype, we log the execution and simulate the API call.
    
    execution_result = {}
    
    if action_type == "BLOCK_CARD":
        # Simulate blocking card API
        card_id = payload.get("card_id")
        execution_result = {"status": "success", "message": f"Card {card_id} has been permanently blocked."}
        
    elif action_type == "REPLACE_CARD":
        # Simulate replacing card API
        card_id = payload.get("card_id")
        address = payload.get("address")
        execution_result = {"status": "success", "message": f"New card ordered to replace {card_id}. Will be shipped to {address}."}
        
    elif action_type == "CREATE_DISPUTE":
        # Actually create the dispute ticket
        ticket = create_support_ticket(
            customer_id=state.get("customer_id"),
            thread_id=state.get("thread_id"),
            category="dispute",
            description=payload.get("dispute_details", "Transaction Dispute"),
            priority="high"
        )
        execution_result = {"status": "success", "ticket": ticket, "message": f"Dispute ticket {ticket['ticket_id']} created successfully."}
        
    else:
        execution_result = {"status": "error", "message": f"Unknown action type: {action_type}"}
        
    # Log execution
    log_audit_event(
        thread_id=state.get("thread_id"),
        actor_type="system",
        actor_id="action_executor",
        event_type="action_executed",
        event_payload={"action": proposed_action, "result": execution_result}
    )
    
    message = f"Action Execution Result: {execution_result['message']}"

    # Route through the Response Agent (per PRD §10 flowchart: ActionExecutor -> ResponseAgent)
    # so the raw execution result is reviewed for safety/masking before reaching the customer.
    return {
        "messages": [AIMessage(content=message)],
        "proposed_action": None, # Clear it out so we don't re-execute
        "approval_status": None,
        "active_agent": "response"
    }
