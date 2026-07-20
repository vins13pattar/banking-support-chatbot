"""Agent response schemas."""

from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    """Structured response from specialized agents to the Response Agent."""

    response_text: str = Field(
        ...,
        description="The draft response to be sent to the user."
    )
    citations: list[str] = Field(
        default_factory=list,
        description="List of knowledge base document titles or source IDs used to formulate the response."
    )
    pending_actions: list[str] = Field(
        default_factory=list,
        description="List of actions that are pending approval or execution."
    )
