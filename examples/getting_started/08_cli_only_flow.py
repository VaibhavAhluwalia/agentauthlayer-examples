"""
Step 8: Try the CLI-only flow.

This file explains the system from an operational CLI-first point of view,
without requiring a deeper integration first.
"""

from __future__ import annotations

print("Step 8, try the CLI-only flow")
print(
    {
        "message": "This path helps you understand login, project, token, and sync from the CLI before writing deeper application code.",
        "steps": [
            "Start the server: agentauth up --host 0.0.0.0 --port 8002 --wait 20",
            "Log in: agentauth login --base-url http://127.0.0.1:8002 --email admin@agentauth.dev --password 'YOUR_PASSWORD'",
            "Create a project from the UI or CLI.",
            "Create a project token: agentauth token create --project agent-examples --name agent-examples-sdk-token --scope admin_agents --scope admin_tokens",
            "Sync your module: agentauth sync --module examples.getting_started.03_sync_agent --project agent-examples",
            "List tokens: agentauth token list --subject-type system",
        ],
    }
)
