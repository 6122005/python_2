# Phase 3 Retrospective & v2 Plan (Day 61)

## Retrospective on v1 (Phase 3 Product)
In Phase 3, we built a simple, static LLM chat interface. While users appreciated the clean UI and the general knowledge of the AI, a significant limitation was identified during user feedback sessions:
- **Limitation:** The AI hallucinated facts about recent events and could not provide real-time data or citations. 
- **User Quote:** "I asked it about a news event from yesterday, and it confidently gave me the wrong answer."

## #1 Improvement for v2
The single biggest improvement we can make is **adding an autonomous agent with live tools**. 

By upgrading the backend to a LangGraph React Agent, we can give the LLM access to:
1. **Web Search (DuckDuckGo)**
2. **Wikipedia**

## Why an Agent?
Instead of immediately guessing an answer, the Agent will:
1. Parse the user's question.
2. Determine if it needs live context.
3. Automatically search the internet.
4. Read the results.
5. Formulate an accurate, sourced answer.

This directly solves the hallucination problem and transforms the app from a simple text-generator into a **Smart Research Assistant**.
