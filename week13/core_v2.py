import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Load environment variables
load_dotenv()

def get_agent():
    """Initializes and returns the LangGraph React Agent with tools."""
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
    
    # Initialize Tools safely
    try:
        search_tool = DuckDuckGoSearchRun()
    except Exception:
        from langchain_core.tools import tool
        @tool
        def search_tool(query: str) -> str:
            """Search the web for current events, news, and general information."""
            try:
                from ddgs import DDGS
                with DDGS() as ddgs:
                    res = list(ddgs.text(query, max_results=3))
                    return "\n\n".join(r["body"] for r in res)
            except Exception:
                try:
                    from duckduckgo_search import DDGS
                    with DDGS() as ddgs:
                        res = list(ddgs.text(query, max_results=3))
                        return "\n\n".join(r["body"] for r in res)
                except Exception as e:
                    return f"Search error: {e}"

    try:
        wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    except Exception:
        from langchain_core.tools import tool
        @tool
        def wikipedia_tool(query: str) -> str:
            """Search Wikipedia for encyclopedic facts and history."""
            try:
                import wikipedia
                return wikipedia.summary(query, sentences=3)
            except Exception as e:
                return f"Wikipedia error: {e}"

    tools = [search_tool, wikipedia_tool]
    
    # Create the ReAct agent
    agent_executor = create_react_agent(llm, tools)
    return agent_executor

if __name__ == "__main__":
    agent = get_agent()
    print("Backend Agent initialized successfully.")
    print("Testing agent with a simple query...")
    response = agent.invoke({"messages": [("user", "who win 2024 T20 cricket world cup..?")]})
    print("\nResponse:")
    print(response["messages"][-1].content)
