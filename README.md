# agentauthlayer-examples
Examples and sample agents for using the agentauthlayer SDK.

## Getting Started

### 1. Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Usage
The package is imported as `agent_auth`:
```python
import agent_auth
```

## Running the LangGraph Agent Authorization Demo

We have created two demo agents to test how to secure your agent workflows using `@require_permission` decorators:

### 1. General Demo (`simple_agent.py`)
To run the general simulation showing simple commands executed by a research agent and an admin:
```bash
python simple_agent.py
```

### 2. Math Agent Demo (`math_agent.py`)
This is a more realistic multi-step agent flow that parses mathematical expressions into plans and executes them. It defines custom roles (`math_standard` and `math_advanced`) to showcase permission boundaries in math operations.

To run the math agent:
```bash
python math_agent.py
```

