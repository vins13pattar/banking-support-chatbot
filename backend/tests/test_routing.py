"""Tests for the routing logic and supervisor agent."""

from typing import get_args

import pytest
from langchain_core.messages import HumanMessage

from src.graphs.state import BankingSupportState
from src.graphs.main_graph import route_from_supervisor, route_after_agent
from src.schemas.routing import RoutingDecision


def test_supervisor_cannot_route_to_deterministic_handoff_nodes():
    """Regression: the supervisor LLM must NOT be able to route directly to
    deterministic-handoff-only nodes.

    compliance, human_approval, and action_executor are only ever entered
    as deterministic handoffs (transaction/card -> compliance ->
    human_approval -> action_executor) AFTER a propose_* tool has set
    proposed_action. If "compliance" is a selectable RoutingDecision target,
    the supervisor LLM routes a plain "raise a dispute" request straight to
    compliance, which has no proposed_action yet, so it dead-ends with a
    canned message and the dispute is never proposed or filed.
    """
    allowed = set(get_args(RoutingDecision.model_fields["target_agent"].annotation))
    for handoff_only in ("compliance", "human_approval", "action_executor"):
        assert handoff_only not in allowed, (
            f"{handoff_only} must not be a supervisor-selectable route; "
            "it is reachable only via a deterministic handoff."
        )
    # The transaction agent is what actually owns dispute requests.
    assert "transaction" in allowed


def _make_state(**overrides) -> BankingSupportState:
    base = dict(
        messages=[HumanMessage(content="hi")],
        thread_id="test_thread",
        customer_id="uuid-1234",
        customer_verified=True,
        intent=None,
        active_agent=None,
        account_context=None,
        transaction_context=None,
        proposed_action=None,
        risk_level="low",
        approval_status=None,
        escalation_required=False,
        escalation_reason=None,
        final_response=None,
        error_context=[],
    )
    base.update(overrides)
    return BankingSupportState(**base)


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
    """Test routing when supervisor decides to respond directly.

    active_agent="response" should route to the "response" node itself
    (which formats/safety-checks the final reply before its own separate
    edge to END) -- not straight to END, which would skip that node
    entirely.
    """
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
    assert route == "response"


@pytest.mark.parametrize(
    "next_agent,expected",
    [
        ("compliance", "compliance"),
        ("human_approval", "human_approval"),
        ("action_executor", "action_executor"),
        ("escalation", "escalation"),
        ("response", "response"),
    ],
)
def test_route_after_agent_goes_direct_not_through_supervisor(next_agent, expected):
    """Regression test: a deterministic handoff (e.g. card -> compliance,
    compliance -> human_approval, human_approval -> action_executor) must
    route DIRECTLY to its target node.

    It must never route back to "supervisor": supervisor_node re-derives
    active_agent via an LLM call constrained to RoutingDecision, whose
    Literal options don't even include "human_approval" or
    "action_executor". Bouncing through supervisor would silently
    overwrite the intended handoff and the graph could never actually
    reach the human-approval interrupt.
    """
    state = _make_state(active_agent=next_agent)
    route = route_after_agent(state)
    assert route == expected
    assert route != "supervisor"


def test_route_after_agent_ends_when_no_handoff():
    """When an agent finishes without proposing a handoff, wait for the user."""
    from langgraph.graph import END

    state = _make_state(active_agent=None)
    assert route_after_agent(state) == END
