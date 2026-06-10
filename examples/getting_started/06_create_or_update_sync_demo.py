from __future__ import annotations

print(
    {
        "message": "This example explains how smart sync should behave when your code-defined agent or tools already exist.",
        "expected_sync_behavior": [
            "Create missing tools or agents on first sync.",
            "Update only changed fields on later syncs.",
            "Skip unchanged tools and agents instead of recreating them.",
        ],
        "suggested_steps": [
            "Run: agentauth sync --module examples.getting_started.03_sync_agent --project agent-examples",
            "Run the same sync again and observe that unchanged items should not be recreated.",
            "Then change a field like a description, role, or scope and sync again to observe an update-only path.",
        ],
    }
)
