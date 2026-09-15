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
    
    # Initialize Tools
    search_tool = DuckDuckGoSearchRun()
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    
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
