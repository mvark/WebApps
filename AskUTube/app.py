import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import os
import re

# Read API key securely from Streamlit Cloud Secrets (Settings → Secrets)
API_KEY = os.environ.get("SONAR_API_KEY")
SONAR_API_URL = "https://api.perplexity.ai/chat/completions"

def extract_video_id(url_or_id: str) -> str:
    """Extract a YouTube video ID from a full URL or return the input if it's already an ID."""
    text = url_or_id.strip()
    patterns = [
        r"v=([^&]+)",                          # https://www.youtube.com/watch?v=VIDEO_ID
        r"youtu\.be/([^?&/]+)",               # https://youtu.be/VIDEO_ID
        r"youtube\.com/embed/([^?&/]+)"       # https://www.youtube.com/embed/VIDEO_ID
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(1)
    # If no pattern matched, assume user pasted just the ID
    return text

@st.cache_data(show_spinner=False)
def fetch_transcript(video_id: str):
    """Fetch the transcript using the instance method .fetch()."""
    api = YouTubeTranscriptApi()
    return api.fetch(video_id)

def query_perplexity(prompt: str, transcript_text: str) -> str:
    """Send prompt + transcript to Perplexity Sonar API and return the response text."""
    if not API_KEY:
        return "Error: SONAR_API_KEY not set in Streamlit Secrets."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt}\n\nTranscript:\n{transcript_text}"}
    ]
    payload = {
        "model": "sonar",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        resp = requests.post(SONAR_API_URL, headers=headers, json=payload, timeout=60)
    except requests.RequestException as e:
        return f"Network error calling Sonar API: {e}"

    if resp.status_code == 200:
        return resp.json().get("choices", [{}])[0].get("message", {}).get("content", "No response.")
    else:
        return f"API Error {resp.status_code}: {resp.text}"

# ---------------- Streamlit UI ----------------
st.title("🎥 YouTube Transcript Summarizer (Perplexity Sonar AI)")

video_input = st.text_input("Enter a YouTube URL or Video ID:")
prompt = st.text_area("Your instruction", "Summarize this transcript:")

if st.button("Generate Summary"):
    if not video_input.strip():
        st.warning("Please enter a YouTube URL or video ID.")
    else:
        video_id = extract_video_id(video_input)
        with st.spinner("Fetching transcript..."):
            try:
                transcript = fetch_transcript(video_id)  # <-- uses .fetch() as requested
                # The transcript is typically a list of dicts with 'text'
                transcript_text = "\n".join([chunk.get("text", "") for chunk in transcript])

                if not transcript_text.strip():
                    st.error("Transcript fetched but appears empty.")
                else:
                    st.subheader("Transcript Preview")
                    st.write(transcript_text[:800] + ("..." if len(transcript_text) > 800 else ""))

                    with st.spinner("Asking Sonar AI..."):
                        result = query_perplexity(prompt, transcript_text)

                    st.subheader("AI Result")
                    st.markdown(result)

            except Exception as e:
                st.error(f"Transcript error: {e}")
