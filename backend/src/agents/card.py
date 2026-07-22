"""Card Agent."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.agents._shared import extract_proposed_action
from src.config import settings
from src.tools.card_tools import (
    get_customer_cards_tool,
    propose_block_card_tool,
    propose_replace_card_tool
)

PROPOSE_CARD_ACTION_TOOLS = {"propose_block_card", "propose_replace_card"}

llm = ChatOpenAI(model=settings.llm_model, temperature=0)

CARD_PROMPT = """You are the Card Agent for our bank.
Your job is to help the customer manage their debit and credit cards (viewing, blocking, replacing).

You must provide the customer_id to your tools. The customer_id is: {customer_id}

Important Rules for Sensitive Actions:
Blocking or replacing a card are SENSITIVE actions.
1. When a user asks to block or replace a card, use the 'propose_block_card' or 'propose_replace_card' tool.
2. These tools will return a 'proposed_action' dictionary.
3. You CANNOT execute the action yourself. Once you receive the 'proposed_action', you MUST stop and let the system route it to the Compliance Agent. Do not tell the user it is done, tell them it is being reviewed.
"""

def get_card_agent(customer_id: str | None):
    prompt = CARD_PROMPT.format(customer_id=customer_id or "UNKNOWN")
    return create_react_agent(
        model=llm,
        tools=[
            get_customer_cards_tool,
            propose_block_card_tool,
            propose_replace_card_tool
        ],
        prompt=SystemMessage(content=prompt)
    )

async def card_node(state: dict) -> dict:
    """Run the Card agent."""
    agent = get_card_agent(state.get("customer_id"))
    result = await agent.ainvoke(state)
    
    original_message_count = len(state.get("messages", []))
    new_messages = result["messages"][original_message_count:]

    found = extract_proposed_action(result["messages"], PROPOSE_CARD_ACTION_TOOLS)

    return {
        "messages": new_messages,
        "proposed_action": found if found is not None else state.get("proposed_action"),
        "active_agent": "compliance" if found is not None else None
    }
