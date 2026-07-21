"""Main LangGraph compilation."""

from langgraph.graph import StateGraph, START, END

from src.graphs.state import BankingSupportState
from src.agents.supervisor import supervisor_node
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


def route_from_supervisor(state: BankingSupportState) -> str:
    """Route to the appropriate agent based on the supervisor's decision."""
    agent = state.get("active_agent")
    if not agent:
        return END

    if agent == "response":
        return "response"

    if agent == "escalation":
        return "escalation"

    if agent == "human_approval":
        return "human_approval"

    if agent == "action_executor":
        return "action_executor"

    if agent == "compliance":
        return "compliance"

    valid_agents = ["authentication", "faq", "account", "transaction", "card"]
    if agent in valid_agents:
        return agent

    return END


def route_after_agent(state: BankingSupportState) -> str:
    """Route after an agent node completes.

    If the agent set active_agent to a specific next node (e.g. card -> compliance),
    route to supervisor to handle it. Otherwise, the agent is done and
    waiting for user input, so route to END.
    """
    next_agent = state.get("active_agent")
    if next_agent:
        # Agent wants to hand off to another agent (e.g. card -> compliance)
        return "supervisor"
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

# These always route back to supervisor for next decision
workflow.add_edge("compliance", "supervisor")
workflow.add_edge("human_approval", "supervisor")
workflow.add_edge("action_executor", "supervisor")
workflow.add_edge("escalation", "supervisor")
workflow.add_edge("response", END)

# Compile
# Memory is handled externally by the LangGraph API (PostgresSaver)
graph = workflow.compile()
