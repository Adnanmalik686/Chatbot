import streamlit as st
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key='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')

# Set up the Streamlit page
st.title("🤖 Adnan Chatbot")
st.write("Welcome to a chatbot powered by Groq and Llama3!")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Banking Quiries"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        # Prepare the chat context
        chat_context = [
            {"role": m["role"], "content": m["content"]} 
            for m in st.session_state.messages
        ]
        
        # Create completion with specified parameters
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=chat_context,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Stream the response
        full_response = st.write_stream(
            (chunk.choices[0].delta.content or "" for chunk in completion)
        )
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})