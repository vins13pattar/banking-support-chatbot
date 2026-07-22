"""Transaction Agent."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.agents._shared import extract_proposed_action
from src.config import settings
from src.tools.transaction_tools import make_transaction_read_tools, propose_dispute_tool
from src.tools.support_tools import create_support_ticket_tool

PROPOSE_DISPUTE_TOOLS = {"propose_dispute"}

llm = ChatOpenAI(model=settings.llm_model, temperature=0)

TRANSACTION_PROMPT = """You are the Transaction Agent for our bank.
Your job is to help the customer check recent transactions, search for specific payments, or query declined transactions.

You have access to tools:
- get_recent_transactions
- search_transactions
- get_transaction_details
- propose_dispute (use this if the customer wants to DISPUTE a transaction, e.g. they don't recognise it, were charged twice, or an ATM withdrawal failed but they were debited)
- create_support_ticket (use this ONLY for non-dispute complaints or general issues, NOT for disputes)

Important Rules for Disputes:
Creating a transaction dispute is a SENSITIVE, high-risk action that requires compliance review and human approval.
1. When a customer wants to dispute a transaction, first confirm which transaction (using get_transaction_details or search_transactions) and collect their reason.
2. Then use the 'propose_dispute' tool. You CANNOT create the dispute ticket yourself.
3. Once you receive the proposed action, you MUST stop and let the system route it to the Compliance Agent. Tell the customer the dispute is being reviewed, NOT that it has been filed.

Other Rules:
1. If you use create_support_ticket, you must provide the customer_id and thread_id. customer_id is: {customer_id}. The current thread_id is: {thread_id}
"""

def get_transaction_agent(customer_id: str | None, thread_id: str):
    prompt = TRANSACTION_PROMPT.format(
        customer_id=customer_id or "UNKNOWN (Error: User must be authenticated)",
        thread_id=thread_id
    )
    return create_react_agent(
        model=llm,
        tools=[
            *make_transaction_read_tools(customer_id),
            propose_dispute_tool,
            create_support_ticket_tool
        ],
        prompt=SystemMessage(content=prompt)
    )

async def transaction_node(state: dict) -> dict:
    """Run the Transaction agent."""
    agent = get_transaction_agent(state.get("customer_id"), state.get("thread_id"))
    result = await agent.ainvoke(state)

    original_message_count = len(state.get("messages", []))
    new_messages = result["messages"][original_message_count:]

    # If a dispute was proposed, hand off to the Compliance Agent instead of
    # ending the turn (mirrors card_node's handling of its propose_* tools).
    found = extract_proposed_action(result["messages"], PROPOSE_DISPUTE_TOOLS)

    return {
        "messages": new_messages,
        "proposed_action": found if found is not None else state.get("proposed_action"),
        "active_agent": "compliance" if found is not None else None
    }
