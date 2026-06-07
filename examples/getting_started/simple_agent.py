from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent_auth import register_agent, register_tool


@register_tool(action="math.compute", description="Perform a basic math operation")
def math_compute(a: float, b: float, operator: str) -> float:
    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b
    raise ValueError(f"Unsupported operator: {operator}")


register_agent(
    agent_id="basic-math-agent",
    name="Basic Math Agent",
    owner="VaibhavAhluwalia",
    role="research_agent",
    project_id="demo-project",
    scopes=[],
)


class MathState(TypedDict):
    a: float
    b: float
    operator: str
    result: float



def run_math_tool(state: MathState) -> MathState:
    result = math_compute(state["a"], state["b"], state["operator"])
    return {
        **state,
        "result": result,
    }


builder = StateGraph(MathState)
builder.add_node("run_math_tool", run_math_tool)
builder.add_edge(START, "run_math_tool")
builder.add_edge("run_math_tool", END)

graph = builder.compile()


if __name__ == "__main__":
    sample = {
        "a": 12,
        "b": 3,
        "operator": "/",
        "result": 0,
    }
    output = graph.invoke(sample)
    print("Basic Math Agent Output")
    print(output)
