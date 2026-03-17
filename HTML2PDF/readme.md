# Highlight to PDF ✨

A simple, lightweight, **100% client-side** web tool that lets users highlight any text on the page and export only the highlighted portion as a clean PDF.

No server, no backend, no data sent anywhere — everything runs in the browser!

### Features
- Select any text with your mouse
- One-click conversion to PDF
- Clean, professional-looking output
- Fully offline capable
- Mobile-friendly

### Demo

Just open `index.html` in your browser and try highlighting text!

### How to Use

1. Clone or download the repository
2. Open the `index.html` file in any modern web browser (Chrome, Firefox, Edge, Safari)
3. Highlight any text you want
4. Click the **"Convert Highlighted Text to PDF"** button
5. Your PDF will download automatically!

### How It Works (Simple Explanation)

- Uses the browser's built-in `window.getSelection()` to capture highlighted text
- Creates a temporary styled div with only the selected content
- Uses the popular **html2pdf.js** library to convert that div into a PDF
- Everything happens locally in your browser

### Technologies Used
- HTML5
- CSS3
- Vanilla JavaScript
- [html2pdf.js](https://github.com/eKoopmans/html2pdf.js) (via CDN)

### Want to Customize?

Feel free to:
- Change colors and styling
- Add a title or date to the PDF
- Support multiple highlights
- Save original formatting

---

Made with ❤️ for students, researchers, writers, and anyone who loves highlighting important stuff!
