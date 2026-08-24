# User Feedback: v1 vs v2 (Day 64)

## Deployment Context
- **v1 Product:** Simple Streamlit UI connected directly to a base LLM (no tools, no internet access).
- **v2 Product:** Upgraded Streamlit UI connected to a LangGraph Agent with DuckDuckGo and Wikipedia tools. Agent reasoning is exposed via a UI expander.

## User Feedback Comparison

| User | v1 Feedback (Week 11) | v2 Feedback (Week 13) |
|---|---|---|
| **User A** | "It hallucinates answers about recent events. Unreliable." | "Wow! The expander shows exactly what it searched for. I asked about yesterday's news and it gave me the right answer with a source." |
| **User B** | "Clean UI, but basically just ChatGPT. Nothing special." | "Seeing the 'Agent reasoning' steps builds a lot of trust. I know exactly how it came to its conclusion." |
| **User C** | "Could not answer multi-step historical questions properly." | "It searched Wikipedia for the first fact, then searched DuckDuckGo for the second. Big improvement." |

## What's Still Missing?
- Users requested the ability to upload their own PDFs (combining Week 12 RAG integration into this UI).
- The agent sometimes takes 10-15 seconds to reply because it's doing multiple web searches. We need a way to stream the thoughts in real-time instead of waiting for the final chunk.
