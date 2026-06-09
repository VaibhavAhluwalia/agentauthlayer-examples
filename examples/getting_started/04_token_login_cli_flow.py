from __future__ import annotations

print(
    {
        "message": "Use a project token to authenticate the CLI and SDK without password login.",
        "steps": [
            "Create a project token from Project Settings or Tokens in the UI.",
            "Run: agentauth login --base-url http://127.0.0.1:8002 --token YOUR_PROJECT_TOKEN --email admin@agentauth.dev",
            "After that, AuthAPIClient() and other CLI commands can reuse the stored credentials.",
        ],
    }
)
