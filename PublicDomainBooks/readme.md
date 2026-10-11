# Public-Domain Book Search (Google Books)

A tiny web page that searches the **Google Books** collection for **public-domain books** and lists them with links to download (PDF / EPUB) or read online.

There are for instance scores of [out-of-copyright books](https://mvark.blogspot.com/2014/05/try-this-web-app-to-discover-old.html) mostly by Britishers on Indian languages. These books are still relevant and especially useful for those whose medium of education has been in English. 

**No jQuery. No libraries. No build step. No external dependencies.**
Just one HTML file with the JavaScript inside it.

---

## What it does

1. You type a search term (for example `science`) and press **Enter**.
2. The page asks the Google Books API for matching free books.
3. It shows the results as a numbered list:
   - **Bold title** = a PDF or EPUB can be downloaded.
   - **Plain title** = can only be read on the web.
4. **Previous / Next** buttons let you page through results.

---

## Why no jQuery or other libraries are needed

The code uses the browser's built-in **`fetch()` API** together with **`async` / `await`**.

| Feature | What it does | Replaces |
|---|---|---|
| `fetch()` | Sends a web request and returns a *Promise* (a "result that will arrive soon") | jQuery's `$.ajax` / `$.getJSON`, or the old JSONP `<script>` trick |
| `async` / `await` | Lets you write "wait for the answer, then continue" as simple top-to-bottom code | Nested callbacks |
| `addEventListener` | Listens for key presses and clicks | jQuery's `.on()` |
| `document.getElementById` | Finds elements on the page | jQuery's `$('#id')` |

Every modern browser supports all of these, so the page works as a single file with nothing to install.

---

## Project structure

Everything lives in one file:

```
books.html
├── <html> ... search box, results area, tips ...
└── <script> ... all JavaScript (config, fetch, rendering, paging) ... </script>
```

Suggested skeleton:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Google Books</title>
</head>
<body>
  <h4>Search for Books in the Public Domain from the Google Books collection</h4>
  <p><input type="text" id="search_input" aria-label="Search input" placeholder="Enter search term"></p>

  <div id="fetching">Fetching results...</div>
  <div id="content"></div>
  <!-- the script creates <div id="pagination"> by itself -->

  <script>
    // JavaScript that fetches results using Google Books API
  </script>
</body>
</html>
```
---

## One-time setup: get a Google Books API key

Without a key, all anonymous visitors share one small quota and you will see **HTTP 429** errors. A free key gives you your own quota.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a project.
2. Open **APIs & Services → Library**, search for **Books API** and click **Enable**.
3. Open **APIs & Services → Credentials → Create credentials → API key**.
4. **Restrict the key** (it will be visible in your page source):
   - *Application restrictions:* choose **HTTP referrers** and add your site, for example `https://yoursite.com/*`.
   - *API restrictions:* choose **Restrict key** and select **Books API** only.
5. Paste the key into the script:

   ```js
   var API_KEY = "YOUR_KEY_HERE";
   ```

> The page also works with `API_KEY = ""`, but expect 429 errors when traffic is high.

---

## Settings at the top of the script

| Variable | Default | Meaning |
|---|---|---|
| `API_KEY` | `""` | Your Google Books API key |
| `MAX_RESULTS` | `40` | Books requested per page (40 is the API maximum) |
| `MAX_RETRIES` | `3` | How many times to retry after a 429/503 error |
| `ONLY_PUBLIC_DOMAIN` | `true` | `false` also lists other free downloadable books |

---

## How the code works (reading order)

1. **`DOMContentLoaded` listener** (bottom of the script): focuses the search box and listens for the **Enter** key.
2. **`loadResults(query, page)`**: starts a search, shows "Fetching results...", and blocks double submissions while one is running.
3. **`buildUrl()`**: builds the API address, for example
   `https://www.googleapis.com/books/v1/volumes?q=science&maxResults=40&startIndex=0&printType=books&orderBy=relevance&filter=free-ebooks&key=...`
4. **`fetchWithRetry()`**: calls `fetch()`. If Google answers **429** or **503**, it waits (1s, 2s, 4s, or the `Retry-After` time Google sends) and tries again.
5. **`cache`**: remembers results per query and page, so going back to a page costs no new API call.
6. **`renderResponse()` and `createBookListItem()`**: turn each book into a list entry.
7. **`renderPagination()`**: draws Previous / Next buttons.
8. **`esc()`**: escapes text before it is placed in the page, so odd characters in a title cannot break the page or inject HTML.

---

## Good to know (the "gotchas")

- **Page size can be smaller than asked.** The API sometimes returns fewer books than `MAX_RESULTS`. The script therefore remembers where each page really ended (`pageStarts`) instead of calculating `page × 40`. Otherwise books would be skipped.
- **`totalItems` is only an estimate.** That is why there is no "Page 1 of N". "Next" stays available until a page comes back empty, then you see "No more results".
- **Many public-domain books have no PDF/EPUB.** The API flags them `FULL_PUBLIC_DOMAIN`, but only a *web reader* link exists. They are shown with a plain title and a **Web** link.
- **EPUB links can be dead.** The API often includes an EPUB `downloadLink` even when `epub.isAvailable` is `false`. The script only shows a link when `isAvailable` is `true`.
- **Links are forced to `https`.** The API returns some `http://` links.

---

## Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| "Google Books has temporarily limited requests (HTTP 429)" | Quota exceeded | Add an API key; wait a minute; avoid rapid repeated searches |
| `403` error in the console | Key restricted to a different site, or Books API not enabled | Check the referrer restriction and that **Books API** is enabled |
| "No books found" | No free books match the term | Try another term, or use `intitle:`, `inauthor:` (see below) |
| Fewer results than expected | API returns variable page sizes; filter keeps only public-domain books | Normal behaviour. Set `ONLY_PUBLIC_DOMAIN = false` for more |
| Nothing happens on Enter | Script error | Open DevTools (F12) → **Console** tab and read the message |

**Debugging tip:** each page logs a line such as `Page 1: API returned 20 items` in the browser console.

---

## Search tips for users

- `intitle:`, `inauthor:`, `inpublisher:`, `isbn:` narrow a search.
- Put quotes around words for an exact phrase, for example `"Elizabeth Bennet"`.
- Use `+` and `-` to include or exclude words, for example `"Elizabeth+Bennet"+Darcy-Austen`.

---

## Quick reference: the whole flow

```
Enter key
  → loadResults()
    → buildUrl()
    → fetchWithRetry()  ──(429/503?)── wait → retry (up to MAX_RETRIES)
    → cache the answer
    → renderResponse()
        → createBookListItem() for each book
        → renderPagination()
```

---

## Credits and data

Book data comes from the [Google Books API](https://developers.google.com/books/docs/v1/using). Please follow Google's API terms when you use it.
