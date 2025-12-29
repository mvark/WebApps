# NPS NAV Multi‑Year Line Chart (Chart.js)

[National Pension System or NPS](https://indiacola.blogspot.com/2025/01/nps.html) is one of the cheapest market-linked annuity and long-term investment options in India.

This project visualizes multi‑year NAV history for the NPS scheme "ICICI PRUDENTIAL PENSION FUND SCHEME E - TIER II" using a public JSON API and a fully client‑side Chart.js setup. It is designed as a reusable example for analyzing seasonal patterns (monthly dips and rises) across years for schemes from different Pension Fund Managers (PFM). 

<img width="504" height="424" alt="image" src="https://github.com/user-attachments/assets/cb397d59-2d87-4a38-8a22-8e967fa04d63" />


## Features

- Fetches historical NAV for scheme **SM007004** from `https://npsnav.in/api/historical/SM007004`  
- Converts daily data into **monthly averages per year**  
- Plots each year as a **separate colored line** on a shared Jan–Dec x‑axis  
- Current year (2025) drawn as a **thicker dark‑red line**  
- 52‑week **high** and **low**:
  - Shown as **dashed vertical lines** on the chart
  - Displayed clearly in an info bar above the chart
- **Smart year labels**:
  - Year names rendered at the right end of each line
  - Automatic vertical spacing to avoid overlap
  - Dotted connectors from label to the line when shifted
- Pure front‑end: just open the HTML file in a browser.

## Tech Stack

- **HTML / CSS / JavaScript**
- **Chart.js 4.x** for rendering the line chart  
- **Chart.js Annotation Plugin** for 52‑week high/low vertical markers  

All libraries are loaded via CDN, so there is no build step or bundler required.

## Getting Started

### 1. Clone or download

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

Add the generated `nps_nav_chart.html` file to the root of this folder.

### 2. Run locally

**Option A – Just open the file**

1. Double‑click `nps_nav_chart.html`
2. Your default browser should open the visualization

**Option B – Serve via a local HTTP server (recommended)**

If the browser blocks the API call (CORS or file protocol issues), run a simple HTTP server:

```bash
# Python 3
python -m http.server 8000

# or Node.js
npx http-server
```

Then open:

```text
http://localhost:8000/nps_nav_chart.html
```

The page will fetch the NAV data live from the API and render the chart.

## How the Chart Works

### Data source

The HTML file fetches data from:

```text
https://npsnav.in/api/historical/SM007004
```

The response format:

```json
{
  "data": [
    { "date": "26-12-2025", "nav": 60.5769 },
    { "date": "24-12-2025", "nav": 60.8192 },
    ...
  ]
}
```

The script:

1. Parses `date` (`DD-MM-YYYY`) into JavaScript `Date` objects  
2. Groups entries by **calendar year**  
3. Aggregates daily NAV values into **average NAV per month per year**  
4. Builds a Chart.js dataset for each year using distinct colors

### Visual encoding

- **X‑axis:** Months from Jan (0) to Dec (11), rendered as labels `Jan`–`Dec`  
- **Y‑axis:** NAV (not forced to start at zero, to preserve detail)  
- **Lines:** One per year, with custom colors; 2025 has increased line width  
- **52‑week markers:**
  - Vertical dashed line near **February** for the 52‑week low  
  - Vertical dashed line near **November** for the 52‑week high  
  - Exact values and dates shown in a top info bar

### Smart year labels

Instead of a legend, each year is shown at the right end of its line:

- After Chart.js draws datasets, a custom plugin:
  - Reads the canvas positions of each dataset’s last point
  - Sorts labels by Y‑position
  - Enforces minimum spacing (e.g., 18 px) between labels
  - Moves labels down when they would overlap
  - Draws a small dotted connector from the adjusted label back to the actual end point  

This keeps the right side readable even when many years converge.

## Reusing and Adapting

To reuse this example for another NPS scheme or a different API:

1. **Change the API URL**

   In the script, replace:

   ```javascript
   fetch('https://npsnav.in/api/historical/SM007004')
   ```

   with your desired endpoint returning a similar `{ date, nav }` structure.

2. **Adjust highlighting**

   - Update the “current year” in the `yearColors` map and increase its `width`
   - Optionally update 52‑week high/low values and dates shown in the top info bar

3. **Customize color scheme**

   The `yearColors` mapping is a simple object:

   ```javascript
   const yearColors = {
     2025: { color: '#8B0000', width: 3 },
     2024: { color: '#FF4500', width: 2 },
     // ...
   };
   ```

   Modify or extend as needed for more years.

4. **Change aggregation logic**

   Currently, monthly values are **averages** of daily NAV in that month.  
   You can switch to first/last NAV of each month, or high/low, by altering the aggregation step.
