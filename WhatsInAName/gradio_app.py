import gradio as gr
import requests
import os

# Sonar API call function
def query_sonar(name):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ.get('SONAR_API_KEY')}",
        "Content-Type": "application/json"
    }
    prompt = f"Share some interesting origins, meanings, or cultural facts about the name '{name}'."
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "You are a fun and informative assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result.get('choices', [{}])[0].get('message', {}).get('content', 'No answer.')
    except Exception as e:
        return f"Error: {e}"

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 🔮 Fun Facts About Your Name")
    name_input = gr.Textbox(label="Enter a name")
    output = gr.Textbox(label="AI Fun Fact")
    submit = gr.Button("Get Fun Fact")
    submit.click(fn=query_sonar, inputs=name_input, outputs=output)

if __name__ == "__main__":
    demo.launch()
