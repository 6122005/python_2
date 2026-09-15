"""Short-term (working) memory for a single conversation session.

Short-term memory is nothing more than the running list of turns in the
current conversation. It lives only in RAM, resets when the process exits,
and is exactly what gets sent back to the model on every call so it can
refer to earlier turns. See notes/memory_types.md for the full writeup.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, List, Literal

Role = Literal["user", "assistant"]


@dataclass
class Turn:
    role: Role
    content: str


class ShortTermMemory:
    """Fixed-size rolling window over the current conversation.

    Args:
        max_turns: how many (user, assistant) turn PAIRS to keep. Older
            turns are silently dropped once the window fills up, which
            keeps token usage bounded on long sessions. This is the
            "forgetting" behavior described in notes/memory_types.md.
    """

    def __init__(self, max_turns: int = 20) -> None:
        if max_turns < 1:
            raise ValueError("max_turns must be >= 1")
        self._max_messages = max_turns * 2
        self._turns: Deque[Turn] = deque(maxlen=self._max_messages)

    def add_user(self, content: str) -> None:
        self._turns.append(Turn("user", content))

    def add_assistant(self, content: str) -> None:
        self._turns.append(Turn("assistant", content))

    def as_messages(self) -> List[dict]:
        """Return turns in the {role, content} shape the Anthropic API expects."""
        return [{"role": t.role, "content": t.content} for t in self._turns]

    def clear(self) -> None:
        self._turns.clear()

    def __len__(self) -> int:
        return len(self._turns)

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"ShortTermMemory(turns={len(self._turns)}, capacity={self._max_messages})"
