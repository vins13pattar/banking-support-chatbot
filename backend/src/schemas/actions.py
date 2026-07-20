"""Action schemas."""

from typing import Any
from pydantic import BaseModel, Field


class ProposedAction(BaseModel):
    """A sensitive action proposed by an agent that requires compliance review or human approval."""

    action_type: str = Field(
        ...,
        description="The identifier of the tool or action to execute (e.g., 'create_dispute_ticket', 'block_card')."
    )
    summary: str = Field(
        ...,
        description="A human-readable summary of the action being proposed."
    )
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="The arguments or payload required to execute the action."
    )
