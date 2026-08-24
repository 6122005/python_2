import streamlit as st
from core_v2 import get_agent
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

st.set_page_config(page_title="Smart Research Assistant v2", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ Smart Research Assistant v2")
st.markdown("This assistant is powered by a **LangGraph Agent** equipped with **DuckDuckGo** and **Wikipedia** tools.")
st.markdown("---")

# Initialize chat history and agent in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = get_agent()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
            if "reasoning" in message:
                with st.expander("View Agent's Reasoning & Tool Usage"):
                    for step in message["reasoning"]:
                        st.write(step)

# React to user input
if prompt := st.chat_input("Ask me anything... (e.g., What is the weather in Paris?)"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking and searching..."):
            try:
                # Invoke the agent
                response = st.session_state.agent.invoke({"messages": [("user", prompt)]})
                
                reasoning_steps = []
                
                # Extract the reasoning steps to show in expander! (Day 63 requirement)
                with st.expander("View Agent's Reasoning & Tool Usage"):
                    for msg in response["messages"]:
                        if isinstance(msg, HumanMessage):
                            continue # Skip showing user prompt again
                        
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tc in msg.tool_calls:
                                step = f"🔧 **Tool Call:** `{tc['name']}`\n\n📥 **Input:** `{tc['args']}`"
                                st.write(step)
                                st.markdown("---")
                                reasoning_steps.append(step)
                        elif isinstance(msg, ToolMessage):
                            step = f"📤 **Tool Output:** {msg.content[:300]}..." # truncate for display
                            st.write(step)
                            st.markdown("---")
                            reasoning_steps.append(step)
                
                final_answer = response["messages"][-1].content
                st.markdown(final_answer)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": final_answer,
                    "reasoning": reasoning_steps
                })
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
