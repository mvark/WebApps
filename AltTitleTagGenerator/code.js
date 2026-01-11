function generateImageDescription(imageUrl) {
  const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
  if (!apiKey) throw new Error("GEMINI_API_KEY not found in Script Properties.");

  // 1. Fetch image with a standard User-Agent to avoid blocks
  const fetchOptions = {
    "headers": { "User-Agent": "Mozilla/5.0 (Windows) Chrome/120.0.0.0" },
    "muteHttpExceptions": true
  };
  const response = UrlFetchApp.fetch(imageUrl, fetchOptions);
  if (response.getResponseCode() !== 200) throw new Error("Image fetch failed: " + response.getResponseCode());

  const imageBlob = response.getBlob();
  const base64Image = Utilities.base64Encode(imageBlob.getBytes());
  const contentType = imageBlob.getContentType();

  // 2. Prepare Gemini API Request
  // Using 2.0-flash for maximum stability
  //const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
   const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=${apiKey}`;
  
  // Revised prompt to ensure key consistency
  const prompt = "Analyze this image. Provide: 1) A descriptive ALT text (max 125 chars) and 2) A helpful TITLE tooltip. Return ONLY a JSON object with keys 'altText' and 'titleText'.";

  const payload = {
    "contents": [{
      "parts": [
        { "inline_data": { "mime_type": contentType, "data": base64Image } },
        { "text": prompt }
      ]
    }],
    "generationConfig": { "response_mime_type": "application/json" }
  };

  const apiResponse = UrlFetchApp.fetch(apiUrl, {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(payload)
  });

  const fullResult = JSON.parse(apiResponse.getContentText());
  
  // Robust check for content
  if (!fullResult.candidates || !fullResult.candidates[0].content.parts[0].text) {
    throw new Error("AI returned an empty response. Check image safety/size.");
  }

  const rawText = fullResult.candidates[0].content.parts[0].text;
  
  // Cleanup: Sometimes AI adds markdown ```json blocks even in JSON mode
  const cleanJson = rawText.replace(/```json|```/g, "").trim();
  const parsed = JSON.parse(cleanJson);

  // Fallback values if keys are missing
  const finalAlt = parsed.altText || parsed.alt || "No description available";
  const finalTitle = parsed.titleText || parsed.title || "No tooltip available";

  // 3. Log to History
  logToSheet(imageUrl, finalAlt, finalTitle);

  return { altText: finalAlt, titleText: finalTitle };
}

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const result = generateImageDescription(data.imageUrl);
    
    // Return formatted string for the Bookmarklet prompt
    return ContentService.createTextOutput(JSON.stringify({ 
      "success": true, 
      "data": "ALT: " + result.altText + "\nTITLE: " + result.titleText 
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
  const testUrl = '[https://picsum.photos/id/237/400/300.jpg](https://picsum.photos/id/237/400/300.jpg)';
  Logger.log('🚀 Testing...');
  try {
    const res = generateImageDescription(testUrl);
    Logger.log('✅ ALT: ' + res.altText);
    Logger.log('✅ TITLE: ' + res.titleText);
  } catch (e) { Logger.log('❌ ' + e.toString()); }
}
