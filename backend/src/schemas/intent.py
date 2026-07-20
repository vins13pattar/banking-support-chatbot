"""Intent classification schema."""

from typing import Literal
from pydantic import BaseModel, Field


class IntentClassification(BaseModel):
    """Classification of the user's underlying intent."""

    intent: Literal[
        "general_inquiry",
        "account_inquiry",
        "transaction_inquiry",
        "card_management",
        "dispute",
        "complaint",
        "unknown",
    ] = Field(
        ...,
        description="The broad category of the user's request."
    )
    sub_intent: str = Field(
        ...,
        description="A more specific description of the intent (e.g., 'check_balance', 'report_lost_card')."
    )
    confidence: float = Field(
        ...,
        description="Confidence score between 0.0 and 1.0.",
        ge=0.0,
        le=1.0,
    )
