# What is an AI Agent?

An AI Agent is an artificial intelligence system that does not just answer questions or generate text based on its internal knowledge, but can actively interact with its environment, make decisions, and use external tools to achieve a specific goal. While a standard LLM acts as a passive answering engine, an agent operates autonomously in a loop of thinking and acting.

## Key Concepts

### The ReAct Pattern (Reason + Act)
ReAct is a prompt engineering paradigm that combines reasoning (chain-of-thought) with action (tool use).
1. **Thought:** The agent thinks about what it needs to do to solve the current step of the problem.
2. **Action:** The agent decides to call a specific tool with specific arguments.
3. **Observation:** The environment returns the result of the tool execution.
The agent repeats this cycle until it has enough information to provide a final answer.

### Tool Use (Function Calling)
Tools give agents the ability to interact with the outside world. Tools can be APIs, databases, web search engines, or even code interpreters. Through "function calling," the LLM is provided with a schema of available tools and their expected arguments. The LLM can then output a structured response indicating which tool to run.

### Planning Loops
Agents use planning loops to break down complex tasks into manageable sub-tasks. They can reflect on past actions, correct mistakes, and dynamically adjust their plan based on new observations.

## When to use Agents vs. Simple Chains

**Use Simple Chains when:**
- The task is deterministic and predictable.
- The workflow is linear (e.g., Extract text -> Summarize -> Translate).
- All required context can be provided upfront or fetched in a single, predictable step.
- Speed and low cost are critical.

**Use Agents when:**
- The task requires dynamic decision making.
- The steps to solve the problem are unknown upfront and depend on intermediate results.
- The system needs to self-correct or retry failed actions.
- The task involves exploring external data sources sequentially (e.g., search web -> read article -> search for clarification).
