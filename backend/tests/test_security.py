"""Security tests to prevent prompt injection and unauthorized access.

These test enforce_auth_gate directly -- the actual security boundary --
rather than route_from_supervisor. route_from_supervisor only ever runs
immediately after supervisor_node, which has already applied
enforce_auth_gate before returning; testing the edge function with
hand-crafted "should never happen" state (a protected agent paired with
customer_verified=False) doesn't exercise a real code path.
"""

from src.agents.supervisor import enforce_auth_gate


def test_enforce_auth_gate_blocks_unverified_protected_access():
    """A prompt-injection attempt that tricks the LLM into choosing a
    protected agent (e.g. "account") must still be redirected to
    authentication when the customer isn't verified -- regardless of
    what the LLM itself believes about whether auth is required.
    """
    assert enforce_auth_gate("account", customer_verified=False) == "authentication"


def test_enforce_auth_gate_allows_verified_access():
    """A verified customer reaches the protected agent normally."""
    assert enforce_auth_gate("account", customer_verified=True) == "account"


def test_enforce_auth_gate_passes_through_unprotected_agents():
    """Non-protected agents (faq, response, ...) are never redirected,
    verified or not."""
    assert enforce_auth_gate("faq", customer_verified=False) == "faq"
