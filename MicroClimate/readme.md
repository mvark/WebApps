# Hyderabad Micro Climate Dashboard

A single-file, no-build-step weather dashboard for Hyderabad, built on the [WeatherUnion API](https://www.weatherunion.com/) (Zomato's hyperlocal weather network). Pick any of 40+ 
localities in Hyderabad as checkboxes and 
see live temperature, humidity, wind, and rainfall side by side — plus a map with a coloured dot per locality
showing where it's currently raining.

<img width="1330" height="611" alt="hyderabad-weather" src="https://github.com/user-attachments/assets/af4b9633-e25c-4357-9f40-87fdbb9619be" />


Inspired by [this tweet](https://x.com/un1c0rnioz/status/2084686552299634805) and ICFOSS's 
public [IoT-based Micro Climate Monitoring System](https://space.icfoss.org) for Kerala, whose plain grid layout 
(localities as columns, weather metrics as rows) this project borrows.

## Features

- **Checkbox-driven table** — check a locality to add it as a column, uncheck to remove it. Unchecking never triggers a network call; only genuinely new localities are fetched.
- **Live map** — [Leaflet](https://leafletjs.com/) + OpenStreetMap tiles (both open source, no API key required for the map itself). Each checked locality gets a dot: **blue** if `rain_intensity > 0`, **red** otherwise or if data isn't available yet.
- **Per-locality caching** — weather data for a locality is fetched once and reused until you hit **Refresh**, keeping API usage low.
- **Zero dependencies to install** — it's one HTML file with everything (styling, logic, map) inline. Open it in a browser and it runs.

[View the dashboard](https://mvark.github.io/web/weather_map.html) with your own [WeatherUnion API key](https://www.weatherunion.com/) 

## Getting Started

### Prerequisites

- A **WeatherUnion API key** (the `X-Zomato-Api-Key` header). Request one at [weatherunion.com](https://www.weatherunion.com/) — it's free for personal/non-commercial use at the time of writing, but check their current terms.
- Any modern browser. No server, build tool, or package manager needed.

### Running it

1. Clone or download this repo.
2. Open [`hyderabad_weather_dashboard.html`](https://github.com/mvark/mvark.github.io/blob/main/web/weather_map.html) directly in your browser (double-click it, or `open hyderabad_weather_dashboard.html` / `start hyderabad_weather_dashboard.html` depending on OS).
3. Paste your API key into the **X-Zomato-Api-Key** field at the top.
4. Check any localities you're interested in — the default selection is Miyapur, Kondapur, Serilingampally, Gachibowli, and Madhapur.

There's no `npm install`, no dev server, and no environment file — the key is entered at runtime in the browser and is never written to disk or sent anywhere except WeatherUnion's API.

## How It Works

- Each locality is mapped to a fixed **latitude/longitude** pair (see list of WeatherUnion's [weather station coordinates](https://b.zmtcdn.com/data/file_assets/65fa362da3aa560a92f0b8aeec0dfda31713163042.pdf)).
- Checking a box calls `GET /gw/weather/external/v0/get_weather_data?latitude=...&longitude=...` with your API key in the request header, and renders the result into both the table and the map.
- The whole thing is vanilla JavaScript — no framework, no build step — so it's easy to read top to bottom in one sitting.

## API Response Schema
 
WeatherUnion doesn't publish a formal API reference — this is based on the response shape actually returned by `get_weather_data` (and matches what this dashboard's `fetchLocality()` function parses).
 
### Successful response
 
```json
{
  "status": 200,
  "message": "Successful response fetched",
  "device_type": 1,
  "locality_weather_data": {
    "temperature": 28.7,
    "humidity": 78.8,
    "wind_speed": 4.2,
    "wind_direction": 180,
    "rain_intensity": 0,
    "rain_accumulation": 24.2
  }
}
```
 
| Field | Type | Meaning |
|---|---|---|
| `status` | number | HTTP-style status code for the request (`200` on success). |
| `message` | string | Human-readable status message. |
| `device_type` | number | `1` = automated weather station (temperature/humidity/wind + rain), `2` = rain-gauge-only station (rain fields only — see Limitations above). |
| `locality_weather_data` | object | Container for the actual readings, described below. |
| `locality_weather_data.temperature` | number | Air temperature in °C. |
| `locality_weather_data.humidity` | number | Relative humidity, as a percentage. |
| `locality_weather_data.wind_speed` | number | Wind speed in km/h. |
| `locality_weather_data.wind_direction` | number | Wind direction in degrees (0–360, meteorological convention). |
| `locality_weather_data.rain_intensity` | number | Current rainfall rate in mm/hr. This is what the dashboard's map dots use to decide blue vs red. |
| `locality_weather_data.rain_accumulation` | number | Cumulative rainfall in mm for the current measurement period. |
 
Any of the `locality_weather_data` fields can be **absent** from the response — this dashboard's code treats a missing/`null` value as `"-"` in the table and popups rather than assuming `0`, since "no reading" and "zero rainfall" aren't the same thing.
 
### Error response
 
Errors come back with a different, much smaller shape — no `locality_weather_data` at all:
 
```json
{
  "status": "400",
  "message": "coordinates are invalid"
}
```
 
Note `status` is a **string** here (`"400"`) versus a **number** on success (`200`) — an inconsistency worth defending against if you're writing your own parsing logic rather than relying on this dashboard's `try`/`catch` + `resp.ok` check, which sidesteps the type difference entirely by not inspecting `status` directly.

## Project Structure

```
.
├── hyderabad_weather_dashboard.html   # the app - open this in a browser
└── README.md
```

## Data & Attribution

- Weather data: [WeatherUnion API](https://www.weatherunion.com/)
- Map tiles: © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors

## Reusing This Code for Other Locations
 
This dashboard isn't Hyderabad-specific in any structural way — the only Hyderabad-specific part is the `LOCALITIES` lookup table and the map's initial centre point. WeatherUnion covers 30+ Indian cities, and Zomato publishes the complete, authoritative list of every city, locality, coordinate pair, and locality ID as a PDF:
 
**[Live Weather - A Zomato Giveback (PDF)](https://b.zmtcdn.com/data/file_assets/65fa362da3aa560a92f0b8aeec0dfda31713163042.pdf)**
 
Each row in that PDF has six columns:
 
| Column | Example | Used by this dashboard? |
|---|---|---|
| `cityName` | `Bengaluru` | Used to find the rows for your target city |
| `localityName` | `Koramangala` | Becomes the key in `LOCALITIES` |
| `localityId` | `ZWL001156` | Not currently used (only needed if you re-add locality-specific endpoints beyond the main weather one) |
| `latitude` | `12.933756` | Used directly - the weather endpoint takes coordinates |
| `longitude` | `77.625825` | Used directly |
| `device_type` | `1 - Automated weather system` or `2 - Rain gauge system` | Not used, but worth knowing: rain-gauge-only stations won't report temperature/humidity/wind, only rainfall |
 
### Steps to adapt the dashboard to a new city
 
1. **Open the PDF** and find every row where `cityName` matches your target city (e.g. `Bengaluru`, `Mumbai`, `Pune`, `Chennai`). For a small number of localities you can copy these by hand; for a whole city, a PDF table-extraction tool (e.g. `pdftotext -layout`, Python's `pdfplumber`, or Tabula) makes this faster.
2. **Rebuild the `LOCALITIES` object** in `hyderabad_weather_dashboard.html` using the `localityName`, `latitude`, and `longitude` columns:
```js
   const LOCALITIES = {
     "Koramangala": { lat: 12.933756, lon: 77.625825 },
     "Indiranagar": { lat: 12.952636, lon: 77.653059 },
     "Whitefield":  { lat: 12.975224, lon: 77.740422 },
     // ...one entry per locality row from the PDF
   };
```
 
3. **Update `DEFAULT_CHECKED`** to a handful of locality names that actually exist in your new `LOCALITIES` object.
4. **Recenter the map.** Find this line near the top of the script:
```js
   const map = L.map('map').setView([17.4400, 78.4483], 11); // centred roughly on Hyderabad
```
 
   and replace the `[lat, lon]` pair with a rough centre point for your city (any of that city's locality coordinates works fine as an approximation), adjusting the zoom level (`11`) if the city's spread is noticeably larger or smaller.
 
5. **Nothing else changes.** The `fetch()` call to WeatherUnion's `get_weather_data` endpoint is generic — it just wants a `latitude`/`longitude` pair and your API key, so any city from the PDF works as a drop-in replacement.
One thing worth checking as you copy rows: some localities are rain-gauge-only (`device_type: 2`), which means temperature/humidity/wind fields may come back empty for those specific points even though rainfall data is available — that's expected, not a bug.
 
## Limitations
 
- This is a client-side-only demo. Your API key lives in a plain browser input field and is sent directly from the browser to WeatherUnion — fine for personal/local use, but **don't deploy this as-is to a public URL** without moving the key server-side, since anyone viewing the page's source or network requests could see it.
- WeatherUnion coverage is limited to specific localities in specific cities; not every neighbourhood in Hyderabad has a station.
