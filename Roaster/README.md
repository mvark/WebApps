## GitHub User Roaster with Perplexity AI's Sonar 

**What is it?**
A playful Streamlit app that analyzes a GitHub user’s recent public commits—highlighting coding patterns, quirky commit messages, and even emojis—and then uses Perplexity AI’s Sonar model to deliver a sharp, humorous “roast” of the user. 

The idea was suggested in this [GitHub blog post](https://github.blog/open-source/for-the-love-of-code-2025/)

---

## Features

* Fetches a GitHub user’s latest 30 public events and extracts commit messages.
* Scans commit messages for emojis and patterns to amp up AI humor.
* Crafts a custom prompt incorporating commit details and emoji usage.
* Uses Sonar (Perplexity AI) to generate a hilarious roast.
* Built with **Streamlit**, with secrets (like the API key) safely stored via **Streamlit Cloud settings**—so nothing sensitive ends up in your codebase.

---

## How to Deploy on Streamlit Community Cloud (Free)

Follow these simple steps to get your own live version up and running:

### 1. Add Your Code to GitHub

Ensure your project is in a public GitHub repo and includes:

* `app.py` – the Streamlit entry script
* `requirements.txt` – list of dependencies (`requests`, etc.) - optional
* `README.md` – this file

### 2. Add a `requirements.txt` File (optional)

Include all Python libraries your app uses—e.g.:

```
requests
streamlit
```

*(Streamlit is pre-installed on Community Cloud, but you can pin a version if needed)*
([Streamlit Docs][1])

### 3. Sign In to Streamlit Community Cloud

Go to [share.streamlit.io](https://share.streamlit.io) and authenticate with your GitHub account.
([Streamlit Docs][2])

### 4. Connect Your Repository

Click **“New app”**, then:

* Select your GitHub repo
* Choose the branch (like `main`)
* Point to `app.py` as the entry file

### 5. Set Up Secrets

Before deploying:

* Go to App Settings and then the **Secrets** section in the Cloud UI
* Add your `SONAR_API_KEY` so it’s kept secure (outside of your code)

### 6. Deploy the App

Click **“Deploy”**—your app will build and go live in minutes.
([Streamlit Docs][3])

### 7. Iterate Easily

Push updates to GitHub—Streamlit Cloud auto-deploys the latest version!


---

## Quick Start Example

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/your-roaster-app.git
   cd your-roaster-app
   ```

2. **Prepare `requirements.txt`**

   ```
   requests
   streamlit
   ```

3. **Push changes**

4. **Deploy on Streamlit Cloud**

5. **Set your `SONAR_API_KEY`** in the UI

6. **Visit your live app** and enjoy the roast!

---

## Disclaimer

Remember to **revoke or rotate** your Sonar API key if ever exposed. Always store sensitive keys in **Streamlit Cloud secrets**, not in public code!

---

## TL;DR

This app blends GitHub data through its API with AI fun, housed in a sleek one-click deployable Streamlit interface. Whether for laughs or developer introspection, let the roast begin!

[1]: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies "App dependencies for your Community Cloud app - Streamlit"
[2]: https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started "Get started with Streamlit Community Cloud"
[3]: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app "Prep and deploy your app on Community Cloud - Streamlit Docs"

