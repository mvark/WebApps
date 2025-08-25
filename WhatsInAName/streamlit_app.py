import streamlit as st
import requests
import os

# Read Groq API key from Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def query_groq(name: str) -> str:
    """Query Groq API with a prompt about a given name"""
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not found. Please add it in Streamlit secrets."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Share some interesting origins, meanings, or cultural facts about the name '{name}'. Keep it fun and conversational."

    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": "You are a fun and informative assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "No response found.")
    except Exception as e:
        return f"Error calling Groq API: {e}"

# -------------------- Streamlit UI --------------------

st.title("🔤 What's in a Name? (Groq-powered)")

name = st.text_input("Enter a name:")

if st.button("Get Fun Fact"):
    if name.strip():
        with st.spinner("Asking Groq..."):
            result = query_groq(name.strip())
        st.success("Here’s what I found:")
        st.write(result)
    else:
        st.warning("Please enter a name to continue.")
