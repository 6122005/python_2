import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

def main():
    load_dotenv()
    
    # Initialize the Groq LLM using LangChain
    # "openai/gpt-oss-20b" is the model we verified works on Groq
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7)
    
    print("Welcome to the LangChain Chatbot (Day 56)!")
    print("Type 'quit' or 'exit' to end the chat.")
    print("-" * 50)
    
    # Keep track of chat history
    chat_history = [
        SystemMessage(content="You are a helpful AI assistant. Keep answers concise and friendly.")
    ]
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Chat ended. Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        # Add user's message to history
        chat_history.append(HumanMessage(content=user_input))
        
        try:
            # Call the LLM
            response = llm.invoke(chat_history)
            
            # Print response
            print(f"AI: {response.content}")
            
            # Add AI's response to history
            chat_history.append(response)
            
        except Exception as e:
            print(f"Error communicating with LLM: {e}")

if __name__ == "__main__":
    main()
