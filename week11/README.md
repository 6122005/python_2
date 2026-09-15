# Week 11 — Agent Memory + Planning

Five days of building toward one theme: agents that remember things and
plan before they act. Each day's deliverable is a real, runnable module,
not a toy snippet — they share a common `src/` core so the code compounds
instead of being rewritten daily.

## Folder structure

```
week11-agent-memory-planning/
├── README.md
├── requirements.txt
├── .env.example
├── notes/
│   └── memory_types.md          # Mon (D51) — short vs long-term memory notes
├── src/
│   ├── llm_client.py            # Shared, retry-safe Anthropic API wrapper
│   ├── memory/
│   │   ├── short_term.py        # Rolling conversation window
│   │   └── long_term.py         # JSON-backed durable fact store
│   └── agents/
│       ├── agent_with_memory.py     # Tue (D52) — short-term memory only
│       ├── agent_with_longterm.py   # Wed (D53) — short-term + long-term
│       └── react_agent.py           # Thu (D54) — ReAct reasoning + tools
├── scripts/
│   └── run_stress_tests.py      # Fri (D55) — runs the 10 stress tests
├── reports/
│   └── agent_failure_report.md  # Fri (D55) — findings from the stress tests
├── tests/
│   └── test_memory.py           # Offline unit tests (no API key needed)
└── data/
    └── facts.json               # Created automatically by long-term memory
```

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then paste your ANTHROPIC_API_KEY into .env
export $(cat .env | xargs)  # or use python-dotenv, already wired in
```

## Running each day's deliverable

```bash
# Tue — short-term memory only
python -m src.agents.agent_with_memory

# Wed — long-term memory, run twice with the same --session to prove
# facts persist across process restarts
python -m src.agents.agent_with_longterm --session s1
python -m src.agents.agent_with_longterm --session s2

# Thu — ReAct agent (reasons out loud before every tool call)
python -m src.agents.react_agent "Research LangGraph and summarize it in one sentence"

# Fri — stress test suite, writes reports/agent_failure_report.md
python scripts/run_stress_tests.py
```

## Offline tests (no API key required)

```bash
pytest tests/ -v
```

These cover the memory classes and tool functions directly — the parts
of the system that don't depend on a live model call — so you get fast
feedback without burning API credits.

## Design notes

- **One LLM client, three agents.** `src/llm_client.py` is the only place
  that talks to the Anthropic API. Every agent composes it with different
  memory/planning strategies instead of re-implementing API plumbing.
- **Memory is two separate, composable classes**, not one blob — you can
  use `ShortTermMemory` alone (Tue), or layer `LongTermMemory` on top
  (Wed) without touching the short-term code.
- **The ReAct loop has a hard `max_steps` ceiling.** An agent that reasons
  in a loop can also loop forever; day 5's stress tests exist specifically
  to find that failure mode, so day 4 already guards against it.
