def build_gemini_prompt(messages, new_user_message):
    """
    messages: list dict dari file JSON, format {role: "user"/"assistant", text: "..."}
    new_user_message: string pesan terbaru dari user
    """
    # 1. Skenario tetap
    prompt = "* skenario : anda adalah seorang customer care dari sebuah toko elektronik, "
    prompt += "dan harus melakukan respons maksimal 2 kalimat, dan seminimal mungkin, "
    prompt += "dengan intonasi hangat dan ramah, serta solutif.\n\n"

    # 2. Konteks percakapan sebelumnya
    prompt += "* konteks perkacapan sebelumnya:\n"
    for msg in messages:
        if msg["role"] == "user":
            prompt += f"user : {msg['text']},\n"
        elif msg["role"] == "assistant":
            prompt += f"model : {msg['text']},\n"

    # 3. Tambahkan pesan terbaru dari user
    prompt += f"\n* lalu user mengirimkan pesan :\n{new_user_message},\n"

    return prompt
