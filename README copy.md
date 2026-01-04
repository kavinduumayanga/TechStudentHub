# Tech & Student Help Hub (Static Site)

A lightweight, AdSense-friendly static website built with pure **HTML + CSS + minimal vanilla JS**.

- No backend
- No build step
- System fonts only (no external font/icon CDNs)
- Mobile-first, fast, and easy to expand with more blog posts

## Project structure

```
/
  index.html
  about.html
  contact.html
  privacy-policy.html
  terms.html
  disclaimer.html
  404.html
  robots.txt
  sitemap.xml
  /blog/
     index.html
     post-1.html
     post-2.html
     post-3.html
  /assets/
     /css/
        style.css
     /js/
        main.js
     /images/
        placeholder.svg
```

## Run locally

### Option A: Open the file directly

- Double-click `index.html` or open it in your browser.

### Option B: Use VS Code Live Server (recommended)

1. Install the **Live Server** extension in VS Code.
2. Right-click `index.html` → **Open with Live Server**.

This helps with consistent relative paths and simulating real hosting.

## Deploy to GitHub Pages

1. Create a GitHub repository and push this folder.
2. In GitHub: **Settings → Pages**.
3. Under **Build and deployment**, set:
   - Source: **Deploy from a branch**
   - Branch: **main** (or your default) and folder **/** (root)
4. Wait for GitHub to publish your site.

### Canonical URLs

Each page includes a canonical placeholder comment like:

- `<!-- <link rel="canonical" href="https://YOUR-DOMAIN-HERE/..." /> -->`

After deployment, update those canonical tags to your real domain.

## Where to insert AdSense code (after approval)

### 1) Global AdSense script (in `<head>`)

Every HTML file includes a clearly marked placeholder comment block:

```html
<!-- AdSense placeholder (paste your AdSense script here after approval) -->
<!--
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
    crossorigin="anonymous"></script>
-->
```

When approved, replace `ca-pub-XXXXXXXXXXXXXXXX` with your real publisher ID and remove the surrounding comment markers.

### 2) Ad unit placeholders (inside blog posts)

Each blog post contains visible placeholders you can replace with AdSense ad units:

- Top of article
- In-article
- End of article

Search for `Ad placeholder` in:

- `blog/post-1.html`
- `blog/post-2.html`
- `blog/post-3.html`

## AdSense-friendly checklist (practical)

Before applying (or re-applying):

- Content is original, useful, and readable (not scraped/spun)
- Navigation is clear: Home, Blog, About, Contact
- Legal pages exist and are accessible: Privacy Policy, Terms, Disclaimer
- No broken links; pages load correctly on mobile
- Pages are fast (minimal JS, optimized images)
- No misleading UI (ads should never look like navigation/download buttons)
- Clear site purpose and categories

## Add a new blog post (static workflow)

1. Copy an existing post file, for example:
   - Copy `blog/post-1.html` → `blog/post-4.html`
2. Update the post metadata:
   - `<title>`
   - Meta description
   - Category label (kicker)
   - Date (`<time datetime="...">`)
   - Reading time text
   - Table of contents anchors
   - JSON-LD fields (`headline`, `description`, dates, `@id` URL placeholder)
3. Add a new card to the blog list:
   - Edit `blog/index.html`
   - Add a new `<article class="card" ...>` block
   - Update `data-search` text so search can match title/excerpt keywords
4. (Optional but recommended) Add it to “Latest Articles” on the home page:
   - Edit `index.html`
5. Add internal links:
   - Add “Related reading” links in the new post
   - Consider linking from older posts to the new one
6. Update `sitemap.xml`:
   - Add a new `<url>` entry for `/blog/post-4.html`

## Notes

- The contact form uses `mailto:` (no backend). Some devices may not open a mail client; a direct mailto link is also provided.
- `robots.txt` allows all crawling and points to `sitemap.xml`.
