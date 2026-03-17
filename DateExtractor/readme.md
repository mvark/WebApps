# Price & Expiry Date AI Extractor

A lightweight, single-file web application that uses **Google Gemini AI** to extract and validate retail data from photos of packaged food. 

## 🚀 Features

* **Multimodal Extraction:** Extracts Mfg Date, Expiry Date, MRP, and Unit Sale Price from image URLs.
* **Automatic Logic Validation:** Detects and corrects swapped dates (e.g., if Mfg Date is listed after Expiry Date).
* **Expiry Countdown:** Automatically calculates days remaining until expiry and flags expired items in red.
* **Minimalist Design:** Built with vanilla HTML/JavaScript and CSS—no complex build tools required.

## 🛠️ Prerequisites

* A **Google Gemini API Key**. You can get one for free at [Google AI Studio](https://aistudio.google.com/).
* A modern web browser (Chrome, Edge, or Safari).

## 📋 How to Use

1.  **Download the Code:** Save the `index.html` file to your computer.
2.  **Open in Browser:** Double-click the file to open it in your preferred browser.
3.  **Enter API Key:** Paste your Gemini API key into the top input field.
4.  **Provide Image URL:** Paste a direct URL to an image of a food package (e.g., from an e-commerce site or Imgur).
5.  **Extract:** Click the **"Extract & Validate Data"** button.

## ⚠️ Important Note on CORS

This application uses the `fetch()` API to grab images from URLs. Many websites block direct access to their images (CORS policy). 
* **For local testing:** Use images from open sources like GitHub or Imgur.
* **For production:** In a real-world scenario, you would route these requests through a proxy server to bypass CORS restrictions.

## ⚙️ Technical Details

* **Model:** `gemini-2.5-flash`
* **Tech Stack:** HTML5, CSS3, JavaScript (ES Modules)
* **API:** `@google/generative-ai` SDK via ESM

---
*Developed as a utility for smart shopping and pantry management.*
