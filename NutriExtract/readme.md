# Nutri-Extract: Browser-Side AI Nutrition Extractor

**Nutri-Extract** is a zero-install, single-file web application that leverages Google’s **Gemini 2.5 Flash** to perform Optical Character Recognition (OCR) on nutrition labels. It transforms a simple image URL into a structured data table without requiring a dedicated backend server.

![NutritionTableExtractor](https://github.com/user-attachments/assets/ad9d3625-7cef-48e8-be18-9f578bc5a91d)

## 🚀 Key Features

* **Serverless Architecture**: Runs entirely in the browser using ES modules.
* **Gemini 2.5 Flash Integration**: Uses the latest high-efficiency model for rapid extraction.
* **Structured JSON Output**: Automatically maps messy label text to clean keys like `energy-kcal`, `proteins`, and `fat`.

---

## 🛠️ How It Works (Technical Breakdown)

### 1. SDK Integration

The app uses an `importmap` to load the `@google/generative-ai` library directly from a CDN (esm.run). This allows the script to remain a single file without needing `npm install` or a build step.

### 2. Image Processing

When a URL is provided, the app performs the following steps:

1. **Fetch**: It attempts to download the image as a Blob.
2. **Conversion**: Uses `FileReader` to encode the blob into a **Base64 string**, which is the format Gemini’s `inlineData` requires.
3. **Transmission**: Sends the Base64 data and a specific prompt to the Gemini API.

### 3. Prompt Engineering

The system uses a strict prompt to force Gemini to return **only** a JSON object. It explicitly instructs the AI to:

* Extract values specifically for **100g/100ml**.
* Ignore units (e.g., return `450` instead of `450kcal`).
* Handle missing data by returning `null`.

---

## Code Walkthrough 

### 1. The "Zero-Install" Library Import

```javascript
<script type="importmap">
  {
    "imports": {
      "@google/generative-ai": "https://esm.run/@google/generative-ai"
    }
  }
</script>
<script type="module">
  import { GoogleGenerativeAI } from "@google/generative-ai";
</script>

```

* **The Statement:** The `importmap` acts like a "phone book" for the browser.
* **The Detail:** Usually, to use Google's AI library, you would need to use `npm` and a bundler. By using `esm.run`, you are telling the browser to download the library as a modern ES Module. The `type="module"` in the second script tag is mandatory; without it, the `import` statement would cause a syntax error.

### 2. The Binary Image Pipeline

Because the Gemini API doesn't "visit" the URL you provide, the browser has to download the image and package it for transport.

```javascript
const blob = await fetch(imgUrl).then(res => res.blob());

```

* **The Statement:** This fetches the image and converts it into a `Blob` (Binary Large Object).
* **The Detail:** A Blob is the raw, unencoded data of the file. We need this because we need to know the `mimeType` (e.g., `image/jpeg`) to tell Gemini what it is looking at.

```javascript
const reader = new FileReader();
reader.onloadend = () => resolve(reader.result.split(',')[1]);
reader.readAsDataURL(blob);

```

* **The Statement:** This converts the binary Blob into a Base64 string.
* **The Detail:** `readAsDataURL` creates a string that starts with `data:image/png;base64,...`. Gemini only wants the raw code *after* the comma. The `.split(',')[1]` is a surgical strike to remove that header, leaving only the pure data.

### 3. The "Instructional" Prompt

```javascript
const prompt = `Extract nutritional values per 100g. 
                Return ONLY a JSON object with these keys: 
                "energy-kcal", "proteins", "carbohydrates"...`;

```

* **The Statement:** This is the "System Instruction."
* **The Detail:** You aren't just asking for text; you are defining the **Schema**. By listing the exact keys you want, you ensure the AI doesn't give you "Protein" one time and "Proteins" (plural) the next. This consistency is what makes the automatic table-filling possible later.

### 4. Sending the Multimodal Request

```javascript
const result = await model.generateContent([
    prompt,
    { inlineData: { data: base64Data, mimeType: blob.type } }
]);

```

* **The Statement:** This sends the text and the image bytes in one single array.
* **The Detail:** This is the definition of **Multimodal**. The AI doesn't "read" the label and then "answer" the prompt separately. It uses the prompt as a lens through which it views the image data.

### 5. The "Markdown" Sanitizer

```javascript
const text = result.response.text().replace(/```json|```/g, "").trim();
const data = JSON.parse(text);

```

* **The Statement:** This strips out formatting marks and turns text into a JavaScript Object.
* **The Detail:** LLMs are trained to be chatty. Even when told "ONLY JSON," they often wrap the answer in "code blocks" (backticks).
* The Regex `/```json|```/g` looks for those backticks and removes them globally.
* `JSON.parse()` takes the cleaned string and turns it into a live object that code can interact with.



### 6. Mapping the Object to the UI

```javascript
for (const [key, value] of Object.entries(data)) {
    html += `<tr>
        <td style="text-transform: capitalize;">${key.replace('-', ' ')}</td>
        <td>${value || 'N/A'}</td>
    </tr>`;
}

```

* **The Statement:** This iterates through every piece of data Gemini found.
* **The Detail:** * `Object.entries(data)` turns your JSON into a list of pairs.
* `${key.replace('-', ' ')}` takes a technical key like `saturated-fat` and makes it human-readable as `saturated fat`.
* `${value || 'N/A'}` is a "fallback." If the AI returned `null` for a missing value, it displays "N/A" instead of an empty box.

### ⚠️ Note 

The most "fragile" line in the code is:
`const blob = await fetch(imgUrl).then(res => res.blob());`

This line is the "CORS Trigger." If a user tries an image from a site like Amazon or Walmart, the browser's security policy will stop the code right there. Adding a "File Upload" button (using `<input type="file">`) would bypass this because the file comes from the user's hard drive, not a foreign server.


## ⚠️ Important Limitations 

### 1. The CORS Wall

Most modern websites block other websites from "stealing" their images via `fetch`. If you try to use an image from a site like Amazon or a news outlet, the browser will likely throw a **CORS Error**.

* **Solution**: This app works best when images are hosted on a service with open CORS (like Imgur) or when the file is run from a local development server.

### 2. API Key Security

This app handles your `GEMINI_API_KEY` in **plain text** on the client side.

* **Warning**: Never host this publicly with your key hardcoded. Only use this for local development or private tools. If you share the link to your hosted version, anyone who inspects the page can potentially see how you handle data.

### 3. Image URL vs. File Upload

The current code relies on a URL. For a better user experience on GitHub, consider adding a `<input type="file">` so users can upload photos directly from their phones, which bypasses the CORS issue entirely.

---

## 📖 Setup

1. Clone the repository or download `nutriextract.html`.
2. Open the file in any modern web browser.
3. Generate an API Key at [Google AI Studio](https://aistudio.google.com/).
4. Paste your key, provide a CORS-compliant image URL, and click **Extract**.
