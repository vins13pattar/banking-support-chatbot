"""Approval service interacting with the LangGraph API."""

from datetime import datetime, timezone

import httpx
from sqlmodel import Session, select

from src.config import settings
from src.database import engine
from src.models.approval_request import ApprovalRequest
from src.schemas.approval import ApprovalDecision


class LangGraphClient:
    """Simple client for interacting with the LangGraph Agent Server."""
    
    def __init__(self):
        self.base_url = settings.langgraph_api_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    async def get_thread_state(self, thread_id: str) -> dict:
        """Get the current state of a thread."""
        response = await self.client.get(f"/threads/{thread_id}/state")
        response.raise_for_status()
        return response.json()

    async def resume_thread(self, thread_id: str, decision: ApprovalDecision) -> dict:
        """Resume a suspended thread with a decision payload.

        Both fields below are required by the server's RunCreateStateful
        schema: "assistant_id" (missing entirely before) and the lowercase
        "command" key (previously sent as "Command", which the schema does
        not recognize -- so the resume payload was silently ignored and the
        request failed schema validation with a 422 either way). Without
        this, every approve/reject decision updated the ApprovalRequest DB
        row to "approved"/"rejected" but never actually resumed the
        interrupted graph, leaving the customer's thread stuck.
        """
        payload = {
            "assistant_id": settings.langgraph_assistant_id,
            "command": {
                "resume": decision.model_dump()
            }
        }

        response = await self.client.post(
            f"/threads/{thread_id}/runs/wait",
            json=payload
        )
        response.raise_for_status()
        return response.json()


# Singleton
lg_client = LangGraphClient()


def get_or_create_pending_approval(
    thread_id: str,
    customer_id: str | None,
    action_type: str,
    action_summary: str,
    proposed_payload: dict,
    risk_level: str,
):
    """Get the existing pending approval for this thread, or persist a new one.

    This MUST be called whenever the graph interrupts for human review.
    Without a persisted row here, `get_pending_approvals` and
    `submit_approval_decision` (both of which query this table) have
    nothing to find, so the admin dashboard's pending-approvals list would
    always be empty and reviewers would have no way to discover or act on
    the request.

    Get-or-create (rather than always inserting) matters because of how
    LangGraph interrupts work: when a node calls `interrupt()`, the whole
    node function re-runs from the top on resume, so any code before the
    `interrupt()` call executes again. Without this check, resuming a
    thread would insert a second, duplicate "pending" row every time.

    Returns (record, created) so callers can tell a fresh interrupt from a
    replayed resume -- e.g. to only log an "approval_requested" audit event
    once instead of duplicating it on every resume, which has the exact
    same replay hazard this function was written to avoid for the DB row.
    """
    with Session(engine) as session:
        existing = session.exec(
            select(ApprovalRequest).where(
                ApprovalRequest.thread_id == thread_id,
                ApprovalRequest.status == "pending",
            )
        ).first()
        if existing:
            return existing, False

        record = ApprovalRequest(
            thread_id=thread_id,
            customer_id=customer_id,
            action_type=action_type,
            action_summary=action_summary,
            proposed_payload=proposed_payload,
            risk_level=risk_level,
            status="pending",
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record, True


async def get_pending_approvals() -> list[dict]:
    """Get all pending approvals.
    
    In a real system, we'd query our own DB if we synced it, or use the LangGraph API's 
    search endpoints. For this prototype, we'll return a mock list or just rely on the 
    frontend explicitly knowing the thread_id.
    Since we can't easily query all suspended threads without LangGraph Studio's internal APIs,
    we'll provide a mock or require the thread_id.
    """
    with Session(engine) as session:
        statement = select(ApprovalRequest).where(ApprovalRequest.status == "pending")
        results = session.exec(statement).all()
        
        return [
            {
                "approval_id": str(req.id),
                "thread_id": req.thread_id,
                "customer_id": str(req.customer_id),
                "action_type": req.action_type,
                "action_summary": req.action_summary,
                "risk_level": req.risk_level,
                "proposed_payload": req.proposed_payload,
                "requested_at": req.requested_at.isoformat()
            }
            for req in results
        ]


async def submit_approval_decision(thread_id: str, decision: ApprovalDecision, reviewer: str = "admin") -> dict:
    """Submit a decision and resume the LangGraph thread.

    Resume the graph BEFORE writing the decision to the DB, not after. If
    the DB write happened first and resume_thread then failed (as it did
    until the assistant_id/command payload bug above was fixed), the record
    was left permanently "approved"/"rejected" -- and therefore no longer
    "pending" -- while the actual interrupted graph never advanced and the
    customer's thread stayed stuck. That left no way to retry from the UI,
    since the pending-approvals list only shows status="pending" rows. By
    resuming first, a failure leaves the row untouched at "pending" so the
    admin can simply retry the decision.
    """
    try:
        result = await lg_client.resume_thread(thread_id, decision)
    except Exception as e:
        return {"status": "error", "message": f"Failed to resume thread: {str(e)}"}

    # Resume succeeded; now record the decision.
    with Session(engine) as session:
        statement = select(ApprovalRequest).where(
            ApprovalRequest.thread_id == thread_id,
            ApprovalRequest.status == "pending"
        )
        req = session.exec(statement).first()

        if req:
            req.status = "approved" if decision.approved else "rejected"
            if decision.approved and decision.modified_action:
                req.status = "modified"

            req.reviewer = reviewer
            req.reviewer_comment = decision.reviewer_comment
            req.reviewed_at = datetime.now(timezone.utc)
            session.add(req)
            session.commit()

    return {"status": "success", "message": "Thread resumed successfully.", "langgraph_result": result}
