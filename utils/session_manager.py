import streamlit as st

def init_session():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

def add_message(role, text):
    st.session_state["messages"].append({"role": role, "text": text})
