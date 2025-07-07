# 🎬 BingeBuddy

A light weight web application for searching movies, TV shows, and celebrities with streaming availability in India. Co-created with GitHub Copilot using vanilla JavaScript and powered by The Movie Database (TMDB) API.

## ✨ Features

### 🔍 Multi-Modal Search
- **Movies & TV Shows**: Search across both content types simultaneously
- **Celebrity Search**: Find actors, directors, producers, and other film personalities
- **Smart Sorting**: Results sorted by popularity for better relevance

### 🎭 Rich Content Details
- **Comprehensive Info**: Release dates, runtime, seasons/episodes, ratings
- **Cast & Crew**: Interactive cast and crew listings with clickable names
- **Plot Summaries**: Overviews and synopses

### 📺 Streaming Integration
- **India-Specific**: Shows streaming availability for Indian platforms:
  - Netflix
  - Amazon Prime Video
  - Disney+ Hotstar
  - Sony LIV
  - ZEE5
  - JioCinema
  - Aha Video

### 🔗 External References
- **TMDB Integration**: Direct links to The Movie Database pages
- **Cross-Navigation**: Click on cast/crew names to explore their filmography

### 📱 Responsive Design
- **Mobile-First**: Optimized for all screen sizes
- **Touch-Friendly**: Easy navigation on mobile devices
- **Fast Loading**: Efficient API calls and image optimization

## 🚀 Quick Start

### Prerequisites
- Modern web browser with JavaScript enabled
- TMDB API key (free registration at [themoviedb.org](https://www.themoviedb.org/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/movie-search-app.git
   cd movie-search-app
   ```

2. **Configure API Key**
   
   Open `show.html` and replace the API key:
   ```javascript
   const API_KEY = 'your_tmdb_api_key_here';
   ```

3. **Launch the Application**
   
   Simply open `show.html` in your web browser:
   ```bash
   # Using a local server (recommended)
   python -m http.server 8000
   # Then visit http://localhost:8000/show.html
   
   # Or open directly
   open show.html
   ```

## 🎯 Usage

### Basic Search
1. Select search type: "Movies & TV Shows" or "Celebrity"
2. Enter your search term
3. Press Enter or click "Search"
4. Browse through the results

### Advanced Features
- **Cast/Crew Navigation**: Click on any cast or crew member's name to search for their other works
- **Content Discovery**: Click on movie/show titles in celebrity profiles to search for that content
- **Streaming Access**: Click on streaming service badges to go directly to the content

### Search Examples
```
Movies & TV Shows:
- "Parasite" → Find Bong Joon-ho's acclaimed film
- "Breaking Bad" → Discover the complete TV series

Celebrity:
- "Christopher Nolan" → Explore the director's filmography
- "Priyanka Chopra" → View the actress's movies and shows
```

## 🛠️ Technical Details

### Architecture
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **API**: The Movie Database (TMDB) REST API
- **Styling**: Modern CSS with Flexbox and Grid
- **Images**: Responsive image loading with fallbacks

### API Endpoints Used
- `search/multi` - Multi-content search
- `search/movie` - Movie-specific search
- `search/tv` - TV show search
- `search/person` - Celebrity search
- `movie/{id}` - Detailed movie information
- `tv/{id}` - Detailed TV show information
- `person/{id}` - Celebrity details and filmography
- `{type}/{id}/watch/providers` - Streaming availability

### Performance Optimizations
- **Lazy Loading**: Content loaded progressively
- **Error Handling**: Graceful degradation for API failures
- **Caching**: Browser caching for repeated searches
- **Responsive Images**: Optimized image sizes

## 🔧 Configuration

### Environment Variables
```javascript
// In show.html
const API_KEY = 'your_tmdb_api_key_here';
const BASE_URL = 'https://api.themoviedb.org/3';
const IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w92';
```

### Customization Options
- **Result Limits**: Modify `slice(0, 50)` to change number of results
- **Image Sizes**: Update `IMAGE_BASE_URL` for different image resolutions
- **Streaming Services**: Add new platforms in `getProviderLink()` function

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **[The Movie Database (TMDB)](https://www.themoviedb.org/)** - For providing the comprehensive movie and TV database API
- **[Streaming Services]** - For making content accessible through their platforms
- **[Open Source Community]** - For inspiration and best practices

---

**⭐ Star this repository if you found it helpful!**
