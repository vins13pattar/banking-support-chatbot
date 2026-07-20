"""Tests for the HITL (Human In The Loop) approval node."""

import pytest
from langchain_core.messages import AIMessage

from src.graphs.state import BankingSupportState
from src.agents.human_approval import human_approval_node, create_approval_request


def test_create_approval_request():
    """Test that the approval request is formatted correctly."""
    state = BankingSupportState(
        messages=[],
        thread_id="thread_123",
        customer_id="cust_456",
        customer_verified=True,
        intent=None,
        active_agent=None,
        account_context=None,
        transaction_context=None,
        proposed_action={
            "action_type": "BLOCK_CARD",
            "summary": "Block card due to loss",
            "payload": {"card_id": "card_789"}
        },
        risk_level="medium",
        approval_status=None,
        escalation_required=False,
        escalation_reason=None,
        final_response=None,
        error_context=[]
    )
    
    req = create_approval_request(state)
    assert req["thread_id"] == "thread_123"
    assert req["action_type"] == "BLOCK_CARD"
    assert req["risk_level"] == "medium"
    assert req["proposed_payload"]["card_id"] == "card_789"


@pytest.mark.asyncio
async def test_human_approval_node_no_action():
    """Test the node behaves correctly when there is no proposed action."""
    state = {"proposed_action": None}
    
    # Should just clear active_agent
    result = await human_approval_node(state)
    assert result["active_agent"] is None


# The actual interrupt() behavior is tricky to unit test without the full graph compilation and 
# Checkpointer injected, because interrupt() raises a GraphInterrupt exception which is caught
# by the LangGraph executor. We would test the full compiled graph in integration tests.
