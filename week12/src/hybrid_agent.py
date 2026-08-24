import os
import warnings
from dotenv import load_dotenv

# Suppress warnings for clean output
warnings.filterwarnings("ignore")

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

# Import the RAG chain builder from Day 58
from lc_rag import build_rag_chain

@tool
def search_documents(query: str) -> str:
    """Use this tool to search internal documents or PDFs for information, specifically regarding RAG passwords."""
    rag_chain = build_rag_chain()
    response = rag_chain.invoke({"input": query})
    return response["answer"]

def main():
    load_dotenv()
    
    # Initialize the LLM
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    
    # Initialize Tools
    web_search = DuckDuckGoSearchRun()
    web_search.name = "web_search"
    web_search.description = "Use this tool to search the live internet for general knowledge, news, current events, or things outside the internal documents."
    
    tools = [search_documents, web_search]
    
    # Create Agent
    agent_executor = create_react_agent(llm, tools)
    
    print("--- Hybrid Agent Ready (Day 59) ---")
    print("This agent has access to your local PDFs (search_documents) and the live Internet (web_search).")
    print("Type 'quit' or 'exit' to stop.")
    
    while True:
        question = input("\nUser: ")
        if question.lower() in ['quit', 'exit']:
            print("Exiting...")
            break
            
        if not question.strip():
            continue
            
        try:
            response = agent_executor.invoke({"messages": [("user", question)]})
            print(f"\nAgent: {response['messages'][-1].content}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
