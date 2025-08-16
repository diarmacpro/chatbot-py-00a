import streamlit as st
from services.gemini_client import send_to_gemini
from utils.session_manager import init_session, add_message

st.set_page_config(page_title="Chatbot Gemini", page_icon="🤖")
st.title("🤖 Chatbot Gemini")

# Init session
init_session()

# Tampilkan riwayat chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Input chat user
if prompt := st.chat_input("Ketik pesan..."):
    add_message("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    response = send_to_gemini(prompt)

    add_message("assistant", response)
    with st.chat_message("assistant"):
        st.markdown(response)
