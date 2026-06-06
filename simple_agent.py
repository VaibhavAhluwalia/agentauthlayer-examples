import sys
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from agent_auth import require_permission
from agent_auth.policy import PolicyEvaluator, PolicyRequest

# Intercept and print the library inputs (PolicyRequest) passed to the PolicyEvaluator
original_evaluate = PolicyEvaluator.evaluate

def debug_evaluate(self, request: PolicyRequest):
    print(f"\n🔍 \033[95m[Library Input Debug]\033[0m Intercepted PolicyRequest:")
    print(f"   • principal_id (Agent/User ID): \033[96m{request.principal_id}\033[0m")
    print(f"   • action (Required Permission): \033[96m{request.action}\033[0m")
    print(f"   • resource:                    \033[96m{request.resource}\033[0m")
    print(f"   • granted_scopes:              \033[96m{request.granted_scopes}\033[0m")
    print(f"   • role:                        \033[96m{request.role}\033[0m")
    print(f"   • context:                     \033[96m{request.context}\033[0m")
    
    decision = original_evaluate(self, request)
    
    status_color = "\033[92m" if decision.allowed else "\033[91m"
    print(f"   • SDK Decision:                {status_color}{'ALLOWED' if decision.allowed else 'DENIED'}\033[0m (Reason: {decision.reason})")
    return decision

PolicyEvaluator.evaluate = debug_evaluate


# Define the State for our LangGraph Agent
class AgentState(TypedDict):
    agent_id: str
    role: str
    granted_scopes: List[str]
    context: dict
    commands: List[str]
    messages: List[str]

# Define Authorized Tools using agentauthlayer's require_permission decorator
@require_permission("tool.search_web")
def search_web_tool(query: str, **kwargs):
    """Search the web for information. Requires 'tool.search_web' permission."""
    return f"[SUCCESS] Searched web for: '{query}'"

@require_permission("tool.send_email")
def send_email_tool(recipient: str, body: str, **kwargs):
    """Send an email notification. Requires 'tool.send_email' permission."""
    return f"[SUCCESS] Sent email to {recipient}: '{body}'"

# LangGraph Node: Tool Execution Node
def execute_tools_node(state: AgentState):
    messages = list(state.get("messages", []))
    
    # We pass the auth context parameters down to the tools so the decorator can evaluate them
    auth_kwargs = {
        "agent_id": state["agent_id"],
        "role": state["role"],
        "granted_scopes": state["granted_scopes"],
        "context": state["context"],
    }
    
    print(f"\n🔑 Running actions with Agent ID: \033[94m{state['agent_id']}\033[0m")
    print(f"   Role: \033[93m{state['role'] or 'None'}\033[0m, Scopes: \033[92m{state['granted_scopes']}\033[0m")
    
    for command in state["commands"]:
        print(f"👉 Attempting to run command: \033[1m{command}\033[0m")
        try:
            if command == "search":
                res = search_web_tool(query="LangGraph Agent Security", **auth_kwargs)
                messages.append(res)
                print(f"   🟢 {res}")
            elif command == "email":
                res = send_email_tool(recipient="admin@security.io", body="Security Audit Complete", **auth_kwargs)
                messages.append(res)
                print(f"   🟢 {res}")
            else:
                messages.append(f"[UNKNOWN] Command '{command}' not recognized")
        except PermissionError as e:
            err_msg = f"[DENIED] {e}"
            messages.append(err_msg)
            print(f"   🔴 {err_msg}")
            
    return {"messages": messages}

# Build the LangGraph Workflow
workflow = StateGraph(AgentState)
workflow.add_node("execute_tools", execute_tools_node)
workflow.add_edge(START, "execute_tools")
workflow.add_edge("execute_tools", END)
runnable_graph = workflow.compile()

def run_demo():
    print("=" * 60)
    print("🛡️  LANGGRAPH AGENT AUTHENTICATION & AUTHORIZATION DEMO 🛡️")
    print("=" * 60)
    
    # Scenario 1: A Research Agent attempting to search the web and send an email
    # Under DEFAULT_ROLES:
    # - 'research_agent' is ALLOWED to run 'tool.search_web'.
    # - 'research_agent' is NOT allowed to run 'tool.send_email'.
    print("\n🎬 Scenario 1: Research Agent (Limited permissions)")
    research_state = {
        "agent_id": "agent-research-001",
        "role": "research_agent",
        "granted_scopes": ["search_web"],
        "context": {"environment": "approved"},
        "commands": ["search", "email"],
        "messages": [],
    }
    runnable_graph.invoke(research_state)

    # Scenario 2: An Admin Agent attempting the same commands
    # Under DEFAULT_ROLES:
    # - 'admin' has '*' permissions, meaning both actions are ALLOWED.
    print("\n🎬 Scenario 2: Admin Agent (Full permissions)")
    admin_state = {
        "agent_id": "agent-admin-999",
        "role": "admin",
        "granted_scopes": [],
        "context": {"environment": "approved"},
        "commands": ["search", "email"],
        "messages": [],
    }
    runnable_graph.invoke(admin_state)
    
    print("\n" + "=" * 60)
    print("🎯 Demo execution finished successfully!")
    print("=" * 60)

if __name__ == "__main__":
    run_demo()
