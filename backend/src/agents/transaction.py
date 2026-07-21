"""Transaction Agent."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config import settings
from src.tools.transaction_tools import (
    get_recent_transactions_tool,
    search_transactions_tool,
    get_transaction_details_tool,
)
from src.tools.support_tools import create_support_ticket_tool

llm = ChatOpenAI(model=settings.llm_model, temperature=0)

TRANSACTION_PROMPT = """You are the Transaction Agent for our bank.
Your job is to help the customer check recent transactions, search for specific payments, or query declined transactions.

You have access to tools:
- get_recent_transactions
- search_transactions
- get_transaction_details
- create_support_ticket (use this if the user wants to dispute a transaction or complains about a failed transaction)

Important Rules:
1. You must provide the customer_id to your tools. The customer_id is: {customer_id}
2. The current thread_id for creating tickets is: {thread_id}
3. If a customer wants to DISPUTE a transaction, you can create a support ticket with category='dispute' and provide them the ticket ID. Note: For a real dispute workflow, the compliance agent would handle it, but for simple inquiries, you can create the ticket.
"""

def get_transaction_agent(customer_id: str | None, thread_id: str):
    prompt = TRANSACTION_PROMPT.format(
        customer_id=customer_id or "UNKNOWN (Error: User must be authenticated)",
        thread_id=thread_id
    )
    return create_react_agent(
        model=llm,
        tools=[
            get_recent_transactions_tool,
            search_transactions_tool,
            get_transaction_details_tool,
            create_support_ticket_tool
        ],
        prompt=SystemMessage(content=prompt)
    )

async def transaction_node(state: dict) -> dict:
    """Run the Transaction agent."""
    agent = get_transaction_agent(state.get("customer_id"), state.get("thread_id"))
    result = await agent.ainvoke(state)
    return {
        "messages": result["messages"][-1:],
        "active_agent": None 
    }
