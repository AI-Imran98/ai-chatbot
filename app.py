import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Page config
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 AI Chatbot")
st.subheader("Your intelligent AI assistant!")

# System prompt - chatbot personality
SYSTEM_PROMPT = """You are a helpful, friendly, and professional AI assistant.
Answer questions clearly and concisely.
Be polite and professional at all times."""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# Clear chat button
if len(st.session_state.messages) > 0:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# AI response function
def get_ai_response(messages):
    # Build conversation history
    conversation = f"{SYSTEM_PROMPT}\n\n"
    for msg in messages:
        if msg["role"] == "user":
            conversation += f"User: {msg['content']}\n"
        else:
            conversation += f"Assistant: {msg['content']}\n"
    conversation += "Assistant:"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=conversation
    )
    return response.text

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Get AI response
    with st.spinner("AI is thinking..."):
        response = get_ai_response(st.session_state.messages)

    # Show AI response
    st.chat_message("assistant").write(response)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })