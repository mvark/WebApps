# India Geographic Features Reference

A single-file, interactive reference table + map for learning geographic
terms — the kind of vocabulary list geography classes hand out (*archipelago,
delta, escarpment, isthmus...*) but turned into something you can click
around instead of just read.

## Why this is useful for learning geography

Most glossaries give you a term and a definition side by side, and leave you
to imagine what a "gorge" or a "salt pan" actually looks like on the ground.
This sample pairs every term with a **real, well-known Indian example**, and
lets you jump straight from the word to the place on a map:

- **67 geography terms**, each with a plain-English description and a named
  real-world example (*Delta → Sundarbans*, *Canyon → Gandikota Canyon*,
  *Isthmus → Adam's Bridge*...).
- **Click any row and the map flies there** — turning an abstract definition
  ("a narrow strip of land connecting larger land masses") into a concrete
  location you can see relative to the rest of the country.
- **Shape tells you something about scale before you even click**: a
  🔴 **circle** marks a specific point on the map (a waterfall, a cave, a
  single hill) while a 🟥 **square** marks a broad, regional feature (a
  desert, a delta, an entire valley). That distinction — *is this a place or
  a place-sized-region* — is itself a small geography lesson.
- **Two rows are deliberately unfilled** (*Fjord*, *Taiga*) with "Not found
  in India" as their example — a reminder that not every landform occurs
  everywhere, which is a geography lesson in itself.

If you are a Indian geography buff, a good exercise is to cover the
Example column and guess the real place before clicking the row to check.

## What it looks like

A two-pane layout: the reference table on one side, an interactive
[Leaflet](https://leafletjs.com/) map on the other. On a phone or narrow
window, it stacks into a scrollable map-on-top, list-below layout instead.

| Desktop | Mobile |
|---|---|
| Table and map side by side | Map on top, card-style list below |

## How it works (and the interesting parts)

This is intentionally light on dependencies and framework machinery — just
one HTML file, [Leaflet](https://leafletjs.com/) loaded from a CDN, and
plain CSS/JS. A few implementation details are worth calling out:

### One data array drives both the table and the map

```js
const FEATURES = [
  { term: "Delta", desc: "Land formed by river sediment at its mouth.",
    example: "Sundarbans", lat: 21.9497, lng: 88.9468, zoom: 8, shape: "square" },
  // ...67 entries total
];
```

Both the `<table>` rows and the map markers are generated from this single
array on page load. There's no second copy of the data to keep in sync —
add a row here and it shows up in both places automatically. This is the
main thing worth learning from this sample if you're newer to building
things like this: **pick one source of truth, and generate every view from
it**, rather than hand-writing the table in HTML *and* a separate list of
map pins.

### Per-feature zoom, because "broad" and "specific" need different zoom levels

```js
{ term: "Ocean", ..., zoom: 5 }   // zoomed way out
{ term: "Pond",  ..., zoom: 13 }  // zoomed way in
```

Every row carries its own `zoom` value, used when the map flies to it. A
single fixed zoom level would either strand you looking at an empty patch of
ocean at zoom 13, or fail to distinguish a temple pond from the district
around it at zoom 5. Tune any row's number directly — nothing else depends
on it.

### Numbered badges instead of default map pins

```js
const icon = L.divIcon({
  className: '',
  html: `<div class="map-badge${isSquare ? ' square' : ''}">${number}</div>`,
  iconSize: [22, 22],
  iconAnchor: [11, 11]
});
```

Rather than Leaflet's default teardrop pin (which needs its own image
assets and doesn't hold a number well), each marker is a tiny `<div>` styled
as a circle or square with CSS — a
[`divIcon`](https://leafletjs.com/reference.html#divicon). Same badge
markup and CSS classes are reused in the table's first column, so the
numbers on the map and the numbers in the table are guaranteed to match —
they're rendered by the same code path, not kept in sync by hand.

### A responsive table with zero extra markup

```css
@media (max-width: 768px) {
  table, tbody, tr, td { display: block; width: 100%; }
  thead { display: none; }
  td[data-label]:before { content: attr(data-label) ": "; font-weight: 600; }
}
```

On narrow screens, the table doesn't scroll sideways or get replaced with a
different mobile-only component — it's the *same* markup, just redrawn.
Each `<td>` already carries a `data-label="Term"` attribute; on mobile, CSS
turns that attribute into visible label text via `content: attr(data-label)`,
and stacks every cell into a card-like row. No JavaScript branching for
mobile vs. desktop, no duplicate templates — just one CSS rule.

### Clicking flies the map; it doesn't just jump

```js
map.flyTo([f.lat, f.lng], f.zoom);
```

`flyTo` animates the pan/zoom instead of snapping instantly
(`setView` would do that). It's a small touch, but it keeps you oriented —
you can watch the map travel from wherever it was to the new location,
rather than losing your place with a hard cut.

## Getting started

This is a static file — no build step, no server-side code, no npm install.

1. Download `india_geo_map_and_table.html`.
2. Open it directly in a browser (double-click it), **or** serve it locally
   if your browser blocks local file access for some reason:
   ```bash
   python3 -m http.server 8000
   ```
   then visit `http://localhost:8000/india_geo_map_and_table.html`.
3. That's it — Leaflet and the map tiles load from public CDNs, everything
   else is in the one file.

## Customizing

Everything you'd want to change lives in the `FEATURES` array near the top
of the `<script>` block:

| Want to... | Do this |
|---|---|
| Add a new term | Add a new object to `FEATURES` with `term`, `desc`, `example`, `lat`, `lng`, `zoom` |
| Change how far a row zooms | Edit that row's `zoom` number directly |
| Mark something as a broad/regional feature | Add `shape: "square"` to that row (omit it for a point feature — circle is the default) |
| Change the starting view | Edit `FEATURES[0]`, or change what the map's `setView(...)` call at the bottom references |
| Restyle anything | Everything is in one small `<style>` block at the top — colors, badge size, breakpoint, etc. |

## Notes on the map data

- Base map tiles come from [OpenStreetMap](https://www.openstreetmap.org/)
  via a public tile server — no API key required, but be mindful of usage if
  you deploy this somewhere with real traffic (OSM's tile servers ask that
  you not hammer them; for anything beyond casual/personal use, consider a
  dedicated tile provider).
- Coordinates are approximate, hand-picked to represent each example well at
  a teaching level — not surveyed to precise boundaries.
- There's no political boundary layer drawn for India — only the markers sit
  on top of the base map tiles.
