"""Supervisor Agent for routing."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from src.config import settings
from src.graphs.state import BankingSupportState
from src.schemas.routing import RoutingDecision

# LLM
llm = ChatOpenAI(model=settings.llm_model, temperature=0)

SUPERVISOR_PROMPT = """You are the Supervisor Agent for a banking support chatbot.
Your job is to analyze the user's latest message and the conversation history to determine which specialized agent should handle the request.

Available Agents:
- faq: General banking questions, policy inquiries, bank hours, rates.
- authentication: Verification of customer identity (DOB, phone).
- account: Account balances, account status, types of accounts.
- transaction: Recent transactions, transaction search, declined transactions.
- card: Card management (blocking, unblocking, replacing). (Use 'card' for lost card).
- compliance: Handles ALL disputes, chargebacks, and high-risk operations.
- response: Used ONLY when you want to respond directly without routing, e.g. casual greetings or thanking the user.

Authentication Rules:
- If the user is NOT authenticated (customer_verified=False) and asks about their specific account, transactions, or cards, you MUST route them to the 'authentication' agent. Set requires_authentication=True.
- General questions (FAQ) do NOT require authentication.

Current Customer Status:
- customer_verified: {customer_verified}
- customer_id: {customer_id}
"""


async def supervisor_node(state: BankingSupportState) -> dict:
    """Determine the next agent to route to based on the state."""
    
    system_message = SUPERVISOR_PROMPT.format(
        customer_verified=state.get("customer_verified", False),
        customer_id=state.get("customer_id", "None")
    )
    
    messages = [SystemMessage(content=system_message)] + state["messages"]
    
    # Force structured output using RoutingDecision schema
    structured_llm = llm.with_structured_output(RoutingDecision)
    
    decision: RoutingDecision = await structured_llm.ainvoke(messages)
    
    # Determine the target agent
    target = decision.target_agent
    
    # Enforce authentication constraint
    if decision.requires_authentication and not state.get("customer_verified", False):
        target = "authentication"
        
    return {
        "active_agent": target,
        "intent": target, # loosely using intent as active agent for now
    }
