"""
Step 14: Create a sync token with the SDK helper.

This demonstrates the simpler high-level helper for a token meant to be used
for sync and control-plane update flows.
"""

from __future__ import annotations

from agent_auth import AuthAPIClient


if __name__ == "__main__":
    client = AuthAPIClient()

    token = client.create_sync_token(
        project_id="agent-examples",
        name="agent-examples-sync-token",
    )

    print("Step 14, create a sync token")
    print(token)
