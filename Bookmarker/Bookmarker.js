//Code to be used within Google App Script. 
//For detailed steps, refer to this link - https://mvark.blogspot.com/2021/05/bookmarker-bookmarklet.html

function doGet(request) {
  var ss = SpreadsheetApp.openByUrl("https://docs.google.com/spreadsheet/ccc?key=<GOOGLE_SHEETS_KEY>");
  var sheet = ss.getSheets()[0];
  var headers = ["Timestamp", "URL", "Title", "Category"];
  
  var nextRow = sheet.getLastRow(); 
  var cell = sheet.getRange('A1');
  var col = 0;
  
  for (var i in headers) {
    var val;
    if (headers[i] == "Timestamp") {
      val = new Date(); // Store current timestamp
    } else if (headers[i] == "Category") {
      val = categorizeURL(request.parameter.url); // Call function to categorize the URL
    }
    else {
      //val = request.parameter.URL; // Get URL from request
      val = request.parameter[headers[i]];
    }
    cell.offset(nextRow, col).setValue(val);
    col++;
  }
  
  return ContentService.createTextOutput(request.parameter.url)
         .setMimeType(ContentService.MimeType.TEXT);
}

// Function to categorize the URL using Gemini API
function categorizeURL(url) {
  var apiKey = "YOUR_GEMINI_API_KEY";  // Replace with your actual API key
  var categories = ["News", "Technology", "Entertainment", "Education", "Finance", "Health", "Sports","Misc"]; // Define categories
  
  var endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText?key=" + apiKey;
  
  var promptText = "Analyze the following URL and determine the best matching category from this list: " +
                   categories.join(", ") + ". Categorize as Misc if exact match is not found. Only return the category name, nothing else. URL: " + url;
  
  var payload = {
    "prompt": { "text": promptText }
  };
  
  var options = {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(payload)
  };

  try {
    var response = UrlFetchApp.fetch(endpoint, options);
    var json = JSON.parse(response.getContentText());
    return json.candidates[0].content.trim();  // Extract category from API response
  } catch (e) {
    Logger.log("Error with API call: " + e.toString());
    return "Unknown"; // Fallback in case of an error
  }
}


// Function to categorize the URL using Gemini API
function categorizeURL(url) {
  var apiKey = "YOUR_GEMINI_API_KEY";  // Replace with your actual API key
  var categories = ["News", "Technology", "Entertainment", "Education", "Finance", "Health", "Sports","Misc"]; // Define categories
  
  var endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText?key=" + apiKey;
  
  var promptText = "Analyze the following URL and determine the best matching category from this list: " +
                   categories.join(", ") + ". Categorize as Misc if exact match is not found. Only return the category name, nothing else. URL: " + url;
  
  var payload = {
    "contents": [
      {
        "parts": [
          { "text": promptText }
        ]
      }
    ]
  };
  
  var options = {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(payload)
  };

  try {
    var response = UrlFetchApp.fetch(endpoint, options);
    var json = JSON.parse(response.getContentText());
    
    // Updated to match Gemini API response format
    if (json.candidates && json.candidates[0] && json.candidates[0].content) {
      return json.candidates[0].content.parts[0].text.trim();
    } else {
      return "Misc"; // Default if structure is unexpected
    }
  } catch (e) {
    Logger.log("Error with API call: " + e.toString());
    return "Unknown"; // Fallback in case of an error
  }
}
