## NutriScan

This repository contains the code for a **minimalist web application that turns your mobile browser into a barcode scanner** for web apps. **No dedicated app is required**; just HTML and JavaScript.

### Overview

NutriScan allows you to scan a product barcode using your smartphone's camera and then redirects you to the corresponding product's page on Open Food Facts to display nutrition information.

[Open Food Facts](https://world.openfoodfacts.org/) is the world's largest open source food database, a sort of Wikipedia of Food. Nutrition information for more than 3.6 million products is available on the OFF website. You can access this data through their website, [API, or as a data dump](https://world.openfoodfacts.org/data).

Open Food Facts employs a nutritional rating system that rewards products rich in beneficial nutrients like [fiber](https://indiafoodstats.blogspot.com/2024/09/a-nutritional-breakdown-high-fibre-foods.html) and [protein](https://indiafoodstats.blogspot.com/2024/09/exploring-high-protein-packaged-foods.html), while penalizing those high in less desirable components such as fats, sugars, and sodium.

My sample code scans an **EAN-13 barcode** from a packaged food product and then fetch its:
*   Name
*   Image
*   Nutri-Score giving an indication of the nutritional quality of a food item
*   Nova classification assigning foods a score from 1 to 4 — where 1 represents unprocessed foods and 4 denotes ultra-processed foods

using the **Open Food Facts REST API**.

### Key Features

*   **Barcode Scanning:** Utilises HTML5 and JavaScript to access the mobile device's camera and scan barcodes directly within the browser.
*   **Open Food Facts Integration:** Redirects to Open Food Facts to display detailed nutrition information for the scanned product or fetches product details via the Open Food Facts REST API.
*   **Minimalist Design:** The code is **deliberately kept lean** to demonstrate the minimum amount of code required for a functional app.
*   **Low Data Transfer:** The total data transferred to and from the app is less than 400kb.
*   **No App Required:** Eliminates the need for users to install a dedicated barcode scanner app.

### How to Use

1.  **Access the Web App:** Open the [NutriScan web page](https://mvark.pages.dev/NutriScan) in your mobile browser.
2.  **Scan Barcode:** The app will request access to your device's camera. Grant permission and scan the barcode of a packaged food product.
3.  **View Information:** The app will display the product's name, image, Nutri-Score, and Nova grouping.

### Code Structure

The repository includes:

*   HTML file with the basic structure of the web page.
*   JavaScript code to handle camera access, barcode scanning, and data retrieval from Open Food Facts.
*   The code for the JavaScript file [html5-qrcode.min.js](https://github.com/mebjas/html5-qrcode/blob/master/minified/html5-qrcode.min.js) can be copied from Minhaz's GitHub repository, which hosts the HTML5 QR Code & Barcode Scanner JavaScript library.

### Troubleshooting

During development I discovered that there were instances where `nova_group` and `nutriscore_grade` fields in the JSON were missing from the API response. This was causing an error. With the help of GitHub Copilot & remote debugging through the Android device, I identified & fixed the issue.

### Credits

*   Utilises Minhaz's HTML5 QR Code & Barcode Scanner JavaScript library.
*   Powered by the Open Food Facts API.

### Related

*   [HOW TO Turn Your Mobile Browser into a Barcode Scanner for Web Apps](https://mvark.blogspot.com/2024/01/how-to-turn-your-mobile-browser-into.html)
