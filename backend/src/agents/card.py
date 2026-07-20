"""Card Agent."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config import settings
from src.tools.card_tools import (
    get_customer_cards_tool,
    propose_block_card_tool,
    propose_replace_card_tool
)

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
        state_modifier=SystemMessage(content=prompt)
    )

async def card_node(state: dict) -> dict:
    """Run the Card agent."""
    agent = get_card_agent(state.get("customer_id"))
    result = await agent.ainvoke(state)
    
    # Check if a proposed action was generated
    proposed_action = state.get("proposed_action")
    active_agent = None
    
    for message in reversed(result["messages"]):
        if message.type == "tool" and message.name in ["propose_block_card", "propose_replace_card"]:
            import json
            try:
                data = json.loads(message.content)
                if "proposed_action" in data:
                    proposed_action = data["proposed_action"]
                    active_agent = "compliance" # Force route to compliance
            except:
                pass
            break
            
    return {
        "messages": result["messages"][-1:],
        "proposed_action": proposed_action,
        "active_agent": active_agent
    }
