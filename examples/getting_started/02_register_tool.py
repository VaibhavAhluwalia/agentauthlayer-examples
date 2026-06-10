"""
Step 2: Register a tool.

This file shows how to mark a Python function as a tool that Agent Auth can
later discover and sync into the control plane.
"""

from __future__ import annotations

from agent_auth import register_tool


@register_tool(action="math.add", description="Add two numbers")
def add(a: float, b: float) -> float:
    return a + b


if __name__ == "__main__":
    print("Step 2, register a tool")
    print(
        {
            "tool_action": "math.add",
            "what_this_shows": [
                "how to declare a tool for Agent Auth",
                "how tool metadata is defined before sync",
            ],
            "next_step": "Sync this or another registered module into the control plane.",
            "example_call": add(2, 3),
        }
    )
