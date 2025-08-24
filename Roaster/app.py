import streamlit as st
import requests
import re
import os

# Read the Sonar API key from environment variables
API_KEY = os.environ.get("SONAR_API_KEY")
SONAR_API_URL = "https://api.perplexity.ai/chat/completions"  

def get_github_commits(username):
    url = f"https://api.github.com/users/{username}/events/public"
    response = requests.get(url)
    if response.status_code != 200:
        return None, "Could not fetch GitHub data. Check username or API limits."

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

def prepare_prompt(username, commit_count, sample_commits, emojis):
    emojis_text = ", ".join(set(emojis)) if emojis else "none"
    sample_msgs = "; ".join(sample_commits[:3]) if sample_commits else "No commit messages available."
    prompt = (f"Roast GitHub user '{username}' based on {commit_count} recent commits. "
              f"Sample commit messages: {sample_msgs}. "
              f"Use the following emojis found in commit messages: {emojis_text}. "
              "Create a humorous roast including these details with creative, witty lines.")
    return prompt

def query_sonar_api(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    json_data = {"query": prompt}
    response = requests.post(SONAR_API_URL, json=json_data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("answer", "No roast generated.")
    else:
        return f"Sonar API error: {response.status_code}"

st.title("GitHub User Roaster with Sonar AI 🔥")

username = st.text_input("Enter a GitHub username")

if st.button("Roast Me!"):
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
                st.write(f"🤖 AI Roast:\n\n{roast}")
