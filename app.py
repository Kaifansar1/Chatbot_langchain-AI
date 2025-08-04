import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os

# Set page layout
st.set_page_config(page_title="LangChain ChatBot", layout="centered")
st.title("🤖 Conversational AI ChatBot (LangChain + OpenAI)")
st.markdown("Ask me anything. I remember what we talked about! 💬")

# Sidebar for OpenAI API key input
st.sidebar.title("🔐 OpenAI Settings")
openai_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

# Store memory and chain in session
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()
if "chat_chain" not in st.session_state and openai_key:
    try:
        os.environ["OPENAI_API_KEY"] = openai_key
        llm = ChatOpenAI(temperature=0.7)
        st.session_state.chat_chain = ConversationChain(llm=llm, memory=st.session_state.memory)
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {str(e)}")

# Chat UI
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("🧑 You:", placeholder="Type your message here and press Enter...")

if user_input and openai_key:
    try:
        response = st.session_state.chat_chain.run(user_input)
        st.session_state.chat_history.append(("🧑 You", user_input))
        st.session_state.chat_history.append(("🤖 Bot", response))
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

# Display chat history
for role, message in st.session_state.chat_history:
    st.markdown(f"**{role}**: {message}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; font-size:13px; color:gray;'>👨‍💻 Built by Kaif Ansari using LangChain, OpenAI & Streamlit with ❤️</p>", unsafe_allow_html=True)
