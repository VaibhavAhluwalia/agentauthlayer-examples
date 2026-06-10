"""
Step 11: Understand agent registration fields.

This file explains the difference between the common fields used when
registering an agent in code.
"""

from __future__ import annotations

from agent_auth import register_agent


register_agent(
    agent_id="basic-research-agent",  # stable machine identifier used for sync and lookup
    name="Basic Research Agent",      # human-readable display name shown in the UI
    owner="admin@agentauth.dev",      # owner or creator reference
    role="research_agent",            # policy role used for authorization
    scopes=["docs.read"],             # capability scopes associated with the agent
    project_id="agent-examples",      # project/workspace the agent belongs to
)


if __name__ == "__main__":
    print("Step 11, understand agent registration fields")
    print(
        {
            "agent_id": "stable machine identifier",
            "name": "human-readable display name",
            "owner": "owner or creator reference",
            "role": "policy role",
            "scopes": "capability scopes",
            "project_id": "project/workspace",
        }
    )
