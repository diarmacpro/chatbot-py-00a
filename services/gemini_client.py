import os
import requests
from dotenv import load_dotenv

load_dotenv()  # baca .env di sini

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
API_KEY = os.getenv("GEMINI_API_KEY")

def send_to_gemini(user_message: str) -> str:
    if not API_KEY:
        return "Error: API_KEY tidak ditemukan"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }
    payload = {
        "contents": [
            {"parts": [{"text": user_message}]}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.text}"

    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "Tidak ada respons dari Gemini."
