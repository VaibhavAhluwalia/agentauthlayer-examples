"""
Step 15: Create a runtime token with the SDK helper.

This demonstrates the clearer runtime-specific helper that binds the token to a
project and a runtime agent identity.
"""

from __future__ import annotations

from agent_auth import AuthAPIClient


if __name__ == "__main__":
    client = AuthAPIClient()

    token = client.create_runtime_token(
        project_id="agent-examples",
        agent_id="sample-sync-agent",
        name="agent-examples-runtime-token",
    )

    print("Step 15, create a runtime token")
    print(token)
    print("Derived runtime context:")
    print(client.explain_token(token["token"]))
