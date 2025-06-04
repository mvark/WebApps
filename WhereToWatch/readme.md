# Where To Watch 🍿

A simple HTML + JavaScript-based tool to search for movies using the TMDB API, and check their streaming availability on popular Indian OTT platforms like Netflix, Prime Video, SonyLIV, Hotstar, and Zee5.

---

## 📊 Features

* Minimal, responsive UI with basic styling
* Search by movie title
* Sort results by release date (newest first)
* Display poster, overview, rating, and streaming platforms (India-specific, but can be changed)
* Direct links to streaming search pages
* Handles empty results and API errors

---

## 🔧 Getting Started

1. Clone this repo or copy the HTML file.
2. Get a free API key from [TMDB](https://www.themoviedb.org/).
3. Replace `API_KEY` in the script section with your own TMDB API key.
4. Open the HTML file in any modern web browser on mobile or desktop.

---

## ⚙️ How It Works

### HTML Structure

* **Search input & button**: Allows users to enter a movie title.
* **Results container**: Displays search results with thumbnails and provider links.

### JavaScript Breakdown

#### 1. **API Configuration**

```js
const API_KEY = 'YOUR_API_KEY_HERE'; // Replace with your TMDB key
const BASE_URL = 'https://api.themoviedb.org/3';
```

#### 2. **Event Listeners**

```js
searchButton.addEventListener('click', searchContent);
searchInput.addEventListener('keypress', (event) => {
  if(event.key === 'Enter') searchContent();
});
```

Allows users to trigger a search by clicking the button or pressing Enter.

#### 3. **searchContent()**

* Fetches movie data from TMDB based on search input
* Sorts by release date (newest first)
* Limits results to 20 items
* Calls `displayContentDetails()` for each movie

#### 4. **displayContentDetails(item)**

* Fetches provider data for each movie
* Filters for Indian streaming providers
* Displays title, year, rating, overview, poster, and "Watch on" links

#### 5. **getProviderLink(provider, title)**

* Maps known provider names to their respective search URLs
* Returns HTML anchor elements pointing to those services

---

## ⚠️ Limitations

* No support for TV shows or regional filtering outside India
* No pagination; limited to first 20 search results
* Relies on TMDB "flatrate" provider data (may not be always up to date)
* Movie details & Runtime are not displayed to make page load fast with essential info
* Requires valid TMDB API key to function

---

## 🚀 Potential Improvements

* Add support for TV shows and series
* Add pagination or infinite scroll
* Include movie details like cast, runtime and genres
* Cache results locally for performance
* Enhance UI with loading spinners or themes

---

## ✉️ License & Attribution

* This project uses [TMDB API](https://developers.themoviedb.org/3) under their terms of use.
* Icons and streaming links are inferred using open provider names.
* No backend required.

---

Enjoy exploring your favorite movies and where to watch them!
