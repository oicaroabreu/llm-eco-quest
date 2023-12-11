import streamlit as st
from litellm import completion

st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
    {
        "role": "system",
        "content": "The world needs a Solarpunk revolution! Let's exchange some ideas?",
    },
    {"role": "assistant", "content": "What do you know about Solarpunk?"},
]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

response = completion(
        model="ollama/llama2",
        messages=st.session_state.messages,
        api_base="http://localhost:11434",
        max_tokens=50,
    )
output = response.choices[0].message.content
# Display assistant response in chat message container
with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
        st.markdown(output)
        
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": output})

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
