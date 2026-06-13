"""
Step 16: Create an automation token with the SDK helper.

This demonstrates the helper intended for CI, scripts, and automation jobs.
"""

from __future__ import annotations

from agent_auth import AuthAPIClient


if __name__ == "__main__":
    client = AuthAPIClient()

    token = client.create_automation_token(
        project_id="agent-examples",
        name="agent-examples-automation-token",
    )

    print("Step 16, create an automation token")
    print(token)
