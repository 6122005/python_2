"""Day 2 (D52) — Agent with short-term memory only.

Run it, tell it something, then ask "what did I just ask about?" — it
answers correctly because the full turn history is resent to the model on
every call. Memory here is entirely in RAM: restart the process and it's
gone (that's the point — long-term memory is Wednesday's problem).

Usage:
    python -m src.agents.agent_with_memory
"""
from __future__ import annotations

from src.llm_client import LLMClient
from src.memory.short_term import ShortTermMemory

SYSTEM_PROMPT = "You are a concise, helpful assistant."


class MemoryAgent:
    def __init__(self, llm: LLMClient | None = None, max_turns: int = 20) -> None:
        self.llm = llm or LLMClient()
        self.memory = ShortTermMemory(max_turns=max_turns)

    def ask(self, user_input: str) -> str:
        self.memory.add_user(user_input)
        response = self.llm.send(messages=self.memory.as_messages(), system=SYSTEM_PROMPT)
        reply = LLMClient.text_of(response)
        self.memory.add_assistant(reply)
        return reply


def main() -> None:
    agent = MemoryAgent()
    print("MemoryAgent ready. Type 'exit' to quit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue
        reply = agent.ask(user_input)
        print(f"Agent: {reply}\n")


if __name__ == "__main__":
    main()
