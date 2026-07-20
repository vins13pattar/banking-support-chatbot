"""Transaction-related tools."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.services.transaction_service import (
    get_recent_transactions,
    get_transaction_details,
    search_transactions,
)


class GetRecentTransactionsInput(BaseModel):
    customer_id: str = Field(description="The UUID of the verified customer")
    limit: int = Field(default=5, description="Number of transactions to return (max 20)")


@tool("get_recent_transactions", args_schema=GetRecentTransactionsInput)
def get_recent_transactions_tool(customer_id: str, limit: int = 5) -> dict:
    """Get the most recent transactions across all of the customer's accounts."""
    # Cap limit
    safe_limit = min(limit, 20)
    txns = get_recent_transactions(customer_id, safe_limit)
    if not txns:
        return {"status": "success", "transactions": []}
    
    return {"status": "success", "transactions": txns}


class SearchTransactionsInput(BaseModel):
    customer_id: str = Field(description="The UUID of the verified customer")
    merchant_query: str | None = Field(default=None, description="Partial or full merchant name to search for")
    status: str | None = Field(default=None, description="Filter by status (completed, pending, failed, reversed)")


@tool("search_transactions", args_schema=SearchTransactionsInput)
def search_transactions_tool(customer_id: str, merchant_query: str | None = None, status: str | None = None) -> dict:
    """Search for specific transactions by merchant name or status."""
    txns = search_transactions(customer_id, merchant_query, status)
    return {"status": "success", "transactions": txns}


class GetTransactionDetailsInput(BaseModel):
    transaction_reference: str = Field(description="The unique transaction reference ID (e.g., TXN-1234)")


@tool("get_transaction_details", args_schema=GetTransactionDetailsInput)
def get_transaction_details_tool(transaction_reference: str) -> dict:
    """Get detailed information about a single transaction."""
    txn = get_transaction_details(transaction_reference)
    if txn:
        return {"status": "success", "data": txn}
    return {"status": "error", "message": "Transaction not found."}
