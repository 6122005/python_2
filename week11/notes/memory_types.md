# Memory in LLM Agents: Short-Term vs Long-Term

## 1. The core distinction

| | Short-term memory | Long-term memory |
|---|---|---|
| **What it is** | The running list of turns in the *current* conversation | Durable facts stored *outside* the conversation |
| **Lifetime** | Dies when the process/session ends | Survives across sessions, days, restarts |
| **Where it lives** | RAM (a list/deque you resend each call) | Disk / database / vector store |
| **How the model sees it** | Sent as `messages` in every API call | Injected into the system prompt, or retrieved via RAG |
| **Bounded by** | Context window (tokens) | Storage size, not the context window |

The important mental model: **an LLM has no memory of its own between API
calls.** Every "memory" an agent appears to have is really just data that
*you* re-send on the next call. Short-term and long-term memory are two
different strategies for deciding *what* to re-send.

## 2. Short-term memory

Short-term memory is nothing more than accumulating the conversation as a
list of `{role, content}` turns and sending the whole list back on every
request:

```python
messages = []

def ask(user_text: str) -> str:
    messages.append({"role": "user", "content": user_text})
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=messages,
    )
    reply = response.content[0].text
    messages.append({"role": "assistant", "content": reply})
    return reply
```

Ask `"My favorite color is teal"`, then ask `"what's my favorite color?"` —
it works because both turns are in `messages` on the second call. This is
exactly what `agent_with_memory.py` (Tuesday) does, wrapped in a
`ShortTermMemory` class with a max-turns limit so the list doesn't grow
unbounded and blow the context window on a long session.

**Failure mode:** once the conversation exceeds the window (or the context
limit), old turns get evicted — the agent "forgets" things from earlier in
a very long session. That's expected behavior, not a bug, and it's one of
the cases tested in Friday's stress-test report.

## 3. Long-term memory

Long-term memory means *pulling facts out of* the conversation and saving
them somewhere that outlives the process — a JSON file, a database, or a
vector store for semantic recall. The agent loads relevant facts on
startup and folds them into the system prompt:

```python
import json
from pathlib import Path

FACTS_PATH = Path("data/facts.json")

def load_facts() -> dict:
    if FACTS_PATH.exists():
        return json.loads(FACTS_PATH.read_text())
    return {}

def save_fact(key: str, value: str) -> None:
    facts = load_facts()
    facts[key] = value
    FACTS_PATH.write_text(json.dumps(facts, indent=2))

facts = load_facts()
system_prompt = "You are a helpful assistant.\n\nKnown facts:\n" + "\n".join(
    f"- {k}: {v}" for k, v in facts.items()
)
```

`agent_with_longterm.py` (Wednesday) implements this with a
`LongTermMemory` class, and adds one more piece: at the end of a session
it asks the model itself to extract which facts from the conversation are
worth remembering (returned as JSON), rather than saving everything. That
keeps the fact store small and relevant instead of becoming a dump of the
entire transcript.

## 4. How LangChain frames this

LangChain's memory abstractions map onto the same split:

- **Short-term** → `ConversationBufferMemory` / `ConversationBufferWindowMemory`
  (keep the last N turns) or `ConversationSummaryMemory` (compress older
  turns into a running summary instead of dropping them outright).
- **Long-term** → `VectorStoreRetrieverMemory` (embed and store facts, then
  retrieve the most *relevant* ones per query instead of injecting
  everything) — this is the RAG-style approach for long-term memory at
  scale, versus the flat JSON file used here for a small fact set.

The flat-JSON approach in this project is deliberately simple — it's the
right tool when the fact set is small (dozens of facts, not thousands). At
scale, long-term memory becomes a retrieval problem: embed each fact,
store it in a vector index, and retrieve only the top-k facts relevant to
the current query instead of stuffing all of them into the system prompt.

## 5. Key takeaway

Short-term memory answers *"what did we just talk about?"*
Long-term memory answers *"what do you know about me from before?"*

An agent that's genuinely useful across sessions needs both: short-term
memory for coherent conversation, long-term memory so it doesn't start
from zero every time you open a new session.
