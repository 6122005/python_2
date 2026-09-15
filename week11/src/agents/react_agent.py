"""Day 4 (D54) — ReAct (Reason + Act) agent.

Implements the classic Thought -> Action -> Observation loop: the model is
instructed to reason out loud before each tool call, then we run the tool
it picked and feed the result back until it has enough information to give
a final answer.

Tools are intentionally mocked (a small local knowledge base + a word
counter) rather than hitting the real network, so the agent's control
flow — the part actually being practiced this week — can be run and
graded fully offline and deterministically.

Usage:
    python -m src.agents.react_agent "Research LangGraph and write a one-sentence summary"
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from src.llm_client import LLMClient

SYSTEM_PROMPT = """You are a ReAct-style agent. Before every tool call, think
step by step about what you need and why, in a short paragraph, then call
the tool. When you have enough information, stop calling tools and give a
final answer directly. Call at most one tool per turn."""

DEFAULT_MAX_STEPS = 6


# --------------------------------------------------------------------------
# Tools — deliberately mocked, no real network calls (see module docstring)
# --------------------------------------------------------------------------

_MOCK_KNOWLEDGE_BASE: Dict[str, str] = {
    "langchain": (
        "LangChain is an open-source framework for building applications with "
        "LLMs, providing abstractions for chains, agents, memory, and tool use."
    ),
    "langgraph": (
        "LangGraph is a library built on LangChain for building stateful, "
        "multi-actor applications as graphs of nodes and edges."
    ),
    "react pattern": (
        "ReAct interleaves reasoning traces ('thoughts') with actions (tool "
        "calls), letting an LLM plan, act, and observe results in a loop "
        "instead of answering in one shot."
    ),
}


def tool_search(query: str) -> str:
    """Look up a topic in a small local knowledge base."""
    query_lower = query.lower()
    for key, snippet in _MOCK_KNOWLEDGE_BASE.items():
        if key in query_lower:
            return snippet
    return f"No indexed results for '{query}'."


def tool_word_count(text: str) -> str:
    """Count words in a piece of text."""
    return str(len(text.split()))


TOOL_REGISTRY: Dict[str, Callable[..., str]] = {
    "search": tool_search,
    "word_count": tool_word_count,
}

TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        "name": "search",
        "description": "Look up a topic in the knowledge base. Returns a short summary, "
        "or a 'no results' message if the topic isn't indexed.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "word_count",
        "description": "Count words in a piece of text.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
]


# --------------------------------------------------------------------------
# Agent loop
# --------------------------------------------------------------------------


@dataclass
class StepLog:
    step: int
    thought: str
    action: Optional[str]
    observation: Optional[str]


class ReActAgent:
    def __init__(self, llm: LLMClient | None = None, max_steps: int = DEFAULT_MAX_STEPS) -> None:
        self.llm = llm or LLMClient()
        self.max_steps = max_steps
        self.trace: List[StepLog] = []

    def run(self, task: str) -> str:
        """Run the Thought -> Action -> Observation loop until a final answer
        or max_steps is reached. Returns the final answer text."""
        messages: List[Dict[str, Any]] = [{"role": "user", "content": task}]
        self.trace.clear()

        for step in range(1, self.max_steps + 1):
            response = self.llm.send(messages=messages, system=SYSTEM_PROMPT, tools=TOOL_SCHEMAS)
            thought = LLMClient.text_of(response)
            tool_calls = [block for block in response.content if block.type == "tool_use"]

            if not tool_calls:
                self.trace.append(StepLog(step, thought, None, None))
                return thought

            # Execute at most one tool call per step, per the system prompt.
            call = tool_calls[0]
            fn = TOOL_REGISTRY.get(call.name)
            if fn is None:
                observation = f"Error: unknown tool '{call.name}'"
            else:
                try:
                    observation = fn(**call.input)
                except Exception as exc:  # a bad tool call shouldn't crash the agent
                    observation = f"Error running tool '{call.name}': {exc}"

            self.trace.append(StepLog(step, thought, f"{call.name}({call.input})", observation))

            messages.append({"role": "assistant", "content": response.content})
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "tool_result", "tool_use_id": call.id, "content": observation}
                    ],
                }
            )

        return f"Stopped: reached max_steps ({self.max_steps}) without a final answer."

    def print_trace(self) -> None:
        for log in self.trace:
            print(f"--- Step {log.step} ---")
            if log.thought:
                print(f"Thought: {log.thought}")
            if log.action:
                print(f"Action: {log.action}")
            if log.observation:
                print(f"Observation: {log.observation}")
            print()


def main() -> None:
    task = " ".join(sys.argv[1:]) or "Research LangGraph and write a one-sentence summary."
    agent = ReActAgent()
    answer = agent.run(task)
    agent.print_trace()
    print(f"Final answer: {answer}")


if __name__ == "__main__":
    main()
