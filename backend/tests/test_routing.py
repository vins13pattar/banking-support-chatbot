"""Tests for the routing logic and supervisor agent."""

import pytest
from langchain_core.messages import HumanMessage

from src.graphs.state import BankingSupportState
from src.graphs.main_graph import route_from_supervisor


def test_route_from_supervisor_unauthenticated():
    """Test that if the active_agent is set, the router respects it."""
    state = BankingSupportState(
        messages=[HumanMessage(content="What is my balance?")],
        thread_id="test_thread",
        customer_id=None,
        customer_verified=False,
        intent=None,
        active_agent="authentication",
        account_context=None,
        transaction_context=None,
        proposed_action=None,
        risk_level="low",
        approval_status=None,
        escalation_required=False,
        escalation_reason=None,
        final_response=None,
        error_context=[]
    )
    
    # The router should simply return the active_agent if it is valid
    route = route_from_supervisor(state)
    assert route == "authentication"


def test_route_from_supervisor_authenticated():
    """Test routing to account agent."""
    state = BankingSupportState(
        messages=[HumanMessage(content="What is my balance?")],
        thread_id="test_thread",
        customer_id="uuid-1234",
        customer_verified=True,
        intent=None,
        active_agent="account",
        account_context=None,
        transaction_context=None,
        proposed_action=None,
        risk_level="low",
        approval_status=None,
        escalation_required=False,
        escalation_reason=None,
        final_response=None,
        error_context=[]
    )
    
    route = route_from_supervisor(state)
    assert route == "account"


def test_route_from_supervisor_response():
    """Test routing when supervisor decides to respond directly."""
    state = BankingSupportState(
        messages=[HumanMessage(content="Hello")],
        thread_id="test_thread",
        customer_id=None,
        customer_verified=False,
        intent=None,
        active_agent="response",
        account_context=None,
        transaction_context=None,
        proposed_action=None,
        risk_level="low",
        approval_status=None,
        escalation_required=False,
        escalation_reason=None,
        final_response=None,
        error_context=[]
    )
    
    route = route_from_supervisor(state)
    from langgraph.graph import END
    assert route == END
