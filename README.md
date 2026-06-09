# agentauthlayer-examples

A practical examples repo for learning how to use `agentauthlayer`.

This repo is meant to help you understand:
- how to authenticate with Agent Auth
- how to create and use project tokens
- how to register tools from code
- how sync works
- how runtime authorization works

## Start here

If you are new to the library, read this first:

- [`HOW_AGENTAUTH_WORKS.md`](./HOW_AGENTAUTH_WORKS.md)

That guide explains the mental model behind:
- tokens
- sync
- agent identity
- decorators
- runtime binding

## Quickstart

### 1. Install the latest released package

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

### 4. Create a project in the UI

After login, create a project from the UI if you do not already have one.

### 5. Create a project token

Use:
- **Project Settings**
- or **Tokens**
- or the CLI:

```bash
agentauth token create --project agent-examples --name agent-examples-sdk-token --scope admin_agents --scope admin_tokens
```

### 6. Use the token

You can either export it:

```bash
export AGENT_AUTH_URL=http://127.0.0.1:8002
export AGENT_AUTH_TOKEN=YOUR_PROJECT_TOKEN
```

or store it for CLI + SDK use:

```bash
agentauth login --base-url http://127.0.0.1:8002 --token YOUR_PROJECT_TOKEN --email admin@agentauth.dev
```

### 7. Sync your example

If your local repo currently exposes the top-level example module:

```bash
agentauth sync --module simple_agent --project agent-examples
```

If you later standardize on package-style imports, use the package path instead.

---

## Example progression

## 1. Client with token

Use the client directly with a token to talk to the control plane.

File:
- `examples/getting_started/01_client_with_token.py`

## 2. Register a tool

Learn how code-defined tools are registered for sync.

File:
- `examples/getting_started/02_register_tool.py`

## 3. Happy-path runtime example

Run the basic example where:
- runtime identity is present
- project scope matches
- policy allows the expected action

File:
- `simple_agent.py`

Run:

```bash
./.venv/bin/python simple_agent.py
```

## 4. Runtime binding mismatch example

This example shows a denied path where project scope does not match execution context.

File:
- `examples/getting_started/project_scope_mismatch_demo.py`

Run:

```bash
./.venv/bin/python examples/getting_started/project_scope_mismatch_demo.py
```

---

## What this repo teaches

### Token authentication
Tokens authenticate SDK and CLI calls to the control plane.

### Sync behavior
Sync is intended to:
- create missing things
- update changed things
- skip unchanged things

### Decorator roles
- LangGraph `@tool` defines a runtime tool
- `@register_tool(...)` adds tool metadata for sync
- `@require_permission(...)` enforces runtime authorization

### Runtime identity
Runtime authorization uses more than a token alone.
It also depends on:
- execution context
- project scope
- agent identity
- policy evaluation

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

