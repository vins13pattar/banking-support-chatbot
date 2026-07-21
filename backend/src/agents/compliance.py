"""Compliance Agent."""

from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

from src.config import settings
from src.schemas.risk import RiskClassification

llm = ChatOpenAI(model=settings.llm_model, temperature=0)

COMPLIANCE_PROMPT = """You are the Compliance and Risk Assessment Agent.
A specialised agent has proposed a sensitive action that requires your review.

Your job is to analyze the proposed action and the conversation history to determine the risk level.

Proposed Action:
Type: {action_type}
Summary: {action_summary}
Payload: {action_payload}

Risk Assessment Guidelines:
1. BLOCK_CARD due to loss/theft: Medium Risk. (Needs human approval to ensure the correct card is blocked and verify identity).
2. REPLACE_CARD: High Risk. (Address verification is critical to prevent fraud).
3. CREATE_DISPUTE: Medium Risk. (Financial implication).

Review the conversation to ensure the user's intent matches the proposed action and no suspicious behavior is detected.
Provide your assessment using the requested schema.
"""

async def compliance_node(state: dict) -> dict:
    """Run the Compliance agent to assess risk of a proposed action."""
    
    proposed_action = state.get("proposed_action")
    if not proposed_action:
        return {
            "messages": [AIMessage(content="I understand you would like to handle a dispute or high-risk request. Let me assist you with that.")],
            "active_agent": None
        }
        
    system_message = COMPLIANCE_PROMPT.format(
        action_type=proposed_action.get("action_type"),
        action_summary=proposed_action.get("summary"),
        action_payload=proposed_action.get("payload")
    )
    
    messages = [SystemMessage(content=system_message)] + state["messages"]
    
    # Force structured output using RiskClassification schema
    structured_llm = llm.with_structured_output(RiskClassification)
    
    risk_assessment: RiskClassification = await structured_llm.ainvoke(messages)
    
    if risk_assessment.recommendation == "escalate":
        return {
            "risk_level": risk_assessment.risk_level,
            "escalation_required": True,
            "escalation_reason": f"Compliance escalated action {proposed_action.get('action_type')} due to factors: {', '.join(risk_assessment.factors)}",
            "active_agent": "escalation"
        }
    
    # For prototype, all 'approve' or 'reject' recommendations go to human approval for sensitive actions
    # This triggers the HITL interrupt node next
    message = f"Action '{proposed_action.get('summary')}' has been assessed as {risk_assessment.risk_level} risk. Routing for human approval."
    
    return {
        "messages": [AIMessage(content=message)],
        "risk_level": risk_assessment.risk_level,
        "active_agent": "human_approval"
    }
