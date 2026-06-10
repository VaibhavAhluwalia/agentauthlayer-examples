from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent_auth import AuthAPIClient, register_tool

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from examples._env import load_dotenv


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
    load_dotenv()
    client = AuthAPIClient(token=os.environ["AGENT_AUTH_TOKEN"])
    projects = client.list_projects()

    output = graph.invoke({
        "a": 12,
        "b": 3,
        "operator": "/",
        "result": 0,
    })

    print("Agent Auth client is connected.")
    print({
        "auth_source": client.auth_source,
        "projects": [project["project_id"] for project in projects],
    })
    print("LangGraph math output:")
    print(output)
