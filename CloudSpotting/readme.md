# Hugging Face Vision Inference API Demo

A tiny, dependency-free HTML application that demonstrates how to use the **Hugging Face Inference API** to analyze an image with a large multimodal AI model—directly from the browser.

This project uploads **nothing** to your own server. The selected image is converted to Base64 in the browser and sent directly to a Hugging Face Vision Language Model (VLM), which identifies the cloud and returns structured JSON.

Although this demo identifies **cloud types**, the same approach works for almost any image understanding task.

![License](https://img.shields.io/badge/HTML-100%25-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-yellow)
![](https://img.shields.io/badge/API-Hugging%20Face-orange)

---

## Why this sample?

Most Hugging Face examples focus on Python notebooks, Transformers, or running models locally.

This sample shows something much simpler:

- ✅ Pure client-side JavaScript
- ✅ Single HTML file
- ✅ No Node.js
- ✅ No frameworks
- ✅ No backend
- ✅ No image storage
- ✅ No build tools

Just open the page, select an image, choose a Vision Language Model, and let AI do the rest.

---

## ⚠️ Security Notice

This sample is intentionally designed to be as simple as possible, so the **Hugging Face API token is embedded directly in the JavaScript source**.

**This is NOT suitable for production use.**

Anyone who can access the page can view your API token using the browser's Developer Tools and potentially use your Hugging Face quota.

This sample should therefore be used only:

- ✅ On your local machine
- ✅ For learning and experimentation
- ✅ With a personal API token

Do **not** publish a version containing your real API token to GitHub or deploy it as a public website.

### Production applications

For a production application, the recommended architecture is:

```text
Browser
    │
    ▼
Your Backend / Serverless Function
    │
    ▼
Hugging Face Inference API
```

Your backend stores the API token securely and forwards requests to Hugging Face. The token is never exposed to users.

Keeping the code entirely client-side makes it much easier to understand how the Hugging Face Inference API works, which is why this sample uses that approach.

---

## What is Hugging Face Inference?

Many people know Hugging Face as a repository for downloading machine learning models.

It is also an **Inference Platform**.

Instead of downloading multi-gigabyte models and running them on your own GPU, you simply send an HTTP request to a hosted model.

```text
Browser
      │
      ▼
Image
      │
      ▼
Hugging Face Inference API
      │
      ▼
Vision Language Model
      │
      ▼
JSON Response
```

No GPU.

No CUDA.

No PyTorch.

No TensorFlow.

No machine learning knowledge required.

---

## Vision Language Models (VLMs)

Unlike traditional image classifiers that only return a label, modern Vision Language Models can **understand** an image and answer questions about it.

For example, instead of simply returning:

```
Cirrus
```

the model can explain:

- what cloud it is
- why it thinks so
- how confident it is
- what weather it may indicate
- other plausible matches

This makes VLMs ideal for educational applications.

---

## Sample Prompt

The application asks the model to identify the cloud according to the **World Meteorological Organization (WMO) International Cloud Atlas** and return structured JSON.

Example response:

```json
{
  "predictions": [
    {
      "genus": "Altocumulus",
      "confidence": 94
    },
    {
      "genus": "Cirrocumulus",
      "confidence": 5
    },
    {
      "genus": "Stratocumulus",
      "confidence": 1
    }
  ],
  "weather": "Possible afternoon showers.",
  "reason": "Rounded mid-level cloudlets with slight grey shading."
}
```

The page renders this JSON as a simple HTML report.

---

## Why clouds?

Clouds are an interesting image recognition challenge because many cloud genera look similar.

A Vision Language Model can often explain *why* it prefers one cloud genus over another, making the output far more useful than a simple classifier.

---

## Things you can identify

After trying clouds, simply change the prompt.

Examples include:

- 🌸 Flowers
- 🐦 Birds
- 🍄 Mushrooms
- 🐶 Dog breeds
- 🚗 Vehicles
- 🏛 Landmarks
- 🍕 Food
- 📄 Documents
- 🖼 Paintings
- 📸 Wildlife

The same application works for almost any image understanding task.

---

## Why Hugging Face?

Hugging Face hosts thousands of AI models covering:

- Vision
- NLP
- Speech
- OCR
- Embeddings
- Object Detection
- Image Captioning
- Translation
- Large Language Models

Many of these can be accessed through a simple REST API.

You don't need to know how the model was trained.

Just send an image and receive a result.

---

## Who is this sample for?

This sample is intended for:

- JavaScript developers
- Students
- AI beginners
- Web developers
- Hobbyists
- Anyone curious about AI inference

If you know basic HTML and JavaScript, you already know enough.

---

## Requirements

- A free Hugging Face account
- A Hugging Face API token
- A modern browser

That's it.

---

## Future Ideas

Once you understand the basics, try extending the project:

- Upload images to Supabase
- Save previous analyses
- Compare multiple Vision Language Models
- Drag-and-drop image upload
- Display confidence charts
- Add OCR support
- Detect plants, birds, or insects
- Build a visual search engine

---

## Learn Once, Apply Everywhere

The most valuable takeaway from this sample isn't cloud identification.

It's understanding **AI inference**.

Once you know how to call a hosted model using a simple HTTP request, you can experiment with thousands of open models without worrying about GPUs, CUDA, PyTorch, or machine learning infrastructure.

Change the prompt.

Change the model.

Build something new.

That's the real power of inference.
