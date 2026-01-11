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
