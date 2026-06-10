"""
Step 12: Run an integration example.

This file shows how a framework runtime decorator and Agent Auth decorators can
work together in the same tool definition.

It demonstrates:
- LangGraph-compatible tool definition
- Agent Auth tool registration
- Agent Auth runtime authorization
"""

from __future__ import annotations

from agent_auth import ExecutionContext, register_agent, register_tool, require_permission

try:
    from langchain_core.tools import tool
except Exception as exc:
    raise SystemExit(
        "This example requires langchain-core. Install it in your environment first."
    ) from exc


@tool
@register_tool(action="docs.read", description="Read project documents")
@require_permission("docs.read", resource="project-doc")
def read_project_doc(name: str, *, execution_context: ExecutionContext) -> str:
    return f"Reading project document: {name}"


register_agent(
    agent_id="langgraph-doc-agent",
    name="LangGraph Doc Agent",
    owner="admin@agentauth.dev",
    role="research_agent",
    scopes=["docs.read"],
    project_id="agent-examples",
)


if __name__ == "__main__":
    ctx = ExecutionContext(
        principal_id="langgraph-doc-agent",
        principal_type="agent",
        agent_id="langgraph-doc-agent",
        project_id="agent-examples",
        role="research_agent",
        scopes=["project:agent-examples"],
    )

    print("Step 12, run an integration example")
    print(
        {
            "what_this_shows": [
                "how LangGraph tool definition and Agent Auth decorators can be combined",
                "how runtime authorization still applies during integration",
            ],
            "result": read_project_doc.invoke(
                {
                    "name": "roadmap.md",
                    "execution_context": ctx,
                }
            ),
        }
    )
