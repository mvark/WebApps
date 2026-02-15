# ELI5 Text Explainer (OpenRouter)

A **minimal, single-page web app** that takes any text and explains it **“like I’m 5”**, using free large-language models available via **OpenRouter**.

The goal of this project is **simplicity**:

* No frameworks
* No build tools
* Just HTML + JavaScript
* Same code works across multiple models

---

## ✨ What this app does

* Accepts user input text
* Sends it to an LLM with an *ELI5-style prompt*
* Displays a simplified explanation
* Lets you **switch models** to compare outputs

---

## 🧠 Key idea

OpenRouter provides a **unified API** for many models.
As long as you use *chat-style models*, **the request format stays the same**.

👉 To switch models, you only change this line:

```js
model: "mistralai/mistral-7b-instruct"
```

Everything else remains identical.

---

## 📁 Project structure

```
/
├── index.html   # Entire app (HTML + JS)
└── README.md
```

That’s it.

---

## 🚀 How to try it yourself

### 1️⃣ Get an OpenRouter API key

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Sign in
3. Create a free API key

> Free-tier models and quotas may change over time.

---

### 2️⃣ Clone this repo

```bash
git clone https://github.com/your-username/eli5-openrouter.git
cd eli5-openrouter
```

---

### 3️⃣ Add your API key

Open `index.html` and replace:

```js
const API_KEY = "PASTE_YOUR_OPENROUTER_KEY_HERE";
```

with your actual key.

⚠️ **Do not commit real API keys** to public repos in production.

---

### 4️⃣ Open the app

Just open the file in a browser:

```text
index.html
```

No server required.

---

## 🧩 Supported models (examples)

You can switch between models using the dropdown:

```html
<option value="mistralai/mistral-7b-instruct">Mistral 7B</option>
<option value="google/gemma-7b-it">Gemma 7B</option>
<option value="meta-llama/llama-3-8b-instruct">LLaMA 3 8B</option>
```

If a model fails:

* It’s usually quota-related
* Or the model is temporarily unavailable
* The code itself does not need changes

---

## 🧪 How the code works (high-level)

### 1. User input

Text is read from a `<textarea>`.

### 2. Prompt construction

The app sends two messages:

* A **system prompt** that enforces ELI5-style output
* A **user prompt** containing the input text

```js
messages: [
  { role: "system", content: "Explain things like to a 5 year old." },
  { role: "user", content: userText }
]
```

---

### 3. API call

A standard `fetch()` call to OpenRouter’s chat completion endpoint:

```js
fetch("https://openrouter.ai/api/v1/chat/completions", {...})
```

The response is always parsed the same way:

```js
data.choices[0].message.content
```

---

### 4. Output rendering

The simplified explanation is shown inside a `<pre>` block for readability.

---

## 🎯 Why this project is useful

* Demonstrates **model comparison** clearly
* Shows how **one prompt behaves across models**
* Perfect for:

  * Demos
  * Teaching
  * Blog posts
  * Workshops
  * Experiments

---

## ⚠️ Important notes

* This app runs **entirely in the browser**
* API keys are exposed client-side
* This is fine for demos, **not production**

For production use:

* Add a backend proxy
* Or use serverless functions (Cloudflare, Netlify, etc.)

---

## 🔧 Easy extensions

If you want to build on this:

* Side-by-side model comparison
* Auto-load available models from OpenRouter
* Save explanations locally
* Add temperature / length controls

---

## 📜 License

MIT — use it, modify it, share it.
