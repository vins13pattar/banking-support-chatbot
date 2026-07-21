"""Account Agent."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config import settings
from src.tools.account_tools import get_customer_accounts_tool, get_account_balance_tool

llm = ChatOpenAI(model=settings.llm_model, temperature=0)

ACCOUNT_PROMPT = """You are the Account Agent for our bank.
Your job is to help the customer with their account inquiries (balances, account status, etc.).

You have access to:
- get_customer_accounts: Call this first to see what accounts the customer has.
- get_account_balance: Use this to check the balance of a specific account using its account_id.

Important Rules:
1. Always verify the customer's intent. If they have multiple accounts, specify which account balance you are returning (using the masked account number).
2. If an account is 'frozen' or 'dormant', inform the user politely and recommend they speak to a branch representative or raise a support ticket.
3. You must provide the customer_id to your tools. The customer_id is: {customer_id}
"""

def get_account_agent(customer_id: str | None):
    prompt = ACCOUNT_PROMPT.format(customer_id=customer_id or "UNKNOWN (Error: User must be authenticated)")
    return create_react_agent(
        model=llm,
        tools=[get_customer_accounts_tool, get_account_balance_tool],
        prompt=SystemMessage(content=prompt)
    )

async def account_node(state: dict) -> dict:
    """Run the Account agent."""
    agent = get_account_agent(state.get("customer_id"))
    result = await agent.ainvoke(state)
    return {
        "messages": result["messages"][-1:],
        "active_agent": None 
    }
