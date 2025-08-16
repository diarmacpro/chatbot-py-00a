import requests

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"

def send_to_gemini_with_key(user_message: str, api_key: str) -> str:
    if not api_key:
        return "Error: API_KEY tidak ditemukan"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
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
