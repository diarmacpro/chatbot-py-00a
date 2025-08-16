import streamlit as st
import json
from pathlib import Path

CHAT_DB_FOLDER = Path("chat_db")
CHAT_DB_FOLDER.mkdir(exist_ok=True)

def init_session():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

def add_message(role, text):
    st.session_state["messages"].append({"role": role, "text": text})

def get_chat_file(uuid_str: str) -> Path:
    return CHAT_DB_FOLDER / f"chat_db_{uuid_str}.json"

def load_chat(uuid_str: str):
    chat_file = get_chat_file(uuid_str)
    if chat_file.exists():
        return json.loads(chat_file.read_text())
    return []

def save_chat(uuid_str: str, messages):
    chat_file = get_chat_file(uuid_str)
    chat_file.write_text(json.dumps(messages, indent=2))
