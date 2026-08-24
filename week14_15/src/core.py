import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import data

load_dotenv()

# Initialize LLM
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

def classify_intent(user_input):
    prompt = f"""You are an HR intent router. 
Classify the user's input into one of three categories:
1. "CHECK_BALANCE" (User wants to know how many leaves they have)
2. "APPLY_LEAVE" (User is requesting to take time off)
3. "GENERAL_POLICY" (User is asking a general HR question)

User Input: {user_input}
Category (Output ONLY the category name):"""
    response = llm.invoke([("user", prompt)])
    return response.content.strip().upper()

def extract_days(user_input):
    prompt = f"""Extract the number of days the user wants to take off from their request. 
Output ONLY the integer number of days. If you cannot determine the number of days, output "UNKNOWN".

User Input: {user_input}
Days:"""
    response = llm.invoke([("user", prompt)])
    content = response.content.strip()
    # Safely extract integer
    match = re.search(r'\d+', content)
    if match:
        return int(match.group())
    return None

def generate_response(user_input, system_data):
    prompt = f"""You are VoiceHR, a friendly HR assistant. 
Reply to the user in the same language they spoke to you in (e.g., if they asked in Hinglish, reply in Hinglish).
Be polite and concise.
Use the following system data to formulate your answer:
{system_data}

User Input: {user_input}
Response:"""
    response = llm.invoke([("user", prompt)])
    return response.content.strip()

def process_message(user_input):
    intent = classify_intent(user_input)
    print(f"[Debug] Intent detected: {intent}")
    
    if "CHECK_BALANCE" in intent:
        user_data = data.get_user_data()
        system_data = f"Leave balance is {user_data['leave_balance']} days."
        return generate_response(user_input, system_data)
        
    elif "APPLY_LEAVE" in intent:
        days = extract_days(user_input)
        if not days:
            return generate_response(user_input, "System needs to know exactly how many days they want to apply for. Ask them to clarify.")
        
        success, message = data.apply_leave(days)
        return generate_response(user_input, f"System Message: {message}")
        
    else:
        system_data = "General Policy: Working hours are 9 AM to 5 PM. Overtime is paid at 1.5x. Diwali bonus is 1 month salary."
        return generate_response(user_input, system_data)

def main():
    print("--- VoiceHR Assistant (Terminal Prototype) ---")
    print("Type 'quit' to exit.\n")
    data.init_db()
    
    while True:
        user_input = input("Worker: ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        print("Thinking...")
        response = process_message(user_input)
        print(f"\nVoiceHR: {response}\n")
        print("-" * 40)

if __name__ == "__main__":
    main()
