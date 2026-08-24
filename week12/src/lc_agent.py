import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import datetime

def main():
    load_dotenv()
    
    # Initialize the Groq LLM
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    
    # Initialize LangChain built-in tools
    search_tool = DuckDuckGoSearchRun()
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    
    tools = [search_tool, wikipedia_tool]
    
    # Create the ReAct agent
    agent_executor = create_react_agent(llm, tools)
    
    print("Agent D57 (Wikipedia + DuckDuckGo Tools) ready!")
    
    # Add today's date to help the agent calculate correctly
    today = datetime.date.today().strftime("%Y-%m-%d")
    question = f"Today's date is {today}. How many days until Diwali 2025? Please use your tools to find the exact date of Diwali 2025, and then calculate the number of days from today until that date."
    print(f"\nUser: {question}")
    
    try:
        response = agent_executor.invoke({"messages": [("user", question)]})
        print(f"\nAgent: {response['messages'][-1].content}")
    except Exception as e:
        print(f"Agent error: {e}")

if __name__ == "__main__":
    main()
