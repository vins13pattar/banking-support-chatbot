"""Audit service for logging sensitive actions."""

import logging
from typing import Any
from sqlmodel import Session

from src.database import engine
from src.models.audit_event import AuditEvent

logger = logging.getLogger(__name__)


def log_audit_event(
    thread_id: str,
    actor_type: str,
    actor_id: str,
    event_type: str,
    event_payload: dict[str, Any]
) -> None:
    """Log an immutable audit event for sensitive operations.
    
    Errors are logged but never raised, so callers are not disrupted
    by audit failures.
    """
    try:
        with Session(engine) as session:
            event = AuditEvent(
                thread_id=thread_id,
                actor_type=actor_type,
                actor_id=actor_id,
                event_type=event_type,
                event_payload=event_payload
            )
            session.add(event)
            session.commit()
    except Exception:
        logger.exception("Failed to log audit event (event_type=%s, thread_id=%s)", event_type, thread_id)
