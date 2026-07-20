"""FastAPI routes for the custom backend."""

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from src.database import get_db
from src.models.support_ticket import SupportTicket
from src.models.audit_event import AuditEvent
from src.schemas.approval import ApprovalDecision
from src.services.approval_service import get_pending_approvals, submit_approval_decision
from src.services.ticket_service import get_ticket_status

router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "banking-chatbot-api"}


@router.get("/tickets")
def list_tickets(db: Session = Depends(get_db)):
    """List all support tickets (for Admin Dashboard)."""
    statement = select(SupportTicket).order_by(SupportTicket.created_at.desc())
    tickets = db.exec(statement).all()
    return {"tickets": tickets}


@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    """Get details of a specific ticket."""
    status = get_ticket_status(ticket_id)
    if not status:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return status


@router.get("/approvals/pending")
async def list_pending_approvals():
    """Get all pending approval requests."""
    approvals = await get_pending_approvals()
    return {"approvals": approvals}


@router.post("/approvals/{thread_id}/decision")
async def submit_decision(thread_id: str, decision: ApprovalDecision):
    """Submit an approval decision and resume the workflow."""
    result = await submit_approval_decision(thread_id, decision)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result


@router.get("/audit")
def list_audit_events(db: Session = Depends(get_db), limit: int = 50):
    """List recent audit events."""
    statement = select(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(limit)
    events = db.exec(statement).all()
    return {"events": events}


# Fake Auth for admin dashboard
@router.post("/auth/login")
def admin_login():
    """Mock login for the admin dashboard."""
    return {"token": "mock_admin_token_123", "user": {"name": "Admin User", "role": "admin"}}
