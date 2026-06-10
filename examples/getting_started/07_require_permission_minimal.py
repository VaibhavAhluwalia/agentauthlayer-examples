from __future__ import annotations

from agent_auth import ExecutionContext, require_permission


@require_permission("docs.read", resource="project-doc")
def read_doc(name: str, *, execution_context: ExecutionContext) -> str:
    return f"Reading {name}"


if __name__ == "__main__":
    allowed = ExecutionContext(
        principal_id="basic-research-agent",
        principal_type="agent",
        agent_id="basic-research-agent",
        project_id="agent-examples",
        role="research_agent",
        scopes=["project:agent-examples"],
    )

    print({"allowed_result": read_doc("overview.md", execution_context=allowed)})

    denied = ExecutionContext(
        principal_id="basic-research-agent",
        principal_type="agent",
        agent_id="basic-research-agent",
        project_id="agent-examples",
        role="research_agent",
        scopes=["project:another-project"],
    )

    try:
        read_doc("overview.md", execution_context=denied)
    except PermissionError as exc:
        print({"denied_reason": str(exc)})
