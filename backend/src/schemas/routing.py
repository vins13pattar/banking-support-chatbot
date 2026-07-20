"""Routing schemas."""

from typing import Literal
from pydantic import BaseModel, Field


class RoutingDecision(BaseModel):
    """Decision from the Supervisor agent on where to route the request."""

    target_agent: Literal[
        "faq",
        "authentication",
        "account",
        "transaction",
        "card",
        "compliance",
        "response",
        "escalation",
    ] = Field(
        ...,
        description="The specialized agent or node to handle the user's request."
    )
    reason: str = Field(
        ...,
        description="Explanation of why this agent was chosen."
    )
    requires_authentication: bool = Field(
        ...,
        description="True if the request requires the user to be authenticated first (e.g., account or transaction inquiries)."
    )
    confidence: float = Field(
        ...,
        description="Confidence score between 0.0 and 1.0 that this is the correct routing decision.",
        ge=0.0,
        le=1.0,
    )
