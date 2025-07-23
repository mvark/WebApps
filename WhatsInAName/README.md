# Whats In A Name – Fun Facts About Names Using AI

This is a simple Flask app that uses the **Sonar API from Perplexity.ai** to fetch interesting, cultural, and historical facts about names.

> Enter a name, get a fun fact. That’s it!

## Features

- Accepts any name via a web form
- Queries Perplexity's Sonar model with a custom prompt
- Returns fun, interesting insights about names
- Simple HTML form, no frontend framework required

## Demo Screenshot

![screenshot](screenshot.png) <!-- You can upload a screenshot if needed -->

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/whatsinaname.git
cd whatsinaname
````

### 2. Install dependencies

```bash
pip install flask requests
```

### 3. Set your Sonar API key

Edit `app.py` and replace:

```python
"Authorization": "Bearer YOUR_SONAR_API_KEY"
```

with your actual API key from [Perplexity AI](https://www.perplexity.ai).

### 4. Run the app

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## Example Output

> Name: **Aria**
> Fact: *"The name Aria has multiple origins. In Italian, it means 'air' or a melody. In Hebrew, it means 'lioness'. It has gained popularity due to its musical connotations and appearance in fantasy series."*

---

## Technologies Used

* Python 3
* Flask
* Requests
* Sonar API from Perplexity.ai

---

## 📄 License

MIT License. Try it out and share your feedback

