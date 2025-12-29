# Mutual Fund Multi‑Year NAV Chart (MFapi.in + Chart.js)

This project visualizes the multi‑year NAV history of an Indian mutual fund using the free [**MFapi.in**](https://www.mfapi.in/) API by [Yuvaraj Loganathan](https://www.linkedin.com/in/yuvarajl/) and **Chart.js**. 
It is designed to help investors study seasonal patterns and see 52‑week high/low levels for a scheme at a glance.

The sample is built for: **HDFC Large Cap Fund – IDCW Option – Regular Plan** but you can easily adapt it for any other scheme supported by MFapi.in.

## Features

- Fetches live historical NAV data from **MFapi.in** for a given `schemeCode`.
- Converts daily NAVs into **monthly averages per year**.
- Plots each calendar year as a **separate colored line** on a shared Jan–Dec x‑axis.
- Highlights the **current year** with a thicker dark‑red line.
- Dynamically computes **52‑week high and low**:
  - Uses the last 52 weeks of data from the API.
  - Draws **vertical dashed lines** at the dates of 52‑week high and low.
  - Displays values and dates in a top **info bar**.
- Smart **year labels** at the right end of each line:
  - Prevents overlap by enforcing minimum spacing.
  - Uses dotted connectors when labels are shifted vertically.
- Fully client‑side: just HTML + JavaScript, no backend or build step.

## Tech Stack

- **Chart.js 4.x** (via CDN) – line chart rendering.
- **Chart.js Annotation Plugin** – for 52‑week high/low vertical markers.
- **MFapi.in** – free Indian mutual fund API providing historical NAVs in JSON.

## Getting Started

### 1. Clone or download

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Run locally

**Simplest way:**

- Open `mf_nav_chart.html` directly in a modern browser (Chrome, Edge, Firefox).

If your browser blocks network calls from local files, serve it over HTTP:

```bash
# Python 3
python -m http.server 8000

# Or Node.js (if installed)
npx http-server
```

Then open:

```text
http://localhost:8000/mf_nav_chart.html
```

The page will call MFapi.in and render the chart automatically.

## How It Works

### Data source: MFapi.in

The sample uses:

```text
https://api.mfapi.in/mf/102001
```

MFapi returns JSON with daily NAV entries:

```json
{
  "meta": { ... },
  "data": [
    { "date": "27-12-2025", "nav": "123.4567" },
    { "date": "26-12-2025", "nav": "123.0123" },
    ...
  ]
}
```

The script:

1. Parses the `date` string (`DD-MM-YYYY`) into JavaScript `Date` objects.
2. Sorts records by date (oldest first).
3. Extracts `year` and `month` from each date.
4. Aggregates daily NAVs into **average NAV per month per year**.
5. Builds a dataset for each year (2010, 2011, …, current year).

### 52‑Week High/Low Logic

1. Compute a cutoff date: **today − 52 weeks**.
2. Filter the parsed data to keep only entries on or after that cutoff.
3. Scan this subset to find:
   - Maximum NAV and its date → 52‑week **High**
   - Minimum NAV and its date → 52‑week **Low**
4. Update the info bar with:
   - `52W High: ₹X.XX (DD Mon YYYY)`
   - `52W Low: ₹Y.YY (DD Mon YYYY)`
   - `Current NAV` from the latest API entry.
5. Convert the high/low dates to x‑axis positions using  
   `month + day/31` and draw **vertical dashed lines** at those positions.

### Chart Configuration

- **X‑axis:** Linear, values 0–11 mapped to `Jan`–`Dec`.
- **Y‑axis:** NAV in rupees; not forced to start at zero to preserve detail.
- **Tooltip:** Shows `Month Year` (from x) and `NAV: ₹value`.
- **Legend:** Hidden; instead, year labels are drawn at the right edge.

### Smart Year Labels

A custom Chart.js plugin runs after datasets are drawn:

1. Finds the last point for each year’s line and records its canvas Y‑position.
2. Sorts labels by Y‑position.
3. Enforces a minimum vertical spacing (e.g., 18px) between labels by shifting them down as needed.
4. Draws a dotted connector if a label’s Y‑position was adjusted.
5. Renders the year text (e.g., `2025`, `2024`) to the right of the plotting area.

This keeps the chart readable even when multiple years converge near similar NAV levels.

## Customization

### Change to another mutual fund

Replace the `schemeCode` and title:

```javascript
const schemeCode = '102001'; // change to desired scheme code
```

Update the visible name:

```html
<div class="scheme-title">
  HDFC Large Cap Fund - IDCW Option - Regular Plan
</div>
```

You can find scheme codes and metadata from MFapi.in’s index or their documentation.

### Use daily instead of monthly aggregation

If you want a pure daily NAV line:

- Skip the “monthly average” grouping.
- Push each daily `date` and `nav` pair directly into a single dataset.
- Keep the 52‑week logic as is.

### Styling

- Adjust colors in the `yearColors` map.
- Change font sizes, padding, or chart dimensions in the CSS section.
- Modify dashed line style for 52‑week markers via `borderDash` and `borderColor`.

## Limitations & Notes

- Relies on MFapi.in availability and data freshness.
- 52‑week window is computed relative to the **current date in the browser**.
- This is a visualization and analysis tool and **not** investment advice.
