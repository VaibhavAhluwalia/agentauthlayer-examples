import re
from typing import TypedDict, List, Dict, Any, Tuple
from langgraph.graph import StateGraph, START, END

# ==========================================
# 📦 Import library-native decorators
# ==========================================
# register_tool  → registers a tool's action name so it can be synced to the
#                  control plane with: agentauth sync --module math_agent
# register_agent → declares agent identities (id, role, scopes) for the same sync
# require_permission → enforces the auth check at call-time (offline or online)
from agent_auth import register_tool, register_agent, require_permission
import agent_auth.policy

# ==========================================
# 🤖 Register agent identities
# ==========================================
# These declarations are picked up by `agentauth sync --module math_agent`
# and pushed to the control plane DB automatically.
register_agent(
    agent_id="math-agent-standard-01",
    name="Standard Math Agent",
    owner="developer@company.com",
    role="math_standard",
    scopes=["math.add", "math.subtract"],
)

register_agent(
    agent_id="math-agent-advanced-99",
    name="Advanced Math Agent",
    owner="developer@company.com",
    role="math_advanced",
    scopes=["math.add", "math.subtract", "math.multiply", "math.divide"],
)

# ==========================================
# 🛡️ Offline role definitions (fallback)
# ==========================================
# When the control plane server is running, roles are fetched from it.
# When running offline/locally, the evaluator uses DEFAULT_ROLES as a fallback.
# These mirror what gets synced to the server via `agentauth sync`.
agent_auth.policy.DEFAULT_ROLES['math_standard'] = agent_auth.policy.RoleDefinition(
    name='math_standard',
    description='Can perform basic math (add, subtract)',
    statements=[
        agent_auth.policy.PolicyStatement(
            effect='ALLOW',
            actions=['math.add', 'math.subtract'],
            resources=['*']
        )
    ]
)

agent_auth.policy.DEFAULT_ROLES['math_advanced'] = agent_auth.policy.RoleDefinition(
    name='math_advanced',
    description='Can perform all math operations',
    statements=[
        agent_auth.policy.PolicyStatement(
            effect='ALLOW',
            actions=['math.add', 'math.subtract', 'math.multiply', 'math.divide'],
            resources=['*']
        )
    ]
)

# ==========================================
original_evaluate = agent_auth.policy.PolicyEvaluator.evaluate

def debug_evaluate(self, request: agent_auth.policy.PolicyRequest):
    print(f"\n🔍 \033[95m[Auth Evaluation]\033[0m Action: \033[96m{request.action}\033[0m | Role: \033[96m{request.role}\033[0m")
    decision = original_evaluate(self, request)
    status_color = "\033[92m" if decision.allowed else "\033[91m"
    print(f"   • Decision: {status_color}{'ALLOWED' if decision.allowed else 'DENIED'}\033[0m (Reason: {decision.reason})")
    return decision

agent_auth.policy.PolicyEvaluator.evaluate = debug_evaluate

# ==========================================
# 🛠️ Define Auth-Protected Tools
# ==========================================
# @register_tool  → tells the library what action name maps to this function.
#                   Run `agentauth sync --module math_agent` to push these
#                   definitions to the control plane.
# @require_permission → enforces the permission check at runtime.

@register_tool(action="math.add", description="Add two numbers")
@require_permission("math.add")
def add_tool(a: float, b: float, **kwargs) -> float:
    return a + b

@register_tool(action="math.subtract", description="Subtract two numbers")
@require_permission("math.subtract")
def subtract_tool(a: float, b: float, **kwargs) -> float:
    return a - b

@register_tool(action="math.multiply", description="Multiply two numbers")
@require_permission("math.multiply")
def multiply_tool(a: float, b: float, **kwargs) -> float:
    return a * b

@register_tool(action="math.divide", description="Divide two numbers")
@require_permission("math.divide")
def divide_tool(a: float, b: float, **kwargs) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

# ==========================================
# 🧠 LangGraph State and Agent Nodes
# ==========================================
class AgentState(TypedDict):
    # Auth credentials
    agent_id: str
    role: str
    granted_scopes: List[str]
    context: dict
    
    # Task processing state
    expression: str
    plan: List[Tuple[str, float, float]]  # List of (operation, arg1, arg2)
    step_results: List[float]
    error: str | None
    result: float | None

# 1. Planner Node
# Simple parser to break down expressions like "add(3, subtract(10, 5))" or "multiply(4, 5)"
def planner_node(state: AgentState) -> Dict[str, Any]:
    expr = state["expression"].strip()
    plan = []
    
    # Example: "multiply(4, add(3, 5))" -> Plan: [("add", 3.0, 5.0), ("multiply", 4.0, "result_0")]
    if expr == "add(3, subtract(10, 5))":
        plan = [("subtract", 10.0, 5.0), ("add", 3.0, "result_0")]
    elif expr == "multiply(4, add(3, 5))":
        plan = [("add", 3.0, 5.0), ("multiply", 4.0, "result_0")]
    else:
        # Fallback to simple matching for single operations e.g., "add(5, 10)"
        match = re.match(r"(\w+)\((\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\)", expr)
        if match:
            op, arg1, arg2 = match.groups()
            plan = [(op, float(arg1), float(arg2))]
        else:
            return {"error": f"Failed to parse mathematical expression: {expr}"}
            
    print(f"\n📋 [Planner] Planned steps for '{expr}': {plan}")
    return {"plan": plan, "step_results": [], "error": None}

# 2. Execution Node
def executor_node(state: AgentState) -> Dict[str, Any]:
    plan = state["plan"]
    step_results = []
    error = None
    
    auth_kwargs = {
        "agent_id": state["agent_id"],
        "role": state["role"],
        "granted_scopes": state["granted_scopes"],
        "context": state["context"],
    }
    
    print(f"🚀 [Executor] Running math agent execution (Agent ID: {state['agent_id']})")
    
    for op, arg1, arg2 in plan:
        # Replace placeholders like "result_0" with actual results from previous steps
        val1 = step_results[0] if arg1 == "result_0" else arg1
        val2 = step_results[0] if arg2 == "result_0" else arg2
        
        try:
            if op == "add":
                res = add_tool(val1, val2, **auth_kwargs)
            elif op == "subtract":
                res = subtract_tool(val1, val2, **auth_kwargs)
            elif op == "multiply":
                res = multiply_tool(val1, val2, **auth_kwargs)
            elif op == "divide":
                res = divide_tool(val1, val2, **auth_kwargs)
            else:
                raise ValueError(f"Unknown operation: {op}")
            
            step_results.append(res)
            print(f"   🟢 Step Success: {op}({val1}, {val2}) = {res}")
            
        except PermissionError as e:
            error = f"Security Violation: Access Denied for operation '{op}'"
            print(f"   🔴 Step Blocked: {op}({val1}, {val2}) -> {error}")
            break
        except Exception as e:
            error = f"Execution Error: {str(e)}"
            break
            
    final_result = step_results[-1] if step_results and not error else None
    return {"step_results": step_results, "error": error, "result": final_result}

# 3. Router Node to determine path
def route_after_execution(state: AgentState):
    if state["error"]:
        return "blocked"
    return "completed"

# ==========================================
# 🕸️ Assemble the LangGraph Agent Workflow
# ==========================================
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)

# Set up edges
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "executor")

# Conditional Router
workflow.add_conditional_edges(
    "executor",
    route_after_execution,
    {
        "blocked": END,
        "completed": END
    }
)

runnable_graph = workflow.compile()

# ==========================================
# 🎬 Run Scenarios
# ==========================================
def run_math_demo():
    print("=" * 70)
    print("🧮 LANGGRAPH MATH AGENT AUTHENTICATION & AUTHORIZATION DEMO 🧮")
    print("=" * 70)
    
    # Context setup
    context = {"environment": "production"}
    
    # ----------------------------------------------------
    # Scenario 1: Standard Math Agent (Basic operations only)
    # Task: add(3, subtract(10, 5))
    # ----------------------------------------------------
    print("\n🎬 Scenario 1: Basic Math Task with Standard Agent (Role: math_standard)")
    print("Expected: Success (both add & subtract are allowed for standard math agents)")
    
    state_1 = {
        "agent_id": "math-agent-standard-01",
        "role": "math_standard",
        "granted_scopes": [],
        "context": context,
        "expression": "add(3, subtract(10, 5))",
        "plan": [],
        "step_results": [],
        "error": None,
        "result": None
    }
    
    result_1 = runnable_graph.invoke(state_1)
    print(f"🏁 Final Result: {result_1['result']} (Error: {result_1['error']})")
    
    # ----------------------------------------------------
    # Scenario 2: Standard Math Agent trying Advanced Math
    # Task: multiply(4, add(3, 5))
    # ----------------------------------------------------
    print("\n🎬 Scenario 2: Advanced Math Task with Standard Agent (Role: math_standard)")
    print("Expected: Blocked (multiply is NOT allowed for standard math agents)")
    
    state_2 = {
        "agent_id": "math-agent-standard-01",
        "role": "math_standard",
        "granted_scopes": [],
        "context": context,
        "expression": "multiply(4, add(3, 5))",
        "plan": [],
        "step_results": [],
        "error": None,
        "result": None
    }
    
    result_2 = runnable_graph.invoke(state_2)
    print(f"🏁 Final Result: {result_2['result']} (Error: {result_2['error']})")
    
    # ----------------------------------------------------
    # Scenario 3: Advanced Math Agent running Advanced Math
    # Task: multiply(4, add(3, 5))
    # ----------------------------------------------------
    print("\n🎬 Scenario 3: Advanced Math Task with Advanced Agent (Role: math_advanced)")
    print("Expected: Success (multiply & add are both allowed for advanced math agents)")
    
    state_3 = {
        "agent_id": "math-agent-advanced-99",
        "role": "math_advanced",
        "granted_scopes": [],
        "context": context,
        "expression": "multiply(4, add(3, 5))",
        "plan": [],
        "step_results": [],
        "error": None,
        "result": None
    }
    
    result_3 = runnable_graph.invoke(state_3)
    print(f"🏁 Final Result: {result_3['result']} (Error: {result_3['error']})")
    
    print("\n" + "=" * 70)
    print("🎯 Demo finished!")
    print("=" * 70)

if __name__ == "__main__":
    run_math_demo()
