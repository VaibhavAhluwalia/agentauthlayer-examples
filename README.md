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

## Start here

If you are completely new, follow this order:

1. install and start the local control plane
2. log in and create your first project
3. create a project token
4. run the first client/token example
5. register and sync tools
6. run an integration example
7. read the mental model guide

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

### Step 6, run an integration example

#### `examples/integrations/langgraph_math_agent.py`
A LangGraph-style integration example.

You learn:
- how Agent Auth fits alongside a runtime tool framework
- how LangGraph tool definitions and Agent Auth decorators complement each other

### Step 7, see a runtime binding mismatch

#### `examples/getting_started/project_scope_mismatch_demo.py`
This example shows a denied path where project scope does not match execution context.

You learn:
- what a project-scope mismatch looks like
- how runtime binding can deny execution early

### Step 8, explore a workflow example

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
1. follow steps 1 through 5 first
2. then read `HOW_AGENTAUTH_WORKS.md`
3. then move into the integration and workflow examples
