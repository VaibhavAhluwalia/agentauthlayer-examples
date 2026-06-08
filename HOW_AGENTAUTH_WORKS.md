# How Agent Auth Works

This guide explains the mental model behind `agentauthlayer`.

If you were asking questions like:
- What does the token actually do?
- How does the library know which agent is running?
- Why are there multiple decorators?
- What does sync really do?

this file is the answer.

---

## 1. What Agent Auth is

Agent Auth is a library-first authentication and authorization layer for agents and tools.

It has three main parts:
- the **SDK/library** you use in code
- the **control plane** that stores agents, tools, projects, tokens, and policies
- the **UI** where you can manage and verify what exists

The source of truth starts in code, not in the UI.

---

## 2. What the token does

A token is primarily used for **authentication** to the control plane.

It answers:
- who is calling Agent Auth?
- is this caller valid?
- what scopes/project context came with the token?

Examples:
- SDK calls
- CLI calls
- sync operations
- project/token management operations

### Important
A token is not the entire runtime authorization story by itself.

It authenticates the caller, but policy and execution context still decide whether a tool/action is actually allowed.

---

## 3. What the agent identity is

Agent Auth keeps track of an agent in the control plane using an `agent_id`.

At runtime, the code still needs to know which agent is active.
That is why `ExecutionContext` exists.

An execution context can carry:
- `principal_id`
- `principal_type`
- `agent_id`
- `project_id`
- `role`
- `scopes`

That lets runtime authorization know:
- which project is active
- which agent is active
- which scopes are active

---

## 4. Why there are multiple decorators

This is one of the biggest confusion points.

### LangGraph `@tool`
This defines the runtime tool for LangGraph.

### `@register_tool(...)`
This tells Agent Auth that the function should be part of the synced tool catalog in the control plane.

### `@require_permission(...)`
This performs runtime authorization checks before the tool executes.

So the decorators have different jobs:
- LangGraph defines the tool runtime
- Agent Auth registers and authorizes it

They are complementary, not replacements for each other.

---

## 5. What sync does

Sync is how code-defined tools and agents are sent to the control plane.

The intended behavior is:
- create if missing
- update if changed
- skip if unchanged

Sync should not act like a blind duplicate creation step.

### Tool sync
Tool sync compares current code-defined tool metadata against what is already known and only pushes what changed.

### Agent sync
Agent sync compares the current code-defined agent state against the existing control-plane state and only updates changed fields.

---

## 6. What runtime binding means

Runtime binding is the execution-time link between:
- token context
- project context
- agent identity
- tool/action authorization

A strong runtime check should know:
- this token/project scope belongs to project X
- this execution context claims project X
- this agent identity is the expected one
- this tool/action is allowed by policy

If those do not match, execution should be denied.

### Example of mismatch
If execution context says:
- `project_id = agent-examples`

but scopes say:
- `project:another-project`

runtime authorization should deny it.

That mismatch path is now demonstrated in the examples repo too.

---

## 7. Token lifecycle behavior

Project tokens are shown **once** when created.

That means:
- copy them immediately
- store them safely
- if you lose them, create a new one
- revoke the old one if needed

The UI should not show old token values again later.

That is intentional and safer.

---

## 8. Recommended user flow

The simplest user flow is:

1. start the local server
2. log in
3. create a project
4. create a project token
5. sync your code-defined tools/agents
6. run your local example
7. verify in the UI

---

## 9. Summary

### Token
Used for control-plane authentication.

### Policy
Decides authorization.

### ExecutionContext
Tells runtime which agent/project/scopes are active.

### Sync
Moves code-defined tools and agents into the control plane.

### UI
Lets you manage and verify what exists.

---

If you understand those five ideas, the library becomes much easier to reason about.
