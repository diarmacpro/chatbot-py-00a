import streamlit as st
from services.gemini_client import send_to_gemini_with_key
from utils.session_manager import init_session, add_message, load_chat, save_chat
import uuid
from pathlib import Path
from utils.prompt_builder import build_gemini_prompt

st.set_page_config(page_title="Chatbot Gemini", page_icon="🤖")
st.title("🤖 Chatbot Gemini")

# --- STEP 0: Inisialisasi session ---
if "session_loaded" not in st.session_state:
    st.session_state["session_loaded"] = False
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "user_uuid" not in st.session_state:
    st.session_state["user_uuid"] = None
if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = None

# --- STEP 1: Logout Button (hanya muncul jika sudah login) ---
if st.session_state.get("session_loaded", False):
    if st.button("Logout"):
        st.session_state.clear()  # hapus semua session
        st.stop()  # hentikan eksekusi agar form login muncul

# --- STEP 2: Form Login (hanya muncul jika belum login) ---
if not st.session_state["session_loaded"]:
    with st.form("login_form"):
        user_id = st.text_input("User ID (tanpa spasi/simbol)").strip()
        api_key = st.text_input("Gemini API Key", type="password").strip()
        submitted = st.form_submit_button("Login")

        if submitted:
            if not user_id or not api_key:
                st.warning("User ID dan API Key wajib diisi.")
            else:
                # buat UUID dari user_id
                user_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, user_id))
                st.session_state["user_uuid"] = user_uuid
                st.session_state["gemini_api_key"] = api_key

                # load chat lama jika ada
                st.session_state["messages"] = load_chat(user_uuid)
                st.session_state["session_loaded"] = True
                st.stop()  # hentikan eksekusi agar form login hilang dan chat muncul

# --- STEP 3: Chat Interface (hanya muncul jika sudah login) ---
if st.session_state.get("session_loaded", False):
    init_session()

    # tampilkan chat sebelumnya
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])

    # input chat user
    if prompt := st.chat_input("Ketik pesan...", key=f"chat_input_{st.session_state['user_uuid']}"):
        add_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        # build prompt untuk Gemini
        prompt_text = build_gemini_prompt(st.session_state["messages"], prompt)
        response = send_to_gemini_with_key(prompt_text, st.session_state["gemini_api_key"])

        # simpan dan tampilkan balasan
        add_message("assistant", response)
        with st.chat_message("assistant"):
            st.markdown(response)

        # simpan ke JSON session
        save_chat(st.session_state["user_uuid"], st.session_state["messages"])
