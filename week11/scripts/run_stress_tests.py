"""Day 5 (D55) — Stress test runner.

Runs 10 deliberately tricky tasks against the agents built this week,
captures what actually happened, and (re)writes reports/agent_failure_report.md
from the results. This requires a live ANTHROPIC_API_KEY — it makes real
API calls, unlike tests/test_memory.py which is fully offline.

Usage:
    python scripts/run_stress_tests.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agents.agent_with_longterm import LongTermAgent
from src.agents.react_agent import ReActAgent

REPORT_PATH = Path(__file__).resolve().parent.parent / "reports" / "agent_failure_report.md"


def run_case(name: str, fn) -> dict:
    """Run one stress-test case, capturing success/failure instead of raising."""
    try:
        result = fn()
        return {"name": name, "status": "ran", "result": result, "error": None}
    except Exception as exc:  # a stress test crashing IS a finding, not a bug in the runner
        return {"name": name, "status": "error", "result": None, "error": f"{type(exc).__name__}: {exc}"}


def build_cases() -> list[tuple[str, callable]]:
    tmp_facts = Path(tempfile.mkdtemp()) / "facts.json"

    cases: list[tuple[str, callable]] = [
        (
            "1. Out-of-scope factual question (no matching tool)",
            lambda: ReActAgent(max_steps=4).run("What's the weather in Tokyo right now?"),
        ),
        (
            "2. Empty-input edge case",
            lambda: ReActAgent(max_steps=4).run("Count the words in this text: ''"),
        ),
        (
            "3. Chained multi-tool task in one instruction",
            lambda: ReActAgent(max_steps=6).run(
                "Search for LangChain, then count the words in the result you got back."
            ),
        ),
        (
            "4. Short-term memory beyond the window",
            lambda: _run_memory_overflow_case(),
        ),
        (
            "5. Fact key drift across two long-term sessions",
            lambda: _run_fact_key_drift_case(tmp_facts),
        ),
        (
            "6. Request for a capability with no available tool",
            lambda: ReActAgent(max_steps=4).run("Send an email to my manager summarizing this week."),
        ),
        (
            "7. Deliberate loop trigger (repeated tool misses)",
            lambda: ReActAgent(max_steps=4).run(
                "Keep searching for 'xyz123nonexistent' until you find something, then report it."
            ),
        ),
        (
            "8. Ambiguous / sarcastic fact for extraction",
            lambda: _run_fact_extraction_case(
                tmp_facts, "I guess I like Python, who doesn't. Anyway, what's a decorator?"
            ),
        ),
        (
            "9. Malformed tool argument (wrong type)",
            lambda: ReActAgent(max_steps=4).run(
                "Call the word_count tool directly on the number 12345, not text."
            ),
        ),
        (
            "10. Concurrent-write race on the fact store",
            lambda: _run_concurrent_write_case(tmp_facts),
        ),
    ]
    return cases


def _run_memory_overflow_case():
    from src.agents.agent_with_memory import MemoryAgent

    agent = MemoryAgent(max_turns=20)
    for i in range(25):  # exceeds the 20-turn window
        agent.ask(f"Remember this number: {i}")
    return agent.ask("What was the very first number I told you?")


def _run_fact_key_drift_case(facts_path: Path):
    a1 = LongTermAgent(session_id="drift_s1", facts_path=str(facts_path))
    a1.ask("My favorite programming language is Python.")
    a1.end_session()

    a2 = LongTermAgent(session_id="drift_s2", facts_path=str(facts_path))
    known_before = dict(a2.long_term.all_facts())
    a2.ask("Actually, I've switched to using TypeScript most days now.")
    a2.end_session()
    known_after = dict(a2.long_term.all_facts())
    return {"before": known_before, "after": known_after}


def _run_fact_extraction_case(facts_path: Path, user_line: str):
    agent = LongTermAgent(session_id="sarcasm_test", facts_path=str(facts_path.with_name("sarcasm_facts.json")))
    agent.ask(user_line)
    return agent.end_session()


def _run_concurrent_write_case(facts_path: Path):
    path = str(facts_path.with_name("race_facts.json"))
    a1 = LongTermAgent(session_id="race_a", facts_path=path)
    a2 = LongTermAgent(session_id="race_b", facts_path=path)
    a1.long_term.remember("shared_key", "from_session_a")
    a2.long_term.remember("shared_key", "from_session_b")  # last write wins
    a1.long_term._facts = a1.long_term._load()  # re-read from disk
    return a1.long_term.recall("shared_key")


def render_report(results: list[dict]) -> str:
    lines = [
        "# Agent Failure Report — Week 11, Day 5 (D55)",
        "",
        "Ten stress tests run against this week's agents "
        "(`agent_with_memory.py`, `agent_with_longterm.py`, `react_agent.py`) "
        "via `scripts/run_stress_tests.py`. Each row is what actually happened "
        "when the script last ran.",
        "",
        "| # | Test | Status | What happened | Why |",
        "|---|------|--------|----------------|-----|",
    ]
    for i, r in enumerate(results, start=1):
        status = "✅ ran" if r["status"] == "ran" else "❌ raised"
        outcome = r["result"] if r["status"] == "ran" else r["error"]
        outcome_str = str(outcome).replace("\n", " ")[:200]
        lines.append(f"| {i} | {r['name']} | {status} | {outcome_str} | — fill in root cause after review |")

    lines += [
        "",
        "## Notes",
        "",
        "- This file is regenerated by `scripts/run_stress_tests.py` — edit the "
        "'Why' column analysis in a copy if you want to keep manual notes, "
        "or move them into a separate `agent_failure_report_analysis.md`.",
        "- Cases 4, 7, and 9 are designed to trigger known, deliberate limits "
        "(memory window eviction, the ReAct `max_steps` ceiling, and a "
        "type-mismatch tool call) — seeing them fail gracefully (not crash "
        "the whole process) is the passing condition, not a bug.",
    ]
    return "\n".join(lines)


def main() -> None:
    cases = build_cases()
    results = [run_case(name, fn) for name, fn in cases]
    report = render_report(results)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT_PATH} ({len(results)} cases)")
    for r in results:
        print(f"- {r['name']}: {r['status']}")


if __name__ == "__main__":
    main()
