# How Agent Auth Works

This guide explains the user-facing mental model behind `agentauthlayer`.

It answers common questions like:
- What is the token used for?
- What does sync do?
- Why are there multiple decorators?
- How does runtime authorization work?

---

## 1. What Agent Auth does

Agent Auth helps you:
- authenticate SDK and CLI calls
- register tools and agents from code
- sync those definitions to a control plane
- enforce authorization rules at runtime

You define tools and agents in code, and Agent Auth helps manage and authorize them.

---

## 2. What the token is used for

A token is mainly used to authenticate calls to the control plane.

That includes things like:
- SDK requests
- CLI requests
- sync operations
- token and project management actions

A token proves that the caller is valid.

### Important
A token alone is not the full runtime authorization story.
Runtime authorization also depends on execution context and policy.

---

## 3. What sync does

Sync sends your code-defined tools and agents to the control plane.

The intended behavior is:
- create missing items
- update changed items
- skip unchanged items

That means sync should not feel like duplicate recreation every time.

---

## 4. Why there are multiple decorators

Different decorators do different jobs.

### LangGraph `@tool`
Defines the runtime tool for LangGraph.

### `@register_tool(...)`
Marks the tool so it can be discovered and synced into Agent Auth.

### `@require_permission(...)`
Checks authorization before the tool runs.

So the runtime tool decorator and the Agent Auth decorators are complementary.

---

## 5. What runtime authorization uses

Runtime authorization uses more than a token.
It also uses execution context.

Execution context can carry things like:
- agent identity
- project identity
- scopes
- role

That lets Agent Auth check whether the current action should be allowed.

---

## 6. What project scope means

Project-aware flows can carry project scope information.

That allows runtime checks to reject mismatches, for example when:
- the execution context says one project
- but the active scope says another project

This helps keep authorization consistent.

---

## 7. Token lifecycle

Project tokens are shown once when created.

That means:
- copy them immediately
- store them safely
- if you lose one, create a new token
- revoke the old token if needed

Old token values should not be shown again later.

---

## 8. Recommended user flow

A simple flow is:

1. start the local server
2. log in
3. create a project
4. create a project token
5. sync your tools and agents
6. run your example
7. verify in the UI

---

## 9. Simple summary

### Token
Authenticates the caller.

### Sync
Moves code-defined state into the control plane.

### Execution context
Tells runtime which identity and project are active.

### Policy
Decides whether an action is allowed.

### UI
Lets you manage and verify what exists.
