"""Card-related tools."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.schemas.actions import ProposedAction


class GetCustomerCardsInput(BaseModel):
    customer_id: str = Field(description="The UUID of the verified customer")


@tool("get_customer_cards", args_schema=GetCustomerCardsInput)
def get_customer_cards_tool(customer_id: str) -> dict:
    """Get a list of all cards (debit/credit) belonging to the customer. 
    Mock implementation for prototype.
    """
    # Mock data for the prototype
    return {
        "status": "success",
        "cards": [
            {
                "card_id": f"card-{customer_id[:8]}-1",
                "card_type": "debit",
                "card_number_masked": "XXXX-XXXX-XXXX-1234",
                "status": "active"
            },
            {
                "card_id": f"card-{customer_id[:8]}-2",
                "card_type": "credit",
                "card_number_masked": "XXXX-XXXX-XXXX-9876",
                "status": "active"
            }
        ]
    }


class ProposeBlockCardInput(BaseModel):
    card_id: str = Field(description="The ID of the card to block")
    reason: str = Field(description="Reason for blocking the card (e.g., lost, stolen, fraud)")


@tool("propose_block_card", args_schema=ProposeBlockCardInput)
def propose_block_card_tool(card_id: str, reason: str) -> dict:
    """Propose blocking a card. This is a sensitive action and requires compliance review and human approval.
    Instead of executing the action, this tool returns a ProposedAction that the agent must pass to the compliance agent.
    """
    action = ProposedAction(
        action_type="BLOCK_CARD",
        summary=f"Block card {card_id} due to: {reason}",
        payload={"card_id": card_id, "reason": reason}
    )
    
    return {
        "status": "success", 
        "message": "Action proposed successfully. You MUST now pass this proposed action to the compliance agent for review.",
        "proposed_action": action.model_dump()
    }


class ProposeReplaceCardInput(BaseModel):
    card_id: str = Field(description="The ID of the card to replace")
    address: str = Field(description="The address to ship the new card to")


@tool("propose_replace_card", args_schema=ProposeReplaceCardInput)
def propose_replace_card_tool(card_id: str, address: str) -> dict:
    """Propose replacing a card. This is a sensitive action and requires compliance review and human approval."""
    action = ProposedAction(
        action_type="REPLACE_CARD",
        summary=f"Replace card {card_id} and ship to {address}",
        payload={"card_id": card_id, "address": address}
    )
    
    return {
        "status": "success", 
        "message": "Action proposed successfully. You MUST now pass this proposed action to the compliance agent for review.",
        "proposed_action": action.model_dump()
    }
