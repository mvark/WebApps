# 🧭 Bookmarklet: Download Selected Text as a Word Document (.doc)

This simple **JavaScript bookmarklet** lets you **select text on any webpage** and instantly **download it as a `.doc` (Word) file** — no extensions, servers, or installations required.  

Also see [related sample](https://github.com/mvark/WebApps/tree/main/ExportAsWord) to use this functionality in a web page


## 🔍 How It Works

When you click the bookmarklet:
1. It checks if any text is selected on the page.  
2. If no text is selected, it shows an alert prompting you to select some.  
3. It then extracts the selected text, strips out any HTML tags, and wraps it inside a minimal HTML document.  
4. Finally, it encodes this document as a Word-compatible `.doc` file and triggers an automatic download.


## ⚙️ How to Use

Copy the entire JavaScript code above.

Create a new bookmark in your browser’s bookmarks bar.

Paste the code into the URL field of the bookmark.

Visit any webpage, select some text, and click your new bookmarklet.

A .doc file containing the selected text will download instantly.

🧾 Example Output

The generated Word document contains:

A title: "Exported Selected Text"

The current date and time

Your selected text, neatly formatted and preserved.

## 📋 Bookmarklet Code

You can copy and save this entire line as the URL of a new browser bookmark:

```javascript
javascript:(function(){function downloadSelectedText(){const selection=window.getSelection();let selectedText=selection.toString().trim();if(selectedText.length===0){alert("Please select some text on the page first!");return}const cleanText=selectedText.replace(/<[^>]*>/g,"");const documentContent=`<!DOCTYPE html><html><head><meta charset='utf-8'></head><body><h1>Exported Selected Text</h1><p>Date: ${new Date().toLocaleString()}</p><hr><div style="font-size: 12pt; margin-top: 15px;"><pre style="font-family: Arial, sans-serif; white-space: pre-wrap;">${cleanText}</pre></div></body></html>`;const dataUri='data:application/msword;charset=utf-8,'+encodeURIComponent(documentContent);const a=document.createElement('a');a.href=dataUri;a.download='Selected_Text_Bookmarklet.doc';document.body.appendChild(a);a.click();document.body.removeChild(a);}downloadSelectedText();})();

