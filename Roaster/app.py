import streamlit as st
import requests
import re
import os
import json

# Read the Sonar API key from environment variables
API_KEY = os.environ.get("SONAR_API_KEY")
SONAR_API_URL = "https://api.perplexity.ai/chat/completions"  # Updated API endpoint

def get_github_commits(username):
    url = f"https://api.github.com/users/{username}/events/public"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None, f"GitHub API error {response.status_code}: {response.text}"

        events = response.json()
        commits = []
        emojis = []
        for event in events:
            if event["type"] == "PushEvent":
                for commit in event["payload"]["commits"]:
                    msg = commit["message"]
                    commits.append(msg)
                    emojis += re.findall(r'[:;][\-~]?[)D]', msg)  # Basic smiley match
        return commits, emojis
    except requests.exceptions.RequestException as e:
        return None, f"GitHub API request failed: {e}"

def prepare_prompt(username, commit_count, sample_commits, emojis):
    emojis_text = ", ".join(set(emojis)) if emojis else "none"
    sample_msgs = "; ".join(sample_commits[:3]) if sample_commits else "No commit messages available."
    prompt = (f"Roast GitHub user '{username}' based on {commit_count} recent commits. "
              f"Sample commit messages: {sample_msgs}. "
              f"Use the following emojis found in commit messages: {emojis_text}. "
              "Create a humorous roast including these details with creative, witty lines.")
    return prompt

def query_sonar_api(prompt):
    if not API_KEY:
        return "Error: SONAR_API_KEY environment variable not found."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    payload = {
        "model": "sonar",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(SONAR_API_URL, headers=headers, json=payload)
        
        # Debug info - Uncomment these lines to log request and response details
        # st.write("Request Payload:", json.dumps(payload, indent=2))
        # st.write("Response Status:", response.status_code)
        # st.write("Response Text:", response.text)

        if response.status_code == 200:
            data = response.json()
            # Adjust the path to extract the generated content according to actual API response format
            # Example with OpenAI-style response format:
            return data.get("choices", [{}])[0].get("message", {}).get("content", "No response content.")
        else:
            return f"Sonar API error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Sonar API request failed: {e}"

st.title("GitHub User Roaster with Perplexity AI's Sonar 🔥")

username = st.text_input("Enter a GitHub username")

if st.button("Roast!"):
    if not username:
        st.warning("Please enter a username!")
    else:
        with st.spinner("Fetching data and getting AI roast..."):
            commits, emojis_or_error = get_github_commits(username)
            if commits is None:
                st.error(emojis_or_error)
            else:
                commit_count = len(commits)
                prompt = prepare_prompt(username, commit_count, commits, emojis_or_error)
                roast = query_sonar_api(prompt)
                st.markdown(f"🤖 **AI Roast:**\n\n{roast}")
