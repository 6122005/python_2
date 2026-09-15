"""Long-term memory: durable facts persisted to disk between sessions.

Unlike short-term memory (which dies with the process), long-term memory
is a small JSON key-value store on disk. The agent reads it at startup and
writes to it whenever it learns something worth remembering, so facts
survive across separate runs of the program.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional


@dataclass
class Fact:
    value: str
    updated_at: str
    source_session: Optional[str] = None


class LongTermMemory:
    """JSON-file-backed fact store, keyed by fact name.

    Example on disk::

        {
          "user_name": {"value": "Jenish", "updated_at": "...", "source_session": "s1"},
          "favorite_language": {"value": "Python", "updated_at": "...", "source_session": "s1"}
        }
    """

    def __init__(self, path: str | Path = "data/facts.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._facts: Dict[str, Fact] = self._load()

    def _load(self) -> Dict[str, Fact]:
        if not self.path.exists():
            return {}
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # A corrupt file shouldn't crash the agent, but we also
            # shouldn't silently discard the user's data — back it up.
            backup = self.path.with_suffix(".corrupt.json")
            self.path.replace(backup)
            return {}
        return {k: Fact(**v) for k, v in raw.items()}

    def save(self) -> None:
        payload = {k: asdict(v) for k, v in self._facts.items()}
        self.path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def remember(self, key: str, value: str, session_id: Optional[str] = None) -> None:
        self._facts[key] = Fact(
            value=value,
            updated_at=datetime.now(timezone.utc).isoformat(),
            source_session=session_id,
        )
        self.save()

    def forget(self, key: str) -> None:
        self._facts.pop(key, None)
        self.save()

    def recall(self, key: str) -> Optional[str]:
        fact = self._facts.get(key)
        return fact.value if fact else None

    def all_facts(self) -> Dict[str, str]:
        return {k: v.value for k, v in self._facts.items()}

    def as_system_context(self) -> str:
        """Render known facts as a block to prepend to the system prompt.

        Returns an empty string when there are no facts yet, so callers
        can safely concatenate this without an extra "no facts" branch.
        """
        if not self._facts:
            return ""
        lines = [f"- {k}: {v.value}" for k, v in self._facts.items()]
        return "Known facts about the user from previous sessions:\n" + "\n".join(lines)

    def __len__(self) -> int:
        return len(self._facts)
