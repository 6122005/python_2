import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# Load environment variables
load_dotenv()

@tool
def web_search(query: str) -> str:
    """Search the web for current events, live news, weather, or real-time information."""
    try:
        from ddgs import DDGS
        with DDGS(timeout=7) as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                return "\n\n".join(r.get("body", "") for r in results if r.get("body"))
    except Exception:
        pass

    try:
        from duckduckgo_search import DDGS
        with DDGS(timeout=7) as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                return "\n\n".join(r.get("body", "") for r in results if r.get("body"))
    except Exception as e:
        return f"Web search timed out or was temporarily unavailable ({e}). Please answer using your knowledge base."

    return "No search results found."

@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for encyclopedic facts, people, sports statistics, and history."""
    try:
        import wikipedia
        return wikipedia.summary(query, sentences=3)
    except Exception as e:
        return f"Wikipedia returned: {e}. Answer using your internal knowledge."

def get_agent():
    """Initializes and returns the LangGraph React Agent with resilient tools."""
    # Check both environment variable and Streamlit Cloud secrets
    api_key = os.getenv("GROQ_API_KEY")
    try:
        import streamlit as st
        if not api_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    # Initialize the LLM
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0, groq_api_key=api_key)
    
    tools = [web_search, wikipedia_search]
    
    # Create the ReAct agent
    agent_executor = create_react_agent(llm, tools)
    return agent_executor

if __name__ == "__main__":
    agent = get_agent()
    print("Backend Agent initialized successfully.")
    print("Testing agent with a query...")
    response = agent.invoke({"messages": [("user", "who win 2024 T20 cricket world cup..?")]})
    print("\nResponse:")
    print(response["messages"][-1].content)
