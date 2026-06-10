from __future__ import annotations

import os
import sys
from pathlib import Path

from agent_auth import AuthAPIClient, require_permission

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from examples._env import load_dotenv


@require_permission("payments.refund")
def refund_payment(payment_id: str, amount: float, **auth_context) -> dict[str, object]:
    return {
        "payment_id": payment_id,
        "amount": amount,
        "status": "refunded",
    }


if __name__ == "__main__":
    load_dotenv()
    client = AuthAPIClient(token=os.environ["AGENT_AUTH_TOKEN"])
    projects = client.list_projects()

    print("Agent Auth client is connected.")
    print({
        "auth_source": client.auth_source,
        "projects": [project["project_id"] for project in projects],
    })

    try:
        refund_payment(
            "pay_demo_123",
            25.0,
            agent_id="billing-agent",
            role="research_agent",
            granted_scopes=[],
        )
    except PermissionError as exc:
        print("Permission check blocked the tool call.")
        print(str(exc))
