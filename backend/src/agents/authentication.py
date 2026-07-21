"""Authentication Agent."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config import settings
from src.tools.customer_tools import verify_customer_tool

llm = ChatOpenAI(model=settings.llm_model, temperature=0)

AUTH_PROMPT = """You are the Authentication Agent.
The user needs to be verified before they can access sensitive account information.

To verify the user, you MUST collect:
1. Their Customer Number (e.g., CUST-1001)
2. Their Date of Birth (YYYY-MM-DD)
3. The last 4 digits of their registered phone number

Ask the user for these details. You can ask for them one at a time or all at once.
Once you have all three, use the 'verify_customer' tool.

If verification is successful, politely inform the user that they are verified and ask how you can help them today.
If verification fails, inform the user and ask them to try again.
"""

# Create the ReAct agent
auth_agent = create_react_agent(
    model=llm,
    tools=[verify_customer_tool],
    prompt=SystemMessage(content=AUTH_PROMPT)
)

async def authentication_node(state: dict) -> dict:
    """Run the authentication agent."""
    result = await auth_agent.ainvoke(state)
    
    # We need to extract verification status from the tool calls/messages
    # but for now, we'll just pass the messages back. The state will be updated
    # by the tool if we intercept it, or we can just parse the output.
    # A robust way is to look for tool messages in the result.
    
    customer_verified = state.get("customer_verified", False)
    customer_id = state.get("customer_id", None)
    
    for message in reversed(result["messages"]):
        if message.type == "tool" and message.name == "verify_customer":
            import json
            try:
                data = json.loads(message.content)
                if data.get("status") == "success":
                    customer_verified = True
                    customer_id = data.get("customer_id")
            except:
                pass
            break

    original_message_count = len(state.get("messages", []))
    new_messages = result["messages"][original_message_count:]

    return {
        "messages": new_messages,
        "customer_verified": customer_verified,
        "customer_id": customer_id,
        "active_agent": None  # reset to none to go back to supervisor on next turn
    }
