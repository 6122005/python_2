import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# Load environment variables
load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Get accurate live real-time weather and temperature for any city in the world."""
    try:
        geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1", timeout=5).json()
        if not geo.get("results"):
            return f"Could not find location coordinates for '{city}'."
        loc = geo["results"][0]
        lat, lon, name = loc["latitude"], loc["longitude"], loc["name"]
        data = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m",
            timeout=5
        ).json()
        curr = data.get("current", {})
        temp = curr.get("temperature_2m")
        humidity = curr.get("relative_humidity_2m")
        wind = curr.get("wind_speed_10m")
        return f"Current live weather in {name}: Temperature: {temp}°C, Humidity: {humidity}%, Wind Speed: {wind} km/h."
    except Exception as e:
        return f"Weather lookup temporary issue: {e}"

@tool
def web_search(query: str) -> str:
    """Search the web for current events, live news, or general information outside Wikipedia."""
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
        return f"Web search returned: {e}. Answer using your internal knowledge or Wikipedia."

    return "No search results found."

@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for encyclopedic facts, people, sports statistics, cricketers, and history."""
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
    
    tools = [get_weather, web_search, wikipedia_search]
    
    # Create the ReAct agent
    agent_executor = create_react_agent(llm, tools)
    return agent_executor

if __name__ == "__main__":
    agent = get_agent()
    print("Backend Agent initialized successfully.")
    print("Testing agent with weather query...")
    response = agent.invoke({"messages": [("user", "what is the weather in surat?")]})
    print("\nResponse:")
    print(response["messages"][-1].content)
