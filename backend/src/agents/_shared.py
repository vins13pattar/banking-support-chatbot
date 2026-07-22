"""Helpers shared across multiple agent nodes."""

import json
from collections.abc import Sequence

from langchain_core.messages import BaseMessage


def extract_proposed_action(messages: Sequence[BaseMessage], tool_names: set[str]) -> dict | None:
    """Find the most recent tool result from one of `tool_names` and return
    its "proposed_action" payload, or None if no such result exists.

    Used by any agent (card, transaction, ...) that hands a sensitive action
    off to the Compliance Agent via a propose_* tool: the caller should set
    active_agent to "compliance" only when this returns non-None.
    """
    for message in reversed(messages):
        if message.type == "tool" and message.name in tool_names:
            try:
                data = json.loads(message.content)
            except (TypeError, ValueError):
                return None
            return data.get("proposed_action")
    return None
