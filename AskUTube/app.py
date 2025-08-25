import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import os

# Read API key securely from Streamlit Cloud Secrets
API_KEY = os.environ.get("SONAR_API_KEY")

SONAR_API_URL = "https://api.perplexity.ai/chat/completions"


def query_perplexity(prompt, transcript_text):
    """
    Sends a prompt + transcript to the Perplexity Sonar API.
    Returns the API's response.
    """
    if not API_KEY:
        return "Error: SONAR_API_KEY not set in Streamlit Secrets!"

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

    response = requests.post(SONAR_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response.")
    else:
        return f"API Error {response.status_code}: {response.text}"


# ---- Streamlit UI ----
st.title("🎥 YouTube Transcript Summarizer (Perplexity Sonar AI)")

video_url = st.text_input("Enter a YouTube video URL:")
prompt = st.text_area("Enter your instruction (e.g., 'Summarize this transcript:')", 
                      "Summarize this transcript:")

if st.button("Generate Summary"):
    if not video_url:
        st.warning("Please enter a valid YouTube video URL!")
    else:
        try:
            # Extract video ID from URL
            if "v=" in video_url:
                video_id = video_url.split("v=")[1].split("&")[0]
            else:
                st.error("Invalid YouTube URL format. Use a standard YouTube link.")
                st.stop()

            with st.spinner("Fetching transcript and querying Sonar AI..."):
                transcript = YouTubeTranscriptApi().get_transcript(video_id)
                transcript_text = "\n".join([entry["text"] for entry in transcript])

                # Show a preview of transcript
                st.subheader("Transcript Preview")
                st.write(transcript_text[:500] + "...")

                result = query_perplexity(prompt, transcript_text)
                st.subheader("AI Generated Summary")
                st.markdown(result)

        except Exception as e:
            st.error(f"An error occurred: {e}")
