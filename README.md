# agentauthlayer-examples

A clean examples repo for learning `agentauthlayer` step by step.

## Start here

If you are trying this library for the first time, follow this order:

1. set up the repo
2. start Agent Auth locally
3. create the first admin password
4. create a project
5. sync the getting-started example agent
6. verify the agent and tool in the UI
7. then run the local LangGraph example

---

## Repo structure

```text
agentauthlayer-examples/
  examples/
    getting_started/
      simple_agent.py
    workflows/
      math_agent.py
  README.md
  requirements.txt
```

### Start with
- `examples/getting_started/simple_agent.py`

That file is the simplest first example.

---

## What the getting-started example shows

The getting-started example demonstrates:
- one registered tool
- one registered agent
- one small LangGraph workflow
- one sync command to make the tool and agent appear in the UI

---

## 1. Setup the repo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Start Agent Auth locally

```bash
agentauth up --host 0.0.0.0 --port 8002
```

Then open:

```text
http://127.0.0.1:8002
```

If this is your first time:
- create the first super admin password
- log in
- create a project named `agent-examples`

---

## 3. Optional CLI project setup

You can also use the CLI for project setup:

```bash
agentauth project list
agentauth project create --project-id agent-examples --name "Agent Examples"
```

---

## 4. Sync the getting-started example first

```bash
agentauth login --base-url http://127.0.0.1:8002
agentauth sync --module examples.getting_started.simple_agent --project agent-examples
```

After sync, the UI should show:
- agent: `basic-math-agent`
- tool: `math.compute`

This is the first thing to verify.

---

## 5. Then run the local example

```bash
python examples/getting_started/simple_agent.py
```

Expected result:
- the LangGraph workflow runs one node
- that node calls the math tool
- the script prints the final result

---

## Workflow example

A more involved math example is kept separately in:

```text
examples/workflows/math_agent.py
```

That keeps the first-step developer experience simple, while still leaving room for richer examples later.
