import os
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from datetime import datetime
import pytz

# Tools definition
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a specific city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key or api_key == "your-openweather-api-key-here":
        return "Error: OPENWEATHER_API_KEY is missing or invalid in .env file."
    
    import requests
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The current weather in {city} is {temp}°C with {desc}."
        else:
            return f"Error fetching weather: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error connecting to weather API: {e}"

@tool
def get_time(timezone: str) -> str:
    """Get the current time in a specific timezone. e.g. 'America/New_York'"""
    try:
        tz = pytz.timezone(timezone)
        return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error: Invalid timezone. {e}"

# Web Search Tool
search_tool = DuckDuckGoSearchRun()

tools = [get_weather, get_time, search_tool]

def run_agent():
    from dotenv import load_dotenv
    load_dotenv()
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    
    agent_executor = create_react_agent(llm, tools)
    
    print("Agent V2 with Weather, Time, and Web Search tools ready!")
    print("Type 'quit' or 'exit' to stop.")
    
    while True:
        question = input("\nAsk Agent V2 a question (e.g. 'What's the weather in Tokyo?' or 'Who won the 2024 Super Bowl?'): ")
        if question.lower() in ['quit', 'exit']:
            print("Exiting...")
            break
        
        print(f"\nUser: {question}")
        response = agent_executor.invoke({"messages": [("user", question)]})
        print(f"\nAgent: {response['messages'][-1].content}")

if __name__ == "__main__":
    run_agent()
