"""Approval schemas for API and State."""

from typing import Any
from pydantic import BaseModel, Field


class ApprovalRequestSchema(BaseModel):
    """Schema for presenting an approval request via API."""
    approval_id: str
    thread_id: str
    customer_id: str
    action_type: str
    action_summary: str
    risk_level: str
    proposed_payload: dict[str, Any]


class ApprovalDecision(BaseModel):
    """Decision submitted by a human reviewer via API."""
    approved: bool = Field(..., description="True if approved, False if rejected or modified.")
    reviewer_comment: str = Field(default="", description="Optional comment from the reviewer.")
    modified_action: dict[str, Any] | None = Field(
        default=None, 
        description="Optional modified action payload if the reviewer chose to modify instead of purely approve/reject."
    )
