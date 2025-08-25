import streamlit as st
import requests
import os

# Read API key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def query_groq(name: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": "You are a fun and informative assistant."},
            {"role": "user", "content": (
                f"Share some interesting origins, meanings, "
                f"or cultural facts about the name '{name}'."
            )}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=20)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        return f"Groq API error {resp.status_code}: {resp.text}"

# Streamlit UI
st.title("What's in a Name? (via Groq)")
name = st.text_input("Enter a name:")
if st.button("Get Fun Fact"):
    if name.strip():
        with st.spinner("Consulting Groq..."):
            result = query_groq(name.strip())
        st.markdown(f"**Fun Fact:**\n\n{result}")
    else:
        st.error("Please enter a name!")
