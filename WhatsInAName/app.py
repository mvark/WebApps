from flask import Flask, render_template_string, request
import requests

# Initialize the Flask app
app = Flask(__name__)

# Define a simple HTML form as a string (no separate HTML file used)
HTML = """
<!doctype html>
<title>Sonar Name Facts</title>
<h1>Discover Interesting Things About a Name</h1>
<form method="post">
  Enter a name: <input name="name" required>
  <input type="submit" value="Get Fun Fact">
</form>
{% if fact %}
<hr>
<h2>Result:</h2>
<p>{{ fact }}</p>
{% endif %}
"""

# Function to call the Sonar API with the user-entered name
def query_sonar(name):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_SONAR_API_KEY",  # Replace with your actual API key
        "Content-Type": "application/json"
    }
    prompt = f"Share some interesting origins, meanings, or cultural facts about the name '{name}'."
    data = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "You are a fun and informative assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }

    try:
        # Make the POST request to the Sonar API
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print("SONAR API STATUS CODE:", response.status_code)
        print("SONAR API RAW RESPONSE:", response.text)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response and extract the message content
        result = response.json()
        answer = result.get('choices', [{}])[0].get('message', {}).get('content', 'Sorry, try again!')
        return answer

    except Exception as e:
        # Print error details and return message for user
        print("Error calling Sonar API:", e)
        return f"Error: {e}"

# Main route to handle GET (show form) and POST (process name)
@app.route("/", methods=["GET", "POST"])
def index():
    fact = None
    if request.method == "POST":
        name = request.form["name"].strip()
        if name:
            fact = query_sonar(name)
    return render_template_string(HTML, fact=fact)

# Run the app locally
if __name__ == "__main__":
    app.run()
