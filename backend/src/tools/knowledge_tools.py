"""Knowledge base tools."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.services.knowledge_service import search_knowledge_base, get_policy_document


class SearchKnowledgeBaseInput(BaseModel):
    query: str = Field(description="The search query or keywords")
    category: str | None = Field(default=None, description="Optional category filter (general, accounts, cards, loans, fees, policies)")


@tool("search_banking_knowledge", args_schema=SearchKnowledgeBaseInput)
def search_banking_knowledge_tool(query: str, category: str | None = None) -> dict:
    """Search the bank's knowledge base for policies, FAQs, fees, and rules.
    Use this to answer general banking questions.
    """
    results = search_knowledge_base(query, category)
    if not results:
        return {"status": "error", "message": "No matching knowledge documents found."}
    
    return {"status": "success", "documents": results}


class GetPolicyDocumentInput(BaseModel):
    title: str = Field(description="The title of the policy document to retrieve")


@tool("get_policy_document", args_schema=GetPolicyDocumentInput)
def get_policy_document_tool(title: str) -> dict:
    """Retrieve a specific policy document by its exact or partial title."""
    doc = get_policy_document(title)
    if doc:
        return {"status": "success", "data": doc}
    return {"status": "error", "message": "Policy document not found."}
