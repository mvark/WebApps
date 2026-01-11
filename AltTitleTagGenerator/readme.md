# 🏷️ Alt & Title Tag Generator

A lightweight, serverless tool that uses the **Gemini 2.0 Flash / Gemini 2.5 Flash Lite API ** to automatically generate SEO-friendly `ALT` text and helpful `TITLE` tooltips for any image on the web. 

This project uses a **JavaScript Bookmarklet** (frontend) and a **Google Apps Script Web App** (backend). 

---

## 🚀 How It Works
1. **Activate:** Click the bookmarklet on any webpage.
2. **Select:** Click on the image you want to describe.
3. **Analyze:** The backend fetches the image and sends it to Gemini 2.0 Flash.
4. **Result:** A dialog box appears with the generated tags, ready to be copied into your HTML or CMS.



---

## 🛠️ Setup Instructions

### 1. Backend: Google Apps Script
1. Go to [script.google.com](https://script.google.com) and create a **New Project**.
2. Delete any existing code and paste the content of `Code.gs` from this repository.
3. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
4. In the Apps Script editor, go to **Project Settings** (gear icon) > **Script Properties** and add:
   - **Property:** `GEMINI_API_KEY`
   - **Value:** `YOUR_ACTUAL_API_KEY`
5. Click **Deploy > New Deployment**.
   - **Type:** Web app
   - **Execute as:** Me
   - **Who has access:** Anyone
6. **Copy the Web App URL** (Example: `https://script.google.com/.../exec`).

### 2. Frontend: Bookmarklet
1. Create a new bookmark in your browser (Ctrl+D / Cmd+D).
2. Right-click the new bookmark and select **Edit**.
3. For the **URL**, paste the single-line code below, replacing `YOUR_APPS_SCRIPT_URL` with your deployment URL from the previous step.

```javascript
javascript:(function(){const s='YOUR_APPS_SCRIPT_URL';alert('✓ Image Mode Active\n\nClick any image.');document.body.style.cursor='crosshair';const h=function(e){if(e.target.tagName==='IMG'){e.preventDefault();e.stopPropagation();const u=e.target.src;e.target.style.outline='4px solid #4285f4';fetch(s,{method:'POST',body:JSON.stringify({imageUrl:u})}).then(r=>r.json()).then(j=>{if(j.success){prompt('AI Tags Generated:',j.data)}else{alert('AI Error: '+j.error)}}).catch(a=>alert('Network Error: '+a));document.body.style.cursor='';document.removeEventListener('click',h,true)}};document.addEventListener('click',h,true)})();
```

## Features
- Zero-Storage: No Google Sheets or databases are required; it processes everything in real-time.

- Robust Parsing: Automatically handles and strips Markdown code blocks if the AI includes them in the response.

- User-Agent Spoofing: Includes headers to ensure images are fetched successfully from sites with bot protection.

- Error Handling: Provides clear feedback if the API quota is reached or if an image fails to load.

## Code Sample Adapted to work with AllenAI Molmo 2 8B model via OpenRouter

The code sample openrouter-code.gs uses OpenRouter with the AllenAI Molmo 2 8B model. The main changes to the Gemini Flash sample are the API endpoint, authentication headers, and request/response format.

I'll adapt the code to use OpenRouter with the AllenAI Molmo 2 8B model. The main changes are the API endpoint, authentication headers, and request/response format.

```javascript name=code.js
function generateImageDescription(imageUrl) {
  const apiKey = PropertiesService.getScriptProperties().getProperty('OPENROUTER_API_KEY');
  if (!apiKey) throw new Error("OPENROUTER_API_KEY not found in Script Properties.");

  // 1. Fetch image with a standard User-Agent to avoid blocks
  const fetchOptions = {
    "headers": { "User-Agent": "Mozilla/5.0 (Windows) Chrome/120.0.0.0" },
    "muteHttpExceptions": true
  };
  const response = UrlFetchApp.fetch(imageUrl, fetchOptions);
  if (response.getResponseCode() !== 200) throw new Error("Image fetch failed:  " + response.getResponseCode());

  const imageBlob = response.getBlob();
  const base64Image = Utilities.base64Encode(imageBlob. getBytes());
  const contentType = imageBlob.getContentType();

  // 2. Prepare OpenRouter API Request
  const apiUrl = "https://openrouter.ai/api/v1/chat/completions";
  
  // Revised prompt to ensure key consistency
  const prompt = "Analyze this image. Provide: 1) A descriptive ALT text (max 125 chars) and 2) A helpful TITLE tooltip. Return ONLY a JSON object with keys 'altText' and 'titleText'.";

  const payload = {
    "model": "allenai/molmo-2-8b:free",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image_url",
            "image_url": {
              "url": `data:${contentType};base64,${base64Image}`
            }
          },
          {
            "type": "text",
            "text": prompt
          }
        ]
      }
    ],
    "response_format": { "type": "json_object" }
  };

  const apiResponse = UrlFetchApp. fetch(apiUrl, {
    "method": "post",
    "headers": {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      "HTTP-Referer": "https://your-app-domain.com", // Optional: Add your domain
      "X-Title":  "Alt Title Tag Generator" // Optional: Your app name
    },
    "payload":  JSON.stringify(payload),
    "muteHttpExceptions": true
  });

  const fullResult = JSON.parse(apiResponse.getContentText());
  
  // Check for errors
  if (fullResult.error) {
    throw new Error(`OpenRouter API error: ${fullResult.error.message || JSON.stringify(fullResult.error)}`);
  }

  // Robust check for content
  if (!fullResult.choices || !fullResult. choices[0] || !fullResult.choices[0].message || !fullResult.choices[0].message.content) {
    throw new Error("AI returned an empty response. Check image safety/size.");
  }

  const rawText = fullResult.choices[0].message.content;
  
  // Cleanup: Sometimes AI adds markdown ```json blocks even in JSON mode
  const cleanJson = rawText.replace(/```json|```/g, "").trim();
  const parsed = JSON.parse(cleanJson);

  // Fallback values if keys are missing
  const finalAlt = parsed.altText || parsed.alt || "No description available";
  const finalTitle = parsed.titleText || parsed. title || "No tooltip available";

  // 3. Log to History
  logToSheet(imageUrl, finalAlt, finalTitle);

  return { altText: finalAlt, titleText: finalTitle };
}

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const result = generateImageDescription(data.imageUrl);
    
    // Return formatted string for the Bookmarklet prompt
    return ContentService.createTextOutput(JSON. stringify({ 
      "success":  true, 
      "data":  "ALT: " + result. altText + "\nTITLE: " + result.titleText 
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ 
      "success": false, 
      "error": err.toString() 
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function logToSheet(url, alt, title) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    if (ss) ss.getSheets()[0].appendRow([new Date(), url, alt, title]);
  } catch (e) { Logger.log("Sheet log failed: " + e.message); }
}

function testImageDescription() {
  const testUrl = 'https://picsum.photos/id/237/400/300.jpg';
  Logger.log('🚀 Testing...');
  try {
    const res = generateImageDescription(testUrl);
    Logger.log('✅ ALT: ' + res.altText);
    Logger.log('✅ TITLE: ' + res.titleText);
  } catch (e) { Logger.log('❌ ' + e. toString()); }
}
```

## Key Changes:

1. **API Key**: Changed from `GEMINI_API_KEY` to `OPENROUTER_API_KEY`
2. **API Endpoint**: Now using `https://openrouter.ai/api/v1/chat/completions`
3. **Request Format**: Converted to OpenAI-compatible format with: 
   - `messages` array with role/content structure
   - `image_url` with base64 data URI
   - `response_format` for JSON output
4. **Headers**: Added Authorization header and optional HTTP-Referer/X-Title
5. **Response Parsing**: Updated to handle OpenRouter's response structure (`choices[0].message.content`)
6. **Error Handling**: Added check for OpenRouter-specific error responses

## Setup Instructions:

1. Get an API key from [OpenRouter](https://openrouter.ai/)
2. In Google Apps Script:  **File > Project Settings > Script Properties**
3. Add property: `OPENROUTER_API_KEY` with your key
4. Update the `HTTP-Referer` in the headers with your actual domain (optional but recommended)
5. Run `testImageDescription()` to verify it works

Note: The Molmo model is free but may have rate limits. Check [OpenRouter's documentation](https://openrouter.ai/docs) for current limits. 

To get an API key from OpenRouter.ai, follow these steps:

## Step-by-Step Instructions

1. **Create an Account**
   - Visit [openrouter.ai](https://openrouter.ai).
   - Click "Sign up" or "Sign in" using an email, wallet, or third-party authentication (Google, GitHub, etc.)[[1]](https://lumetrium.com/definer/wiki/sources/ai/api-keys/openrouter)[[2]](https://www.apideck.com/blog/how-to-get-your-openrouter-api-key)[[3]](https://docs.themeisle.com/article/2391-openrouter-setup-guide).

**Add Credits**
   - OpenRouter typically requires prepaid credits before generating API keys.
   - Go to the "Credits" section and add funds; a minimum amount (like $5) may be required[[2]](https://www.apideck.com/blog/how-to-get-your-openrouter-api-key).

2. **Access the Keys Section**
   - After logging in, find the "Keys" or "API Keys" section in your account menu or by visiting [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys)

4. **Generate a New API Key**
   - Click the "Create Key" button. 
   - Give your key a recognizable name (optional, but helpful for organization).
   - Confirm and create the key.

5. **Secure Your API Key**
   - Store your key in a password manager, encrypted note, or environment variable.
   - Never share your API key publicly or commit it to version control. Treat it as confidential information

6. **Test Your API Key (Optional)**
   - You can test your key with a sample `curl` request:
     ```bash
     curl https://openrouter.ai/api/v1/chat/completions \
       -H "Authorization: Bearer YOUR_API_KEY_HERE" \
       -H "Content-Type: application/json" \
       -d '{ "model": "meta-llama/llama-3.1-8b-instruct:free", "messages": [{"role": "user", "content": "Hello"}] }'
     ```
   - Replace `YOUR_API_KEY_HERE` with your actual key.

## Extra Tips

- **For the Molmo model specifically**:  The `allenai/molmo-2-8b: free` model is marked as free, so you might be able to use it without adding credits, but creating an account and API key is still required.

## Adding to Google Apps Script

Once you have your API key: 
1. In your Google Apps Script editor, go to **Project Settings** (gear icon)
2. Scroll to **Script Properties**
3. Click **Add script property**
4. Name: `OPENROUTER_API_KEY`
5. Value: Paste your OpenRouter API key
6. Click **Save**

Now your code will be able to access it using `PropertiesService.getScriptProperties().getProperty('OPENROUTER_API_KEY')`.
