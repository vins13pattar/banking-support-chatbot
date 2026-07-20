"""Response Agent."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from src.config import settings
from src.schemas.responses import AgentResponse

llm = ChatOpenAI(model=settings.llm_model, temperature=0)

RESPONSE_PROMPT = """You are the final Response and Safety Agent for our bank.
The user's query has been processed by other agents, or the supervisor routed to you for a direct response.

Review the conversation history and craft a polite, professional final response.
Ensure no sensitive data (like unmasked account numbers, full phone numbers, or passwords) is included in your response.

Keep the response concise and helpful. Do not repeat internal system messages (like 'Action executed successfully'), instead translate them into a customer-friendly message.
"""

async def response_node(state: dict) -> dict:
    """Run the Response agent to format the final output."""
    
    system_message = SystemMessage(content=RESPONSE_PROMPT)
    messages = [system_message] + state["messages"]
    
    # We could use structured output if we want citations, but for now we just want a string
    response = await llm.ainvoke(messages)
    
    # This node is terminal, so we don't set active_agent.
    # We could also use this node to update final_response state if needed.
    return {
        "messages": [response],
        "active_agent": None,
        "final_response": response.content
    }
