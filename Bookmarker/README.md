# URL Categorizer
This is a simple web application that categorizes a given URL using the Gemini API.

![urlcat](https://github.com/user-attachments/assets/3a4265f7-e6b6-42a5-9877-dfd128d74771)

## Features

-   Takes a URL as input.
-   Uses the Gemini API to categorize the URL.
-   Displays the categorized result on the page.
-   Handles errors gracefully.
-   Provides a loading indicator while the API call is in progress.

## Technologies Used

-   HTML
-   CSS
-   JavaScript
-   Gemini API

## Setup

1.  Clone the repository or download the `URLCategorizer.html` file.
2.  Open the `URLCategorizer.html` file in a text editor.
3.  Replace `"AI"` with your actual Gemini API key.
    ```javascript
    const apiKey = "YOUR_API_KEY"; // Replace with your actual API key
    ```
4.  Save the file.
5.  Open the `URLCategorizer.html` file in your web browser.

## Usage

1.  Enter a URL in the input field.
2.  Click the "Categorize URL" button.
3.  Wait for the loading indicator to disappear.
4.  The categorized result will be displayed on the page.

## Code Explanation

The JavaScript logic handles the following:

1.  **Getting References to HTML Elements:**
    -   The script gets references to the HTML elements that it needs to manipulate using `document.getElementById()`.
2.  **Event Listener for the Categorize Button:**
    -   An event listener is added to the "Categorize URL" button. When the button is clicked, the provided function is executed.
3.  **Getting the URL and Validating It:**
    -   Inside the event listener, the URL entered by the user is retrieved from the input field, and any leading or trailing whitespace is removed using `trim()`.
    -   A basic validation check is performed to ensure that the URL is not empty and starts with either `http://` or `https://`.
4.  **Showing the Loading Indicator and Hiding Previous Results:**
    -   Before making the API call, the loading indicator is displayed, and any previous results are hidden.
5.  **Making the API Call and Handling the Response:**
    -   The `categorizeURL` function is called with the URL as an argument. This function makes the API call to the Gemini API.
    -   The `try...catch...finally` block is used to handle the API call and any potential errors.
    -   In the `try` block:
        -   The `categorizeURL` function is called, and the returned category is stored in a variable.
        -   The results are updated in the HTML, and the result container is made visible.
    -   In the `catch` block:
        -   If any error occurs during the API call, the error message is displayed in the result container, and the container is styled to indicate an error.
    -   In the `finally` block:
        -   The loading indicator is always hidden, regardless of whether the API call was successful or not.
6.  **`categorizeURL` Function:**
    -   This function constructs the API endpoint, prompt text, and payload.
    -   It then makes the API call using the `fetch` function.
    -   If the API call is successful, it parses the response and returns the category.
    -   If the API call fails, it throws an error.

## API Key Security

**Important:** The API key is currently hardcoded in the client-side JavaScript code. This is a security risk. 
This sample is meant for educational purposes to be tried on a computer locally.
In a production environment, you should move the API call to a backend server to protect your API key.

## Error Handling

The code includes error handling to catch and display any errors that occur during the API call. If an error occurs, an error message is displayed in the result container.

## Dependencies

-   This application requires an API key from the Gemini API. You can get a [free Gemini API key through Google AI Studio](https://aistudio.google.com/apikey). 

## License

[MIT](LICENSE)
