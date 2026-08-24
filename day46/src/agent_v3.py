import os
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from datetime import datetime
import pytz
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

@tool
def read_file(path: str) -> str:
    """Read the contents of a .txt file from disk."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {e}"

# Web Search Tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool
def web_search(query: str) -> str:
    """Search the web for real-time information."""
    try:
        search = DuckDuckGoSearchRun()
        return search.invoke(query)
    except Exception as e:
        return f"Web search failed: {e}. Try to answer without it, or say you don't know."

tools = [get_weather, get_time, web_search, read_file]

def run_agent():
    from dotenv import load_dotenv
    load_dotenv()
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    
    agent_executor = create_react_agent(llm, tools)
    
    print("Agent V3 with 4 tools (Weather, Time, Web Search, Read File) ready!")
    question = "Read the file at '/Users/darshankanani/python2/python_2/day46/src/../data/sample.txt' and answer all the questions or instructions found inside it. Use the web search tool if you need to find real-time information to answer them."
    print(f"\nUser: {question}")
    response = agent_executor.invoke({"messages": [("user", question)]})
    print(f"\nAgent: {response['messages'][-1].content}")

if __name__ == "__main__":
    run_agent()
