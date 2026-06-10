"""
Step 3: Sync your agent.

This file explains what should be synced from code into the control plane.
Use it with:

    agentauth sync --module examples.getting_started.03_sync_agent --project agent-examples

Expected behavior:
- first sync should create missing state
- later syncs should update only changed state
- unchanged state should be skipped
"""

from __future__ import annotations

from agent_auth import register_agent, register_tool, require_permission


@register_tool(action="docs.read", description="Read project docs")
@require_permission("docs.read", resource="project-doc")
def read_project_doc(document_name: str) -> str:
    return f"Reading document: {document_name}"


register_agent(
    agent_id="basic-research-agent",
    name="Basic Research Agent",
    owner="admin@agentauth.dev",
    role="research_agent",
    scopes=["docs.read"],
    project_id="agent-examples",
)


if __name__ == "__main__":
    print("Step 3, sync your agent")
    print(
        {
            "module": "examples.getting_started.03_sync_agent",
            "agent_id": "basic-research-agent",
            "tools": ["docs.read"],
            "how_to_run": "agentauth sync --module examples.getting_started.03_sync_agent --project agent-examples",
        }
    )
