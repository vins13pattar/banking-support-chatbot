"""Customer Consent node.

Durable, structured consent gate the CUSTOMER must clear before a proposed
sensitive action (dispute, card block, card replace) is even sent to
Compliance/admin review. This sits between transaction/card's propose_*
tools and the compliance node.
"""

from langchain_core.messages import AIMessage
from langgraph.types import interrupt

from src.services.audit_service import log_audit_event


async def customer_consent_node(state: dict) -> dict:
    """Pause and ask the customer to explicitly approve or reject the
    proposed action before it proceeds to Compliance.

    The interrupt payload is shaped to match the customer-chat frontend's
    built-in Agent Inbox schema (HITLRequest: action_requests +
    review_configs) -- see frontend/customer-chat/src/components/thread/
    agent-inbox/types.ts and lib/agent-inbox-interrupt.ts. The frontend
    already renders real Approve/Reject buttons for interrupts in this shape
    and resumes the thread itself via the LangGraph SDK, so no new frontend
    component or backend endpoint is needed -- only this node.
    """
    proposed_action = state.get("proposed_action")
    if not proposed_action:
        return {"active_agent": None}

    action_type = proposed_action.get("action_type")
    summary = proposed_action.get("summary", "")
    payload = proposed_action.get("payload", {})

    consent_request = {
        "action_requests": [
            {
                "name": action_type,
                "args": payload,
                "description": (
                    f"We need your consent to proceed: {summary}. "
                    "Once you approve, this will be reviewed by our compliance "
                    "team before it is finalized."
                ),
            }
        ],
        "review_configs": [
            {
                "action_name": action_type,
                "allowed_decisions": ["approve", "reject"],
            }
        ],
    }

    response = interrupt(consent_request)

    # The Agent Inbox UI always resumes with {"decisions": [<Decision>, ...]}.
    # We only ever present a single action_request, so exactly one decision
    # comes back.
    decisions = response.get("decisions", []) if isinstance(response, dict) else []
    decision = decisions[0] if decisions else {}
    decision_type = decision.get("type")

    if decision_type == "approve":
        # Code after interrupt() only runs once per actual resume (unlike
        # code before it, which re-runs on every replay) -- see the same
        # reasoning documented in human_approval_node -- so this audit log
        # can't be duplicated by a replay.
        log_audit_event(
            thread_id=state.get("thread_id"),
            actor_type="customer",
            actor_id=str(state.get("customer_id")),
            event_type="consent_approved",
            event_payload={"action_type": action_type, "summary": summary},
        )
        return {"active_agent": "compliance"}

    # Reject (or any other/unrecognized decision): cancel the proposed action
    # before it ever reaches Compliance or the admin approval queue.
    reason = decision.get("message", "")
    log_audit_event(
        thread_id=state.get("thread_id"),
        actor_type="customer",
        actor_id=str(state.get("customer_id")),
        event_type="consent_declined",
        event_payload={"action_type": action_type, "summary": summary, "reason": reason},
    )
    message = AIMessage(
        content=(
            f"No problem, I've cancelled the request: '{summary}'."
            + (f" Reason noted: {reason}" if reason else "")
        )
    )
    return {
        "messages": [message],
        "proposed_action": None,
        "active_agent": "response",
    }
