# PhonaTick - A Word List for Confusing Pronunciations

## Description

The English language presents pronunciation challenges, especially for non-native speakers, 
due to its many vowel sounds and silent or extra letters in words. 
**PhonaTick** is a front-end for a list of words with tricky pronunciations (originally [saved in Google Sheets & retrieved using Google Sheets API](https://mvark.blogspot.com/2014/12/track-learn-about-aphonetic-words.html) but now fetched via [a JSON API through Datasette](http://mvark.blogspot.com/2025/03/datasette-open-source-tool-for-data.html)). 
It provides a searchable list of words with their pronunciations, sourced from Google and WordWeb 
(created by physicist Antony Lewis).

## Features

*   **Word List:**  A comprehensive list of English words with confusing pronunciations.
*   **Pronunciation Guide:** Pronunciations are provided using data from Google and WordWeb.
*   **Web Application:**  The word list is accessible through a simple web application.
*   **Data Source:**  The application uses a SQLite database generated from a CSV file.
*   **JSON API:**  The data is exposed as a JSON API for easy access.

## Technologies Used

*   **Datasette:**  Used to convert the CSV file into a SQLite database, and to browse, filter, and explore the data.
*   **Glitch:**  Hosts the Datasette instance and the web application.
*   **GitHub Copilot:**  Used to generate the initial web app code.
*   **Visual Studio Code:** Code editor used for development.
*   **JavaScript:** Used to build the web application.

## Setup and Deployment

1.  **CSV to SQLite:** The word list is stored in a CSV file. This file is converted into a SQLite database using Datasette.
2.  **Datasette Deployment:** The Datasette instance is self-hosted on Glitch. Glitch allows you to host web apps without managing servers.
3.  **Web App Deployment:** The web application is also deployed on Glitch.

## Usage

1.  **Access the Web App:**  The application can be accessed via a [Glitch link](https://cobalt-pie-astronaut.glitch.me/).
2.  **Browse the List:**  Browse the list of words and their pronunciations.
3.  **Explore the Data:**  [The data can be further explored using the Datasette interface](https://rightful-veiled-lyre.glitch.me/data/aphonetic).

## Credits

*   **Data Source:** Google and WordWeb (Antony Lewis)
*   **Original Idea:** Inspired by the challenges of English pronunciation
*   **GitHub Copilot:**  Helped in the rapid development of the web application.

## Author

*   M.V. 'Anil' Radhakrishna ([@mvark](https://github.com/mvark))

## License

This project is open-source.

## Try it out!

You can try out the app on Glitch. Let the author know what you think!
```
