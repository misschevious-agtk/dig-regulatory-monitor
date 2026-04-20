# 🤖 DIG Regulatory Monitor — Toqan Agent Repository

This repository provides everything a **Toqan agent** needs to read, display, and stay in sync with the content of the [DIG Regulatory Monitor](https://github.com/maleevskaina/dig-regulatory-monitor) website.

---

## 📁 Repository Structure

```
├── .github/
│   └── workflows/
│       └── sync.yml          # GitHub Actions: auto-scrape daily at 06:00 UTC
├── agent/
│   ├── manifest.json         # Toqan agent manifest
│   └── toqan_config.yaml     # Toqan connection & display config
├── content/
│   ├── index.json            # Master index of all scraped pages
│   ├── sync_summary.json     # Last sync metadata
│   └── pages/               # Scraped pages as markdown files
├── scraper/
│   ├── scraper.py            # Main web scraper
│   └── config.py            # Scraper settings (URL, behaviour)
├── sync/
│   └── sync.py              # Change detection & sync reporting
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Create the GitHub repository

```bash
# On GitHub: create a new repo (e.g. "dig-regulatory-monitor-agent")
# Then clone it locally:
git clone https://github.com/maleevskaina/<YOUR-NEW-REPO-NAME>.git
cd <YOUR-NEW-REPO-NAME>
```

### 2. Copy these files into the new repo

```bash
# Copy all files from this package into your repo folder, then:
git add .
git commit -m "feat: initial Toqan agent setup"
git push origin main
```

### 3. Install dependencies locally (optional, for testing)

```bash
pip install -r requirements.txt
```

### 4. Run the scraper manually

```bash
python -m scraper.scraper
```

This will populate `content/pages/` with markdown files and update `content/index.json`.

### 5. Check for changes (sync)

```bash
python -m sync.sync
```

---

## 🔄 Automated Sync (GitHub Actions)

The workflow in `.github/workflows/sync.yml` runs the scraper **every day at 06:00 UTC** and automatically commits updated content back to the repository.

You can also trigger it manually:
> GitHub → your repo → **Actions** → **Scrape & Sync Content** → **Run workflow**

---

## 🤖 Connecting to Toqan

1. Open your **Toqan workspace**
2. Add a new data source → **GitHub Repository**
3. Point it to this repository
4. Set the **config file** to: `agent/toqan_config.yaml`
5. Set the **index file** to: `content/index.json`
6. Set the **content directory** to: `content/pages`

Toqan will then be able to:
- 📄 Read and display every page from the website
- 🔍 Search across all content
- 📝 Summarise individual pages or the full site
- 🕐 Report when content was last synced

---

## ⚙️ Configuration

Edit `scraper/config.py` to change the target URL or scraper behaviour:

```python
SCRAPER_CONFIG = {
    "base_url": "https://your-live-site-url.com",
    "follow_links": True,
    "max_pages": 100,
    ...
}
```

---

## 📝 Notes

- The `content/` folder is **auto-generated** — do not edit files there manually.
- The scraper respects a `User-Agent` header identifying it as `ToqanAgent/1.0`.
- All scraped content is stored as plain markdown, making it easy for any agent to read.
