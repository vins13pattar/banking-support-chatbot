"""LangGraph state schema for the banking support chatbot."""

import operator
from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from typing_extensions import TypedDict


class BankingSupportState(TypedDict):
    """Shared state across all agents in the banking support graph.

    Each agent reads from and writes to specific fields it owns.
    The `messages` field uses the `add_messages` reducer to accumulate
    conversation history. The `error_context` field uses `operator.add`
    to accumulate error logs from multiple nodes.
    """

    # --- Conversation ---
    messages: Annotated[list[AnyMessage], add_messages]
    thread_id: str

    # --- Customer Context ---
    customer_id: str | None
    customer_verified: bool

    # --- Routing ---
    intent: str | None
    active_agent: str | None

    # --- Domain Context (set by specialised agents) ---
    account_context: dict | None
    transaction_context: dict | None

    # --- Action Pipeline ---
    proposed_action: dict | None
    risk_level: str  # "low" | "medium" | "high" | "critical"
    approval_status: str | None  # "pending" | "approved" | "rejected" | "modified"

    # --- Escalation ---
    escalation_required: bool
    escalation_reason: str | None

    # --- Output ---
    final_response: str | None

    # --- Error Tracking ---
    error_context: Annotated[list[str], operator.add]
