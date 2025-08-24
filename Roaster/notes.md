Line-by-line explanation of the code by ChatGPT & Claude Sonnet 4:

---

```python
import streamlit as st
import requests
import re
import os
import json
```

* **Imports** standard Python libraries and modules:

  * `streamlit` — for building the web app interface.
  * `requests` — for making HTTP API calls to GitHub and Sonar APIs.
  * `re` — for regular expressions for finding emoji patterns in commit messages.
  * `os` — for accessing environment variables (API key).
  * `json` — for parsing JSON  data (though not actively used in final code).

```python
API_KEY = os.environ.get("SONAR_API_KEY")
SONAR_API_URL = "https://api.perplexity.ai/chat/completions"  # Updated API endpoint
```

* Retrieves the `SONAR_API_KEY` from environment variables.
* Defines the Sonar API endpoint from Perplexity’s chat completions interface ([Perplexity][1], [Perplexity][2]).

---

```python
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
```

* **Function** to fetch recent public events from GitHub for a given user:

  * Calls GitHub API (`/users/{username}/events/public`).
  * Handles errors if request fails or returns non-200 status.
  * Parses JSON response and initializes empty lists for commits and emojis.
  * Scans for `PushEvent` events and extracts commit messages and simple smiley emoji patterns like :), :-D, ;), etc. using regex.
  * Returns commit list and emojis, or an error message on failure.

---

```python
def prepare_prompt(username, commit_count, sample_commits, emojis):
    emojis_text = ", ".join(set(emojis)) if emojis else "none"
    sample_msgs = "; ".join(sample_commits[:3]) if sample_commits else "No commit messages available."
    prompt = (
        f"Roast GitHub user '{username}' based on {commit_count} recent commits. "
        f"Sample commit messages: {sample_msgs}. "
        f"Use the following emojis found in commit messages: {emojis_text}. "
        "Create a humorous roast including these details with creative, witty lines."
    )
    return prompt
```

* **Function** to build a prompt for Sonar AI:
  * Creates comma-separated unique emoji list and formats emojis.
  * Picks first 3 sample commit messages.
  * Constructs AI prompt with user data for generating a humorous "roast".

---

```python
def query_sonar_api(prompt):
    if not API_KEY:
        return "Error: SONAR_API_KEY environment variable not found."
```

* Checks if the API key is available. If not, returns an error.

```python
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
```

* Sets up headers with Bearer authorization and JSON content type.

```python
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
```

* Formats the API payload according to Perplexity’s chat-completion design, which is compatible with OpenAI format ([Perplexity][2]).
  
  * Uses `"sonar"` model.
  * Includes system and user messages.
  * Sets parameters for randomness and response length.
  * temperature: 0.7: Controls creativity/randomness
  * max_tokens: 500: Limits response length

```python
    try:
        response = requests.post(SONAR_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "No response content.")
        else:
            return f"Sonar API error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Sonar API request failed: {e}"
```

* Sends POST request to the Sonar endpoint.
* If successful, extracts content from the first choice (`message.content`) akin to OpenAI's format ([Perplexity][2]).
* Handles HTTP or request errors with messages. Commented debug code for troubleshooting.

---

```python
st.title("GitHub User Roaster with Perplexity AI's Sonar 🔥")
username = st.text_input("Enter a GitHub username")
```

* Sets Streamlit app title.
* Creates a text input field for the GitHub username.

```python
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
                st.markdown(f"🤖 AI Roast:\n\n{roast}")
```

* On button click, triggers the Roast flow:

  * Validates that username isn't empty.
  * Shows a loading spinner while fetching data and waiting for AI response.
  * Retrieves commit data and emojis.
  * Prepares the AI prompt and queries the Sonar API.
  * Displays either an error or the generated roast as Markdown.

---

### Summary 

* This app creates a fun tool that analyzes a GitHub user's recent commits and uses AI to 
generate a humorous "roast" based on their coding patterns, commit messages, and emoji usage!

* **User input → API flow → output**: Streamlit provides input and renders output.
* **GitHub API**: Fetches commit messages and emojis for context.
* **Prompt engineering**: Builds a creative instruction prompt combining metadata.
* **Perplexity Sonar API**: Generates a witty roast using OpenAI-compatible chat flows ([Perplexity][1], [Perplexity][2]).
* **Error handling and UI feedback**: Ensures smooth UX with warnings, spinner, and graceful messaging.


[1]: https://docs.perplexity.ai/api-reference/chat-completions-post "Chat Completions - Perplexity"
[2]: https://perplexity.mintlify.app/guides/chat-completions-guide "OpenAI Chat Completions Compatibility - Perplexity"

### Critique

Critique of the GitHub User Roaster Streamlit code:

## **🔴 Critical Issues**

### **1. Ineffective Emoji Detection**
```python
emojis += re.findall(r'[:;][\-~]?[)D]', msg) # Basic smiley match
```
**Problems:**
- Only catches ancient ASCII emoticons like `:)` and `:-D`
- Misses actual Unicode emojis (🚀, 🔥, 💻) that developers actually use
- Very limited pattern matching

**Fix:**
```python
import emoji
emojis += emoji.extract_emojis(msg)  # Gets actual emojis
# Or use a broader regex for modern emojis
emojis += re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]', msg)
```

### **2. Poor Error Handling**
```python
if commits is None:
    st.error(emojis_or_error)
```
**Problem:** Using the same variable (`emojis_or_error`) for both emojis list and error messages is confusing and error-prone.

**Fix:**
```python
commits, error_msg = get_github_commits(username)
if commits is None:
    st.error(error_msg)
else:
    emojis = extract_emojis_from_commits(commits)
```

## **🟡 Design & Performance Issues**

### **3. GitHub API Rate Limiting**
**Problem:** No handling of GitHub's rate limits (60 requests/hour for unauthenticated)

**Fix:**
```python
headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
response = requests.get(url, headers=headers)
```

### **4. Limited Data Scope**
**Problem:** Only looks at recent public events (last ~30), missing older commits and private repos

**Fix:** Consider using GitHub's commits API endpoint for specific repos:
```python
url = f"https://api.github.com/users/{username}/repos"
# Then fetch commits from each repo
```

### **5. Hard-coded Limits**
```python
sample_msgs = "; ".join(sample_commits[:3])
"max_tokens": 500
```
**Problem:** Magic numbers without explanation

**Fix:**
```python
SAMPLE_COMMIT_LIMIT = 3
MAX_TOKENS = 500
sample_msgs = "; ".join(sample_commits[:SAMPLE_COMMIT_LIMIT])
```

## **🟢 Code Quality Issues**

### **6. Inconsistent Naming**
- `emojis_or_error` - confusing dual-purpose variable
- Mixed naming conventions

### **7. Missing Input Validation**
```python
if not username:
    st.warning("Please enter a username!")
```
**Problem:** Doesn't validate if username format is valid

**Fix:**
```python
if not username or not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-])*[a-zA-Z0-9]$', username):
    st.warning("Please enter a valid GitHub username!")
```

### **8. No Caching**
**Problem:** Every button click makes fresh API calls

**Fix:**
```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_github_commits(username):
    # existing code
```
Using @st.cache_data (Streamlit v1.18+) would reduce redundant calls for the same user input. 

## **🔧 Improvement Suggestions**

### **9. Better User Experience**
```python
# Add user avatar and basic info
user_info = get_github_user_info(username)  # New function
col1, col2 = st.columns([1, 3])
with col1:
    st.image(user_info['avatar_url'])
with col2:
    st.write(f"**{user_info['name']}** (@{username})")
    st.write(f"Repos: {user_info['public_repos']}")
```

### **10. More Robust Prompt Engineering**
```python
def prepare_prompt(username, commits_data, user_info):
    # Include more context: repo languages, commit frequency, etc.
    context = analyze_coding_patterns(commits_data)
    # Create more sophisticated prompt
```

### **11. Security & Configuration**
```python
# Use st.secrets instead of environment variables
API_KEY = st.secrets.get("perplexity_api_key")

# Add configuration options
with st.sidebar:
    roast_intensity = st.slider("Roast Intensity", 1, 10, 5)
    include_repos = st.checkbox("Include repository names", True)
```

## **📊 Overall Assessment**

**Strengths:**
- ✅ Clean, functional structure, simple UI
- ✅ Good use of Streamlit features (spinner, markdown). 
- ✅ Basic error handling structure (st.warning, and st.error)
- ✅ Prompt formatting and reuse - prepare_prompt consolidates prompt creation logic in one place

**Weaknesses:**
- ❌ Very limited emoji detection
- ❌ No caching or performance optimization
- ❌ Missing input validation

**Recommendation:** This is a fun prototype, but needs significant refactoring for production use. Focus on fixing the API naming confusion and improving the emoji detection first, as these directly impact user experience.
