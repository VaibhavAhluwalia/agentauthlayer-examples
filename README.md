# agentauthlayer-examples

Practical examples for learning `agentauthlayer` from first setup to project-scoped runtime authorization.

This repo is designed to help you get to a **first successful run quickly**, then understand the mental model behind:
- tokens
- sync
- tool registration
- runtime authorization
- project-aware execution

## Who this is for

Use this repo if you want to:
- authenticate SDK and CLI calls with Agent Auth
- register tools from code
- sync agents and tools into the control plane
- use project-scoped tokens
- understand runtime authorization with simple examples

## Library links

- PyPI: <https://pypi.org/project/agentauthlayer/>

## Start here

If you are completely new, follow this order:

1. install and start the local control plane
2. log in and create your first project
3. create a project token
4. run the first client/token example
5. register and sync tools
6. understand sync behavior
7. understand permission checks
8. try token-based code usage
9. try the CLI-only path
10. run an integration example
11. read the mental model guide

---

## 5-minute first success

### 1. Install the latest release

```bash
./.venv/bin/pip install --upgrade agentauthlayer==0.1.10
```

### 2. Start the local server

```bash
./.venv/bin/agentauth up --host 0.0.0.0 --port 8002 --wait 20
```

### 3. Log in

```bash
agentauth login --base-url http://127.0.0.1:8002 --email admin@agentauth.dev --password 'YOUR_PASSWORD'
```

### 4. Create a project token

In the UI, use:
- **Project Settings**
- or **Tokens**

Or use the CLI:

```bash
agentauth token create --project agent-examples --name agent-examples-sdk-token --scope admin_agents --scope admin_tokens
```

### 5. Use the token

```bash
export AGENT_AUTH_URL=http://127.0.0.1:8002
export AGENT_AUTH_TOKEN=YOUR_PROJECT_TOKEN
```

### 6. Run the first example

```bash
./.venv/bin/python examples/getting_started/01_client_with_token.py
```

---

## Step-by-step examples

The repo is organized as a step-by-step path for learning the library.

### Step 1, connect with a token

#### `examples/getting_started/01_client_with_token.py`
Use the SDK client with a token.

You learn:
- how to authenticate the client
- how to talk to the control plane
- what a token is used for

### Step 2, register a tool

#### `examples/getting_started/02_register_tool.py`
Register a tool from code.

You learn:
- what tool registration means
- how sync discovers code-defined tools
- what metadata Agent Auth needs

### Step 3, sync your agent

#### `examples/getting_started/03_sync_agent.py`
Use the sync flow to create or update code-defined state in the control plane.

You learn:
- how sync works
- why sync should only update what changed
- how Agent Auth keeps code and control-plane state aligned

### Step 4, use token login in the CLI

#### `examples/getting_started/04_token_login_cli_flow.py`
See how token-based CLI login works in practice.

You learn:
- how to use a project token with the CLI
- how stored credentials help SDK and CLI workflows

### Step 5, rotate a project token

#### `examples/getting_started/05_project_token_rotation.py`
Learn the expected replace/revoke flow for one-time-reveal project tokens.

You learn:
- why tokens are shown once
- how to replace a lost token
- how to revoke old tokens safely

### Step 6, understand create-or-update sync

#### `examples/getting_started/06_create_or_update_sync_demo.py`
Learn how smart sync should behave when code-defined state already exists.

You learn:
- why sync should create missing items
- why sync should update only changed items
- why unchanged items should be skipped

### Step 7, see a minimal permission example

#### `examples/getting_started/07_require_permission_minimal.py`
Understand runtime authorization in the smallest useful example.

You learn:
- how `@require_permission(...)` works
- what an allowed path looks like
- what a denied path looks like

### Step 8, try the CLI-only flow

#### `examples/getting_started/08_cli_only_flow.py`
Follow the system from the CLI without needing a deeper integration first.

You learn:
- how to think about the system operationally
- how login, project, token, and sync fit together

### Step 9, understand sync no-change vs update behavior

#### `examples/getting_started/09_sync_unchanged_vs_updated.py`
A focused explanation of what smart sync should do on repeat runs.

You learn:
- first sync vs second sync behavior
- unchanged vs updated code-defined state
- why sync should be diff-based

### Step 10, use a token directly in code

#### `examples/getting_started/10_token_used_in_code.py`
Use `AuthAPIClient(token=...)` directly from Python code.

You learn:
- how token-based SDK usage looks in real code
- how to use environment variables cleanly

### Step 11, see a runtime binding mismatch

#### `examples/getting_started/project_scope_mismatch_demo.py`
This example shows a denied path where project scope does not match execution context.

You learn:
- what a project-scope mismatch looks like
- how runtime binding can deny execution early

### Step 12, run an integration example

#### `examples/integrations/12_langgraph_with_agentauth.py`
A LangGraph-style integration example showing how LangGraph and Agent Auth decorators work together.

You learn:
- how runtime tool decorators and Agent Auth decorators complement each other
- how to combine tool definition, registration, and permission checks

### Step 13, explore a workflow example

#### `examples/workflows/math_agent.py`
A slightly larger example showing a more complete flow.

---

## How to think about the library

If you want the conceptual explanation, read:

- [`HOW_AGENTAUTH_WORKS.md`](./HOW_AGENTAUTH_WORKS.md)

That guide explains:
- what the token does
- what sync does
- why there are multiple decorators
- what execution context means
- how runtime authorization works at a safe public level

---

## What each part does

### Token
Authenticates SDK and CLI calls to the control plane.

### Sync
Creates missing items, updates changed items, and skips unchanged items when possible.

### `@register_tool(...)`
Marks a tool so Agent Auth can discover and sync it.

### `@require_permission(...)`
Checks authorization before the tool runs.

### Runtime execution context
Provides project and agent context for runtime authorization.

---

## Token lifecycle

Project tokens are shown once when created.

That means:
- copy them immediately
- store them safely
- if you lose one, create a new token
- revoke the old token if needed

Old token values should not be shown again later.

---

## Keep going

If you want the easiest path:
1. follow steps 1 through 10 first
2. then read `HOW_AGENTAUTH_WORKS.md`
3. then move into the integration and workflow examples
