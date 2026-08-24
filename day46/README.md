# Week 10: What is an agent? Understand agentic patterns

This folder contains the assignments and deliverables for Days 46 to 50 of the 4-week agentic AI course.

## Folder Structure

- `day46_summary.md`: 1-page summary on what an agent is, ReAct pattern, tool use, and when to use agents vs simple chains. (Day 46 Deliverable)
- `day47_function_calling_annotated.md`: Annotated copy of the function calling example from docs. (Day 47 Deliverable)
- `src/agent_v1.py`: First tool-calling agent with 2 tools (`get_weather` and `get_time`). (Day 48 Deliverable)
- `src/agent_v2.py`: Agent upgraded with a web search tool using DuckDuckGo. (Day 49 Deliverable)
- `src/agent_v3.py`: Agent upgraded with a `read_file` tool to read .txt files from disk. (Day 50 Deliverable)
- `data/`: Folder to hold sample files to read (like `sample.txt`).
- `requirements.txt`: List of dependencies needed to run the agents.

## How to run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure you have `OPENAI_API_KEY` set in your environment (for `ChatOpenAI`).
3. Run the scripts from the `src` directory:
   ```bash
   python src/agent_v1.py
   python src/agent_v2.py
   python src/agent_v3.py
   ```
