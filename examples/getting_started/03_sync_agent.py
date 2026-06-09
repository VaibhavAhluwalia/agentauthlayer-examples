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
    print(
        {
            "message": "This module is meant to be synced with agentauth sync.",
            "example": "agentauth sync --module examples.getting_started.03_sync_agent --project agent-examples",
            "agent_id": "basic-research-agent",
            "tools": ["docs.read"],
        }
    )
