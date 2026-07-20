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

# Return to supervisor
workflow.add_edge("authentication", "supervisor")
workflow.add_edge("faq", "supervisor")
workflow.add_edge("account", "supervisor")
workflow.add_edge("transaction", "supervisor")
workflow.add_edge("card", "supervisor")
workflow.add_edge("compliance", "supervisor")
workflow.add_edge("human_approval", "supervisor")
workflow.add_edge("action_executor", "supervisor")
workflow.add_edge("escalation", "supervisor")
workflow.add_edge("response", END)

# Compile
# Memory is handled externally by the LangGraph API (PostgresSaver)
graph = workflow.compile()
