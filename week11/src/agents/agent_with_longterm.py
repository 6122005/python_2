"""Day 3 (D53) — Agent with short-term + long-term memory.

Long-term facts live in data/facts.json. On startup the agent loads
whatever it learned in previous sessions and injects it into the system
prompt. At the end of a session it asks the model to extract any durable
facts worth remembering, and saves them — so a fact mentioned in session 1
is known automatically in session 2, without re-explaining it.

Usage:
    python -m src.agents.agent_with_longterm --session s1
    python -m src.agents.agent_with_longterm --session s2   # facts persist
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

# Add week11 root to sys.path so direct execution works
WEEK11_ROOT = Path(__file__).resolve().parent.parent.parent
if str(WEEK11_ROOT) not in sys.path:
    sys.path.insert(0, str(WEEK11_ROOT))

from src.llm_client import LLMClient
from src.memory.long_term import LongTermMemory
from src.memory.short_term import ShortTermMemory

BASE_SYSTEM_PROMPT = "You are a concise, helpful assistant."
DEFAULT_FACTS_PATH = str(WEEK11_ROOT / "data" / "facts.json")

FACT_EXTRACTION_PROMPT = """Review the conversation above. List any durable
facts about the user worth remembering for future sessions (name,
preferences, ongoing projects, decisions). Respond with ONLY a JSON object
mapping short snake_case keys to string values, e.g.
{"user_name": "Jenish", "favorite_language": "Python"}. If nothing is
worth remembering, respond with {}. No prose, no markdown fences."""


class LongTermAgent:
    def __init__(
        self,
        session_id: str | None = None,
        llm: LLMClient | None = None,
        facts_path: str = DEFAULT_FACTS_PATH,
        max_turns: int = 20,
    ) -> None:
        self.session_id = session_id or uuid.uuid4().hex[:8]
        self.llm = llm or LLMClient()
        self.short_term = ShortTermMemory(max_turns=max_turns)
        self.long_term = LongTermMemory(facts_path)

    def _system_prompt(self) -> str:
        facts_block = self.long_term.as_system_context()
        return f"{BASE_SYSTEM_PROMPT}\n\n{facts_block}" if facts_block else BASE_SYSTEM_PROMPT

    def ask(self, user_input: str) -> str:
        self.short_term.add_user(user_input)
        response = self.llm.send(messages=self.short_term.as_messages(), system=self._system_prompt())
        reply = LLMClient.text_of(response)
        self.short_term.add_assistant(reply)
        return reply

    def end_session(self) -> dict:
        """Ask the model to distill durable facts from this session, then persist them.

        Returns an empty dict (no crash) if the model's response isn't
        valid JSON — fact extraction failing shouldn't take down the
        whole session. This exact failure mode is exercised in Friday's
        stress-test report.
        """
        if len(self.short_term) == 0:
            return {}
        messages = self.short_term.as_messages() + [{"role": "user", "content": FACT_EXTRACTION_PROMPT}]
        response = self.llm.send(messages=messages, system=BASE_SYSTEM_PROMPT)
        raw = LLMClient.text_of(response).strip()
        try:
            facts = json.loads(raw)
        except json.JSONDecodeError:
            facts = {}
        for key, value in facts.items():
            self.long_term.remember(key, str(value), session_id=self.session_id)
        return facts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", default=None, help="Session id, e.g. s1 or s2")
    parser.add_argument("--facts-path", default=DEFAULT_FACTS_PATH)
    args = parser.parse_args()

    agent = LongTermAgent(session_id=args.session, facts_path=args.facts_path)
    known = agent.long_term.all_facts()
    if known:
        print(f"[loaded {len(known)} fact(s) from previous sessions: {known}]")
    print(f"LongTermAgent ready (session={agent.session_id}). Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue
        print(f"Agent: {agent.ask(user_input)}\n")

    new_facts = agent.end_session()
    if new_facts:
        print(f"[saved fact(s): {new_facts}]")


if __name__ == "__main__":
    main()
