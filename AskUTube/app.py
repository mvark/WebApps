import gradio as gr
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import re

def extract_video_id(input_str):
    """
    Extracts YouTube video ID from either a video ID or full URL.
    """
    # If it's already a clean video ID
    if re.fullmatch(r"[a-zA-Z0-9_-]{11}", input_str):
        return input_str

    # Try extracting from URL
    match = re.search(r"(?:v=|\/)([a-zA-Z0-9_-]{11})", input_str)
    if match:
        return match.group(1)
    return None

def summarize_video(video_input, prompt, api_key):
    video_id = extract_video_id(video_input.strip())
    if not video_id:
        return "❌ Invalid YouTube video ID or URL."

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = "\n".join([t["text"] for t in transcript])
    except Exception as e:
        return f"❌ Error fetching transcript: {e}"

    payload = {
        "model": "sonar-small-online",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}\n\nTranscript:\n{full_text}"}
        ]
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)
        result = response.json()["choices"][0]["message"]["content"]
        return result
    except Exception as e:
        return f"❌ Error calling Sonar API: {e}"

gr.Interface(
    fn=summarize_video,
    inputs=[
        gr.Textbox(label="YouTube Video ID or URL"),
        gr.Textbox(label="Custom Prompt", placeholder="Summarize the video, list key takeaways, etc."),
        gr.Textbox(label="Sonar API Key", type="password"),
    ],
    outputs="text",
    title="🎬 YouTube Q&A with Sonar AI",
    description="Paste a YouTube video ID or full URL, enter a custom prompt, and get a transcript-based answer using Perplexity.ai's Sonar API."
).launch()
