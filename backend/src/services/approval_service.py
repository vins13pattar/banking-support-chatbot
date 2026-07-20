"""Approval service interacting with the LangGraph API."""

import httpx
from src.config import settings
from src.schemas.approval import ApprovalDecision
from src.services.audit_service import log_audit_event


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
        """Resume a suspended thread with a decision payload."""
        # LangGraph resume takes the payload directly
        payload = {
            "Command": {
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


async def get_pending_approvals() -> list[dict]:
    """Get all pending approvals.
    
    In a real system, we'd query our own DB if we synced it, or use the LangGraph API's 
    search endpoints. For this prototype, we'll return a mock list or just rely on the 
    frontend explicitly knowing the thread_id.
    Since we can't easily query all suspended threads without LangGraph Studio's internal APIs,
    we'll provide a mock or require the thread_id.
    """
    # Placeholder for prototype: the real app would persist approval requests in the ApprovalRequest DB table
    # Let's query the DB for pending ones!
    from sqlmodel import Session, select
    from src.database import engine
    from src.models.approval_request import ApprovalRequest
    
    with Session(engine) as session:
        # Get from DB instead of LangGraph directly
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
    """Submit a decision and resume the LangGraph thread."""
    
    # 1. Update the DB record
    from sqlmodel import Session, select
    from src.database import engine
    from src.models.approval_request import ApprovalRequest
    from datetime import datetime, timezone
    
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
    
    # 2. Resume the LangGraph thread
    try:
        result = await lg_client.resume_thread(thread_id, decision)
        return {"status": "success", "message": "Thread resumed successfully.", "langgraph_result": result}
    except Exception as e:
        return {"status": "error", "message": f"Failed to resume thread: {str(e)}"}
