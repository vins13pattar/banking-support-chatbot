"""Transaction-related tools."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.schemas.actions import ProposedAction
from src.services.transaction_service import (
    get_recent_transactions,
    get_transaction_details,
    search_transactions,
)


def make_transaction_read_tools(customer_id: str):
    """Build the read-only transaction tools bound to one authenticated customer.

    The tools deliberately do NOT accept customer_id as an LLM-supplied
    argument. Per PRD §13.7 ("Tools must not trust customer IDs generated
    by the LLM. Customer and thread ownership must be verified in
    application code"), the customer_id is closed over here from the
    graph's own authenticated state, so it can't be swapped out by a
    prompt-injected or hallucinated argument.
    """

    class GetRecentTransactionsInput(BaseModel):
        limit: int = Field(default=5, description="Number of transactions to return (max 20)")

    @tool("get_recent_transactions", args_schema=GetRecentTransactionsInput)
    def get_recent_transactions_tool(limit: int = 5) -> dict:
        """Get the most recent transactions across all of the customer's accounts."""
        safe_limit = min(limit, 20)
        txns = get_recent_transactions(customer_id, safe_limit)
        if not txns:
            return {"status": "success", "transactions": []}
        return {"status": "success", "transactions": txns}

    class SearchTransactionsInput(BaseModel):
        merchant_query: str | None = Field(default=None, description="Partial or full merchant name to search for")
        status: str | None = Field(default=None, description="Filter by status (completed, pending, failed, reversed)")

    @tool("search_transactions", args_schema=SearchTransactionsInput)
    def search_transactions_tool(merchant_query: str | None = None, status: str | None = None) -> dict:
        """Search for specific transactions by merchant name or status."""
        txns = search_transactions(customer_id, merchant_query, status)
        return {"status": "success", "transactions": txns}

    class GetTransactionDetailsInput(BaseModel):
        transaction_reference: str = Field(description="The unique transaction reference ID (e.g., TXN-1234)")

    @tool("get_transaction_details", args_schema=GetTransactionDetailsInput)
    def get_transaction_details_tool(transaction_reference: str) -> dict:
        """Get detailed information about a single transaction owned by the customer."""
        txn = get_transaction_details(transaction_reference, customer_id)
        if txn:
            return {"status": "success", "data": txn}
        return {"status": "error", "message": "Transaction not found."}

    return [get_recent_transactions_tool, search_transactions_tool, get_transaction_details_tool]


class ProposeDisputeInput(BaseModel):
    transaction_reference: str = Field(description="The transaction reference being disputed (e.g. TXN-7782)")
    reason: str = Field(description="The customer's reason for disputing the transaction")


@tool("propose_dispute", args_schema=ProposeDisputeInput)
def propose_dispute_tool(transaction_reference: str, reason: str) -> dict:
    """Propose creating a dispute for a transaction.

    Creating a dispute is a high-risk, sensitive action (PRD §7.5/§11.1): it
    must NOT be executed directly. Instead of creating a ticket, this tool
    returns a ProposedAction that the agent must pass to the compliance
    agent for risk assessment and human approval before any ticket is
    actually created.
    """
    action = ProposedAction(
        action_type="CREATE_DISPUTE",
        summary=f"Create dispute for transaction {transaction_reference}",
        payload={"transaction_reference": transaction_reference, "dispute_details": reason},
    )

    return {
        "status": "success",
        "message": "Dispute proposed successfully. You MUST now pass this proposed action to the compliance agent for review. Do not tell the customer the dispute has been filed yet.",
        "proposed_action": action.model_dump(),
    }
