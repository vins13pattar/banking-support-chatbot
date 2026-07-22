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
        "response",
        "escalation",
    ] = Field(
        ...,
        description=(
            "The specialized agent or node to handle the user's request. "
            "Note: 'compliance' is intentionally NOT selectable here. Compliance "
            "(and human_approval / action_executor) are deterministic-handoff-only "
            "nodes reached from transaction/card AFTER a propose_* tool sets "
            "proposed_action -- never routed to directly. A request to dispute a "
            "transaction goes to 'transaction', which owns the propose_dispute tool."
        ),
    )
    reason: str = Field(
        ...,
        description="Explanation of why this agent was chosen."
    )
    confidence: float = Field(
        ...,
        description="Confidence score between 0.0 and 1.0 that this is the correct routing decision.",
        ge=0.0,
        le=1.0,
    )
