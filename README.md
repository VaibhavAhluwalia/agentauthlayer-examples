# agentauthlayer-examples

A clean examples repo for learning `agentauthlayer` step by step.

## Start here

If you are new to the library, read:

- [`HOW_AGENTAUTH_WORKS.md`](./HOW_AGENTAUTH_WORKS.md)

That file explains:
- what the token does
- what the agent identity is
- why there are multiple decorators
- what sync really does
- how runtime binding works

## Token-first usage

After creating a project in the Agent Auth UI, you can create a project token from:
- **Project Settings**
- **Tokens**
- or the CLI with `agentauth token create`

Then either export it for code:

```bash
export AGENT_AUTH_TOKEN=YOUR_PROJECT_TOKEN
export AGENT_AUTH_URL=http://127.0.0.1:8002
```

or store it for SDK + CLI use:

```bash
agentauth login --base-url http://127.0.0.1:8002 --token YOUR_PROJECT_TOKEN --email admin@agentauth.dev
```

## Recommended quickstart

1. Start the local server
2. Log in
3. Create a project
4. Create a project token
5. Sync your code-defined tools/agents
6. Run the example locally
7. Verify the result in the UI

## Start the local server

```bash
agentauth up --host 0.0.0.0 --port 8002 --wait 20
```

## Sync your example

If your local repo currently exposes the top-level module:

```bash
agentauth sync --module simple_agent --project agent-examples
```

If you later restore the packaged module structure, you may use:

```bash
agentauth sync --module examples.getting_started.simple_agent --project agent-examples
```

## Runtime identity and policy demo

This repo demonstrates both:
- a happy path where runtime identity, project scope, and policy align
- a mismatch path where project scope binding is denied

### Happy path

```bash
./.venv/bin/python simple_agent.py
```

### Mismatch path

```bash
./.venv/bin/python examples/getting_started/project_scope_mismatch_demo.py
```

## Token lifecycle

Project tokens are shown once when created.

That means:
- copy them immediately
- store them safely
- if you lose them, create a new token
- revoke the old token if needed

Old token values should not be shown again later.
