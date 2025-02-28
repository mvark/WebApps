## Things Near Me

This repository contains the code for a web application that leverages your browser's geolocation feature to discover and display nearby landmarks. It uses modern JavaScript, so no helper libraries such as jQuery are required. 
It is based on Chris Heilmann's (@codepo8) ["Things Around You"](https://web.archive.org/web/20151230130541/https://developer.mozilla.org/en-US/demos/detail/things-around-you). This version was updated using GitHub Copilot to include a map directly on the webpage using Leaflet.

  
![image](https://github.com/user-attachments/assets/703440fa-74ef-49f1-9066-14100f35961b)

### Overview

Things Near Me utilises the browser's **Geolocation API** to obtain the user's latitude and longitude. 
It then fetches nearby Wikipedia articles using the **Geonames API**, displaying them in a numbered list with brief descriptions and corresponding numbered markers on an 
interactive map.  

![image](https://github.com/user-attachments/assets/89d9e4c2-4188-4b95-b074-c43b573624fd)


### Key Features

*   **Geolocation:** Uses the browser's Geolocation API (`navigator.geolocation.getCurrentPosition`) to determine the user's location. Requires user permission.
*   **Interactive Map:** Employs the Leaflet JavaScript library to display an interactive map with tile-based rendering, marker placement, and popup windows for
  landmark information.
*   **Geonames API Integration:** Fetches nearby Wikipedia articles with titles, summaries, and geographical coordinates using the Geonames API ([https://secure.geonames.org/findNearbyWikipediaJSON](https://secure.geonames.org/findNearbyWikipediaJSON)). A Geonames API username is required.
*   **Responsive Design:** Adapts the layout for different screen sizes using CSS media queries (`@media (max-width: 600px)`) to ensure a consistent user experience on desktop and mobile devices.
*   **Dynamic Content Update:** Uses JavaScript to dynamically update the HTML document with the user's location and the list of nearby articles retrieved from the Geonames API. This involves creating and appending HTML elements to the DOM.

### How to Use

1.  **Enable Geolocation:** To get the app to work, you have to allow the Geolocation feature in your browser. Note that the accuracy of your current location may vary as every browser has its own way of fetching the location coordinates after Geolocation is enabled.
2.  **Explore Landmarks:** The app will display a list of nearby landmarks with descriptions and corresponding markers on the map.

### Code Structure

The repository includes:

*   HTML file with the basic structure of the web page. The JavaScript & CSS code are inline but they can be moved out as external files. The JavaScript code handles geolocation, API requests, map rendering, and dynamic content updates while the minimal CSS aids with styling and responsive design.

### Configuration

To run this app, you will need to:

*   **Replace the Geonames API username** on line 186 in the code with your own. 

### Credits

*   Inspired by Chris Heilmann's (@codepo8) "Things Around You" app.
*   Utilises the Leaflet JavaScript library for the interactive map.
*   Uses the Geonames API for fetching landmark information.
*   Co-created with GitHub Copilot.
