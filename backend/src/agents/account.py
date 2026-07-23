"""Account Agent."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from src.config import settings
from src.tools.account_tools import make_account_tools

llm = ChatOpenAI(model=settings.llm_model, temperature=0)

ACCOUNT_PROMPT = """You are the Account Agent for our bank.
Your job is to help the customer with their account inquiries (balances, account status, etc.).

You have access to:
- get_customer_accounts: Call this first to see what accounts the customer has.
- get_account_balance: Use this to check the balance of a specific account using its account_id.

Important Rules:
1. Always verify the customer's intent. If they have multiple accounts, specify which account balance you are returning (using the masked account number).
2. If an account is 'frozen' or 'dormant', inform the user politely and recommend they speak to a branch representative or raise a support ticket.
"""

def get_account_agent(customer_id: str | None):
    return create_agent(
        model=llm,
        tools=make_account_tools(customer_id),
        system_prompt=SystemMessage(content=ACCOUNT_PROMPT)
    )

async def account_node(state: dict) -> dict:
    """Run the Account agent."""
    agent = get_account_agent(state.get("customer_id"))
    result = await agent.ainvoke(state)
    
    original_message_count = len(state.get("messages", []))
    new_messages = result["messages"][original_message_count:]
    
    return {
        "messages": new_messages,
        "active_agent": None
    }
