from __future__ import annotations

import os
import sys
from pathlib import Path

from agent_auth import AuthAPIClient, register_tool

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from examples._env import load_dotenv


@register_tool(action="math.compute", description="Add two numbers")
def add(a: float, b: float) -> float:
    return a + b


load_dotenv()

token = os.environ["AGENT_AUTH_TOKEN"]
client = AuthAPIClient(token=token)
projects = client.list_projects()

print("Agent Auth client is connected.")
print({
    "auth_source": client.auth_source,
    "projects": [project["project_id"] for project in projects],
})
print("Registered tool result:")
print(add(2, 3))
