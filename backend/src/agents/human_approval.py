"""Human in the loop approval node."""

from langgraph.types import interrupt
from langchain_core.messages import AIMessage

from src.services.audit_service import log_audit_event
from src.services.approval_service import get_or_create_pending_approval


def create_approval_request(state: dict, approval_id: str | None = None) -> dict:
    """Helper to format the approval request for the frontend."""
    return {
        "approval_id": approval_id or state.get("thread_id"),
        "thread_id": state.get("thread_id"),
        "customer_id": state.get("customer_id"),
        "action_type": state.get("proposed_action", {}).get("action_type"),
        "action_summary": state.get("proposed_action", {}).get("summary"),
        "risk_level": state.get("risk_level"),
        "proposed_payload": state.get("proposed_action", {}).get("payload", {})
    }


async def human_approval_node(state: dict) -> dict:
    """Pause execution and request human approval for sensitive actions.
    
    This node uses langgraph.types.interrupt to pause the graph.
    The frontend (admin dashboard) will resume the graph with the human's decision.
    """
    
    proposed_action = state.get("proposed_action")
    if not proposed_action:
        return {"active_agent": None}

    # Persist the pending approval so the admin dashboard can list and act on
    # it (get_or_create is idempotent across the node's re-run-on-resume).
    record = get_or_create_pending_approval(
        thread_id=state.get("thread_id"),
        customer_id=state.get("customer_id"),
        action_type=proposed_action.get("action_type"),
        action_summary=proposed_action.get("summary"),
        proposed_payload=proposed_action.get("payload", {}),
        risk_level=state.get("risk_level"),
    )

    # Format the request to send to the UI
    approval_request = create_approval_request(state, approval_id=str(record.id))

    # Notify user that we are waiting for human approval
    # Note: In a real app we might not send this to the LLM context directly,
    # but we'll add it to messages so the UI can show it to the user.
    # Actually, it's better if the frontend handles the "waiting" state visually,
    # but we can return a message.

    # Log that approval was requested
    log_audit_event(
        thread_id=state.get("thread_id"),
        actor_type="system",
        actor_id="compliance_agent",
        event_type="approval_requested",
        event_payload=approval_request
    )
    
    # Suspend execution here!
    # The graph will wait until resumed with a decision payload
    # Expected resume payload matches ApprovalDecision schema
    decision = interrupt(approval_request)
    
    # Execution resumes here once a human reviews
    approved = decision.get("approved", False)
    comment = decision.get("reviewer_comment", "")
    modified_action = decision.get("modified_action")
    
    status = "approved" if approved else "rejected"
    if approved and modified_action:
        status = "modified"
        
    # Log the decision
    log_audit_event(
        thread_id=state.get("thread_id"),
        actor_type="reviewer",
        actor_id="admin_user", # mock human user
        event_type=f"approval_{status}",
        event_payload=decision
    )
    
    # If rejected, clear the proposed action and route through the Response
    # Agent (per PRD §10 flowchart: HITLInterrupt -Rejected-> ResponseAgent)
    if not approved:
        reject_msg = AIMessage(content=f"The proposed action '{proposed_action.get('summary')}' was REJECTED by human review. Reason: {comment}")
        return {
            "messages": [reject_msg],
            "approval_status": "rejected",
            "proposed_action": None,
            "active_agent": "response"
        }
        
    # If approved (or modified), go to action execution
    final_action = proposed_action
    if status == "modified":
        final_action["payload"] = modified_action
        
    approve_msg = AIMessage(content=f"The proposed action '{final_action.get('summary')}' was APPROVED. Executing now...")
    
    return {
        "messages": [approve_msg],
        "approval_status": status,
        "proposed_action": final_action,
        "active_agent": "action_executor"
    }
