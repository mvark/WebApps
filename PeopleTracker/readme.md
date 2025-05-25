  # People Tracker Bookmarklet

This simple bookmarklet allows you to quickly save the URL, title, and your personal notes about any webpage (like a social media profile) directly into a Google Sheet. It's a quick way to keep track of people or resources you encounter online. It is adapted from a previous [bookmarklet that acts as a replacement for the now deprecated Google Bookmarks](https://mvark.blogspot.com/2021/05/bookmarker-bookmarklet.html)

## How it Works

The system consists of two parts:

1.  **Google Apps Script Web App:** This script runs on Google's servers. It acts as an endpoint that receives data (URL, Title, Notes) sent by your bookmarklet and appends it as a new row to a designated Google Sheet.
2.  **Browser Bookmarklet:** A small piece of JavaScript code saved as a bookmark in your browser. When you click it, it extracts the current page's URL and title, prompts you for notes, and then sends all this information to your Google Apps Script Web App.

## Features

* **Quick Capture:** Save page details and notes with a single click and a few keystrokes.
* **Google Sheet Storage:** All data is stored neatly in a Google Sheet for easy organization and access.
* **Cross-Browser Compatible:** Works in most modern web browsers.
* **Simple Setup:** Easy to configure with your own Google Sheet.

## Setup & Configuration Guide

Follow these steps to set up your People Tracker bookmarklet:

### Step 1: Prepare Your Google Sheet

1.  Go to [Google Sheets](https://docs.google.com/spreadsheets/) and create a **new blank spreadsheet**.
2.  Name it something like "People Tracker Data" or whatever you prefer.
3.  **Important: Get your Spreadsheet ID.** Look at the URL of your new spreadsheet. The ID is the long string of characters between `/d/` and `/edit`.
    Example URL: `https://docs.google.com/spreadsheets/d/THIS_IS_YOUR_ID_GOES_HERE/edit#gid=0`
4.  **Share Your Spreadsheet for Editor Access:**
    * Click the **"Share"** button (top-right corner of the sheet).
    * Under "General access," change "Restricted" to **"Anyone with the link."**
    * Make sure the permission is set to **"Editor."** This allows your Apps Script to write data to the sheet.
    * Click "Done."

### Step 2: Set up the Google Apps Script Web App

This script will receive data from your bookmarklet and write it to your Google Sheet.

1.  Go to [Google Apps Script](https://script.google.com/) and sign in with your Google account.
2.  Click **"New project."**
3.  Delete any existing code in the `Code.gs` file.
4.  Paste the following code into the `Code.gs` file:

    ```javascript
    function doGet(request) {
      // REPLACE 'VQK-VL7c63gWgDa-wp85LpdA' with YOUR Google Sheet ID
      var ss = SpreadsheetApp.openByUrl("https://docs.google.com/spreadsheets/d/<GOOGLE_SHEETS_KEY>/edit");
      var sheet = ss.getSheets()[0]; // Gets the first sheet

      // Define headers for your columns.
      var headers = ["Timestamp", "URL", "Title", "Notes"];

      // Check if headers exist in the sheet, if not, create them
      if (sheet.getLastRow() === 0) {
        sheet.appendRow(headers);
      }

      var rowData = [];
      for (var i = 0; i < headers.length; i++) {
        var header = headers[i];
        if (header === "Timestamp") {
          rowData.push(new Date());
        } else if (request.parameter[header.toLowerCase()]) { // Use .toLowerCase() for parameter keys
          rowData.push(request.parameter[header.toLowerCase()]);
        } else {
          rowData.push(''); // Push an empty string if the parameter is not found
        }
      }

      sheet.appendRow(rowData); // Append the collected data as a new row

      // Return a simple success message
      return ContentService.createTextOutput("Record Saved Successfully!")
        .setMimeType(ContentService.MimeType.TEXT);
    }
    ```
5.  **Important:** Replace `<GOOGLE_SHEETS_KEY>` in `openByUrl` with your actual Google Spreadsheet ID that you obtained in Step 1.
6.  **Save the script:** Click the floppy disk icon or go to `File > Save project`.
7.  **Deploy as a Web App:**
    * Click the **"Deploy"** button (top-right) and select **"New deployment."**
    * For "Select type," choose **"Web app."**
    * **Execute as:** Set this to **"Me" (your email address)**. This ensures the script runs with your permissions to write to your sheet.
    * **Who has access:** Set this to **"Anyone."** This is crucial for the bookmarklet to work in any browser, even if you're not signed into your Google account.
    * Click **"Deploy."**
    * The first time, you'll be asked to **authorize** the script. Follow the prompts, grant the necessary permissions (to connect to external service, view/manage Google Sheets).
    * After successful deployment, you will get a **"Web app URL"**. **Copy this URL carefully.** You will need it for the bookmarklet in Step 3. It will look something like `https://script.google.com/macros/s/<YOUR-WEB-APP>/exec`.

    ### Important Security Note:

    By setting "Who has access" to "Anyone," you are making your web app publicly accessible. This means:

    Anyone who gets hold of your Apps Script web app URL can send data to your spreadsheet.
    While they won't know the spreadsheet ID unless you expose it, they can send data to your script.
    For a personal note-taking tool like this, the security risk is generally low, as the script only appends data. However, be aware of this setting for any future, more sensitive Apps Script projects.

     ### Test the Apps Script URL Directly (in a browser):

    * Open a new browser tab.
    * Paste your full Apps Script Web App URL (the one you put in the bookmarklet) into the address bar.
    * Add some dummy parameters to simulate the bookmarklet: YOUR_APPS_SCRIPT_WEB_APP_URL?Name=TestName&Profile_URL=http://example.com&Notes=TestNotes
    * Press Enter.

    What happens?
    * If it works, you should see "Data Saved Successfully!" in the browser window.
    * If you see a Google error page, an "Authorization required" page, or a script error, it indicates a problem with your Apps Script deployment or permissions.



### Step 3: Create Your Browser Bookmarklet

This is the code you'll save in your browser's bookmark bar.

1.  **Copy the Bookmarklet Code:** Copy the entire minified code below:

    ```javascript
    javascript:(function(){var w='https://script.google.com/macros/s/<YOUR-WEB-APP>/exec';var n=prompt('Add your notes for this page:','');if(n===null)return;var p='?url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title)+'&notes='+encodeURIComponent(n);var u=window.open(w+p,'bookmarker');setTimeout(function(){if(u&&!u.closed){u.close();}},3000);})();
    ```
2.  **Customize the Bookmarklet Code:**
    * **Crucial:** In the copied code, replace `https://script.google.com/macros/s/<YOUR-WEB-APP>/exec` with the **actual Web app URL** you obtained in Step 2.
    * **Example:** If your Web App URL was `https://script.google.com/macros/s/ABC/exec`, your bookmarklet code would become:
        ```javascript
        javascript:(function(){var w='https://script.google.com/macros/s/ABC/exec';var n=prompt('Add your notes for this page:','');if(n===null)return;var p='?url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title)+'&notes='+encodeURIComponent(n);var u=window.open(w+p,'bookmarker');setTimeout(function(){if(u&&!u.closed){u.close();}},3000);})();
        ```
3.  **Add to Your Browser Bookmarks:**
    * **Google Chrome:** Right-click on your bookmarks bar > "Add page..." or "Add bookmark..." > Paste the customized code into the "URL" field. Give it a name like "People Tracker."
    * **Mozilla Firefox:** Right-click on your bookmarks toolbar > "New Bookmark..." > Paste the customized code into the "Location" field. Give it a name.
    * **Microsoft Edge:** Right-click on the Favorites bar > "Add new favorite" > Paste the customized code into the "URL" field. Give it a name.
    * **Safari:** Go to `Bookmarks > Add Bookmark`. Then, `Bookmarks > Edit Bookmarks`. Find your new bookmark, right-click it, and select `Edit Address` or `Edit URL`. Paste the code there.

## How to Use the Bookmarklet

1.  Navigate to any webpage (e.g., a social media profile, an interesting article).
2.  Click the "Page Notes Tracker" bookmarklet in your browser's bookmark bar.
3.  A JavaScript `prompt` will appear, asking you to "Add your notes for this page:".
4.  Type your notes and click "OK."
5.  A new, small window/tab will briefly open to send the data to your Google Apps Script. It will attempt to close after 3 seconds (note: this auto-close might not work on all sites/browsers due to security policies).
6.  Check your Google Sheet; a new row should appear with the timestamp, page URL, page title, and your notes!

## Troubleshooting

* **Data not appearing in Google Sheet:**
    * **Check Sheet Sharing:** Ensure your Google Sheet is shared as "Anyone with the link" and "Editor." (Step 1)
    * **Check Apps Script Deployment:** Verify that your Apps Script web app is deployed with "Execute as: Me" and "Who has access: Anyone." (Step 2)
    * **Verify Web App URL:** Double-check that the `webAppUrl` in your bookmarklet code exactly matches the URL from your Apps Script deployment.
    * **Check Apps Script Executions:** Go to your Apps Script project, click the "Executions" tab (left sidebar). Look for failed executions and their error messages. This is your best debugging tool for server-side issues.
    * **Increase `setTimeout`:** The `setTimeout` might be closing the window too fast. Try changing `3000` to `5000` or `10000` (5 or 10 seconds) in your bookmarklet code and re-save it.
* **Bookmarklet not working (SyntaxError or similar):**
    * Ensure you copied the entire minified bookmarklet code without any missing characters, especially at the very beginning or end.
    * Browser bookmark URL limits can sometimes cut off very long code.
* **New window not closing automatically:** This is a known browser security limitation for cross-origin pop-ups. It's often impossible for the originating page's script to close a window that has navigated to a different domain.
* **Content Security Policy (CSP) issues:** While this method (opening a new window) is generally more resilient to CSPs than `Workspace()` or `Image()` tricks, extremely strict CSPs on some sites might still interfere. If you see errors about "refused to open window" in your browser's developer console, this could be the cause.

---
