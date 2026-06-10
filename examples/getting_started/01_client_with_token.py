"""
Step 1: Connect with a token.

This is the simplest useful SDK example.
It shows how to authenticate the client with a project token and call the
control plane directly.
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

    print("Step 1, connect with a token")
    print(
        {
            "base_url": base_url,
            "what_this_shows": [
                "how to authenticate the SDK client with a token",
                "how to make a basic control-plane call",
            ],
            "projects": client.list_projects(),
        }
    )
