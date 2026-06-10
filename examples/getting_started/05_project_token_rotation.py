"""
Step 5: Rotate a project token.

Project tokens are shown once when created.
If you lose one, create a new token and revoke the old one.
"""

from __future__ import annotations

print("Step 5, rotate a project token")
print(
    {
        "why": "Token values are not retrievable later, so replacement should happen by create-and-revoke rather than recovery.",
        "steps": [
            "Create a new project token from Project Settings or Tokens in the UI.",
            "Copy and store the new token immediately.",
            "Use the token with: agentauth login --base-url http://127.0.0.1:8002 --token YOUR_NEW_PROJECT_TOKEN --email admin@agentauth.dev",
            "List existing tokens with: agentauth token list --subject-type system",
            "Revoke the old token with: agentauth token revoke --jti YOUR_OLD_TOKEN_JTI",
        ],
    }
)
