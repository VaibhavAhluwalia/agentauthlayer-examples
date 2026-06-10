from __future__ import annotations

print(
    {
        "message": "This example explains the expected behavior of smart sync when you run it multiple times.",
        "first_sync": "Create missing tools and agents.",
        "second_sync": "Skip unchanged tools and agents instead of recreating them.",
        "after_code_change": "Update only the fields or tool definitions that changed.",
        "try_this": [
            "Run: agentauth sync --module examples.getting_started.03_sync_agent --project agent-examples",
            "Run the same command again to observe the unchanged path.",
            "Change a field such as a role, scope, or description, then sync again to observe an update path.",
        ],
    }
)
