"""
Step 4: Use token login in the CLI.

This file explains the token-based CLI login flow.
Use this after you create a project token from the UI.
"""

from __future__ import annotations

print("Step 4, use token login in the CLI")
print(
    {
        "why": "Use a project token so CLI and SDK calls can authenticate without password login each time.",
        "steps": [
            "Create a project token from Project Settings or Tokens in the UI.",
            "Run: agentauth login --base-url http://127.0.0.1:8002 --token YOUR_PROJECT_TOKEN --email admin@agentauth.dev",
            "After that, AuthAPIClient() and other CLI commands can reuse the stored credentials.",
        ],
    }
)
