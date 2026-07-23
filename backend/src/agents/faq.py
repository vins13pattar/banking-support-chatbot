"""FAQ Agent."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from src.config import settings
from src.tools.knowledge_tools import search_banking_knowledge_tool, get_policy_document_tool

llm = ChatOpenAI(model=settings.llm_model, temperature=0)

FAQ_PROMPT = """You are the FAQ Agent for our bank.
Your job is to answer general questions about banking hours, policies, interest rates, and fees.

You MUST use the 'search_banking_knowledge' tool to look up information.
Do NOT make up information. If you cannot find the answer in the knowledge base, state that you do not know and offer to connect them to a human agent.

Be polite, concise, and helpful.
"""

faq_agent = create_agent(
    model=llm,
    tools=[search_banking_knowledge_tool, get_policy_document_tool],
    system_prompt=SystemMessage(content=FAQ_PROMPT)
)

async def faq_node(state: dict) -> dict:
    """Run the FAQ agent."""
    result = await faq_agent.ainvoke(state)
    original_message_count = len(state["messages"])
    new_messages = result["messages"][original_message_count:]
    return {
        "messages": new_messages,
        "active_agent": None # reset routing
    }
