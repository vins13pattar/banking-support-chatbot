"""Risk classification schema."""

from typing import Literal
from pydantic import BaseModel, Field


class RiskClassification(BaseModel):
    """Risk assessment from the Compliance Agent."""

    risk_level: Literal["low", "medium", "high", "critical"] = Field(
        ...,
        description="The assessed risk level of the proposed action."
    )
    factors: list[str] = Field(
        default_factory=list,
        description="List of risk factors identified (e.g., 'High value transaction', 'Unverified caller')."
    )
    recommendation: Literal["approve", "reject", "escalate"] = Field(
        ...,
        description="The recommended course of action based on the risk assessment."
    )
