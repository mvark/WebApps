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
