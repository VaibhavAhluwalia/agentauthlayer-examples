"""
Step 10: Use a token directly in code.

This file shows the simplest useful Python example where a project token is
used directly with AuthAPIClient.
"""

from __future__ import annotations

import os

from agent_auth.client import AuthAPIClient


if __name__ == "__main__":
    base_url = os.getenv("AGENT_AUTH_URL", "http://127.0.0.1:8002")
    token = os.getenv("AGENT_AUTH_TOKEN")

    if not token:
        raise SystemExit(
            "Set AGENT_AUTH_TOKEN first. Example: export AGENT_AUTH_TOKEN=YOUR_PROJECT_TOKEN"
        )

    client = AuthAPIClient(base_url=base_url, token=token)

    print("Step 10, use a token directly in code")
    print(
        {
            "base_url": base_url,
            "auth_source": "explicit_token",
            "what_this_shows": [
                "how to construct AuthAPIClient with a token",
                "how to read project-aware state from the control plane",
            ],
            "projects": client.list_projects(),
            "tokens": client.list_tokens("system"),
        }
    )
