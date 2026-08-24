# Week 12: LangChain Fundamentals

This directory contains the deliverables for Week 12 (Days 56-60). We transition from building simple tools to using robust LangChain frameworks and RAG pipelines.

## Deliverables

### Day 56: LangChain Chatbot (`src/langchain_chat.py`)
A command-line chatbot built entirely using LangChain's `ChatGroq` wrapper and `SystemMessage`/`HumanMessage` memory.

### Day 57: LangChain Agent with Built-In Tools (`src/lc_agent.py`)
A LangChain React Agent equipped with `DuckDuckGoSearchRun` and `WikipediaQueryRun`. It is designed to find today's date, search for the date of Diwali 2025, and calculate the difference.

### Day 58: Cleaner LangChain RAG (`src/lc_rag.py`)
A Retrieval-Augmented Generation (RAG) pipeline that:
1. Loads a local PDF document (`data/sample.pdf`) using `PyPDFLoader`.
2. Chunks it using `RecursiveCharacterTextSplitter`.
3. Embeds it using local, free HuggingFace embeddings (`all-MiniLM-L6-v2`).
4. Stores it in a local `ChromaDB` vector store.
5. Uses a QA chain to answer specific questions based on the document (e.g. asking for the secret password).

### Day 59: Hybrid Agent (`src/hybrid_agent.py`)
Combines Day 57 and Day 58. This agent has two tools:
- `search_documents`: A custom `@tool` wrapping the RAG pipeline from Day 58.
- `web_search`: The `DuckDuckGoSearchRun` tool.
The agent dynamically decides whether to search the internal PDF or search the live web based on your questions.

### Day 60: Code Review & Refactoring
All scripts in this directory have been heavily commented, include explicit docstrings, and remove dead code. The repository is clean and ready for Phase 4 work!

## Setup and Running

1. **Install Requirements:**
   ```bash
   cd week12
   pip install -r requirements.txt
   ```
2. **API Keys:**
   Make sure you have your `.env` file copied into `week12/` with `GROQ_API_KEY`.
3. **Run Scripts:**
   Run any of the scripts from the `src/` directory.
   ```bash
   python src/hybrid_agent.py
   ```
