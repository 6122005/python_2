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
    # Initialize the LLM
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    
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
