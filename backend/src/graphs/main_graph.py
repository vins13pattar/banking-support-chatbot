"""Main LangGraph compilation."""

from langgraph.graph import StateGraph, START, END

from src.graphs.state import BankingSupportState
from src.agents.supervisor import supervisor_node, PROTECTED_AGENTS
from src.agents.authentication import authentication_node
from src.agents.faq import faq_node
from src.agents.account import account_node
from src.agents.transaction import transaction_node
from src.agents.card import card_node
from src.agents.compliance import compliance_node
from src.agents.human_approval import human_approval_node
from src.agents.action_executor import action_executor_node
from src.agents.response import response_node
from src.agents.escalation import escalation_node


DETERMINISTIC_HANDOFF_TARGETS = {
    "compliance",
    "human_approval",
    "action_executor",
    "escalation",
    "response",
}

# Every node name route_from_supervisor is allowed to dispatch to.
ROUTABLE_FROM_SUPERVISOR = PROTECTED_AGENTS | DETERMINISTIC_HANDOFF_TARGETS | {"authentication", "faq"}


def route_from_supervisor(state: BankingSupportState) -> str:
    """Route to the node the supervisor already decided on.

    supervisor_node has already applied the deterministic auth gate (see
    enforce_auth_gate in agents/supervisor.py) before returning
    active_agent, so this function only needs to dispatch to the matching
    node name -- it must NOT re-check verification itself. Because this is
    the sole conditional edge run immediately after supervisor_node (there
    is exactly one add_conditional_edges("supervisor", ...) call below), any
    state it sees was just produced by that node, so a second verification
    check here could never actually fire; it would only be dead code.
    """
    agent = state.get("active_agent")
    if agent in ROUTABLE_FROM_SUPERVISOR:
        return agent
    return END


def route_after_agent(state: BankingSupportState) -> str:
    """Route after an agent node completes.

    If the agent set active_agent to a specific deterministic next node
    (e.g. card -> compliance, compliance -> human_approval, human_approval ->
    action_executor), route DIRECTLY to that node.

    This must NOT bounce back through the supervisor: the supervisor node
    re-derives active_agent from an LLM call constrained to the
    RoutingDecision schema, which does not even include "human_approval" or
    "action_executor" as valid targets. Routing these deterministic,
    already-decided handoffs back through supervisor would silently drop
    them (the LLM would overwrite active_agent with an unrelated agent),
    breaking the entire HITL approval pipeline. Deterministic handoffs must
    be enforced by graph edges, not re-interpreted by an LLM.

    Otherwise, the agent is done and waiting for user input, so route to END.
    """
    next_agent = state.get("active_agent")
    if next_agent in DETERMINISTIC_HANDOFF_TARGETS:
        return next_agent
    # Agent is done; wait for the next user message
    return END


def route_after_authentication(state: BankingSupportState) -> str:
    """Route after authentication completes.

    If the user was successfully verified, go back to supervisor so it can
    route to the appropriate domain agent. Otherwise, end and wait for user input.
    """
    if state.get("customer_verified", False):
        return "supervisor"
    return END


# Create Graph
workflow = StateGraph(BankingSupportState)

# Add Nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("authentication", authentication_node)
workflow.add_node("faq", faq_node)
workflow.add_node("account", account_node)
workflow.add_node("transaction", transaction_node)
workflow.add_node("card", card_node)
workflow.add_node("compliance", compliance_node)
workflow.add_node("human_approval", human_approval_node)
workflow.add_node("action_executor", action_executor_node)
workflow.add_node("response", response_node)
workflow.add_node("escalation", escalation_node)

# Add Edges
workflow.add_edge(START, "supervisor")

# Routing from supervisor
workflow.add_conditional_edges(
    "supervisor",
    route_from_supervisor,
    {
        "authentication": "authentication",
        "faq": "faq",
        "account": "account",
        "transaction": "transaction",
        "card": "card",
        "compliance": "compliance",
        "human_approval": "human_approval",
        "action_executor": "action_executor",
        "response": "response",
        "escalation": "escalation",
        END: END,
    }
)

# Authentication: go back to supervisor only if verified, otherwise END (wait for user)
workflow.add_conditional_edges("authentication", route_after_authentication)

# Domain agents: END to wait for user input, unless they set active_agent for handoff
workflow.add_conditional_edges("faq", route_after_agent)
workflow.add_conditional_edges("account", route_after_agent)
workflow.add_conditional_edges("transaction", route_after_agent)
workflow.add_conditional_edges("card", route_after_agent)

# These route directly to their deterministic next node, otherwise END
workflow.add_conditional_edges("compliance", route_after_agent)
workflow.add_conditional_edges("human_approval", route_after_agent)
workflow.add_conditional_edges("action_executor", route_after_agent)
workflow.add_conditional_edges("escalation", route_after_agent)
workflow.add_edge("response", END)

# Compile
# Memory is handled externally by the LangGraph API (PostgresSaver)
graph = workflow.compile()
