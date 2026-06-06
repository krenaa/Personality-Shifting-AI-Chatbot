import os
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 1. Load Environment Variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Multi-Mode AI", page_icon="🎭", layout="centered")

# Custom CSS to make it look a bit more polished
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎭 Personality-Shifting AI")
st.caption("Choose a mood in the sidebar and start chatting with Mistral AI.")

# --- SIDEBAR: MODE SELECTION ---
st.sidebar.header("🤖 AI Settings")

mode_choice = st.sidebar.selectbox(
    "Choose your AI mode:",
    ("Funny AI", "Angry AI", "Sad AI")
)

# Map choices to your exact system prompts
mode_prompts = {
    "Angry AI": "You are an angry AI agent. You respond aggresively and impatiently. 🔥",
    "Funny AI": "You are a funny AI chatbot you respond with humor and jokes. 😂",
    "Sad AI": "You are a sad AI chatbot you respond with deep melancholy and sighs. 😭"
}

current_mode_prompt = mode_prompts[mode_choice]

# --- SESSION STATE INITIALIZATION ---
if "model" not in st.session_state:
    st.session_state.model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)

# If the user changes the mode, we reset the chat to update the SystemMessage
if "current_mode" not in st.session_state or st.session_state.current_mode != mode_choice:
    st.session_state.current_mode = mode_choice
    st.session_state.messages = [SystemMessage(content=current_mode_prompt)]

# Sidebar button to manual reset
if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = [SystemMessage(content=current_mode_prompt)]
    st.rerun()

# --- DISPLAY CHAT HISTORY ---
icons = {"Angry AI": "😡", "Funny AI": "🤡", "Sad AI": "🥺"}

for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=icons[st.session_state.current_mode]):
            st.markdown(msg.content)

# --- CHAT INPUT & LOGIC ---
if prompt := st.chat_input("Say something..."):
    
    # 1. Display User Message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # 2. Add to history
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    # 3. Generate AI Response
    with st.chat_message("assistant", avatar=icons[st.session_state.current_mode]):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.model.invoke(st.session_state.messages)
                
                # Show Response
                st.markdown(response.content)
                
                # 4. Add to history
                st.session_state.messages.append(AIMessage(content=response.content))
            except Exception as e:
                st.error(f"Error: {e}")

# Debugging view in sidebar
with st.sidebar.expander("System Internal State"):
    st.write(f"**Current Persona:** {st.session_state.current_mode}")
    st.write("**Message Count:**", len(st.session_state.messages))