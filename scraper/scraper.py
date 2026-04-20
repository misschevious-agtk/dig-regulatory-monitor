"""
scraper.py
Fetches and parses content from the DIG Regulatory Monitor website.
Outputs clean markdown and JSON files for Toqan to consume.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime
from pathlib import Path
from config import SCRAPER_CONFIG

CONTENT_DIR = Path(__file__).parent.parent / "content"
PAGES_DIR = CONTENT_DIR / "pages"
INDEX_FILE = CONTENT_DIR / "index.json"


def fetch_page(url: str) -> BeautifulSoup | None:
    """Fetch a single page and return a BeautifulSoup object."""
    try:
        headers = {"User-Agent": SCRAPER_CONFIG["user_agent"]}
        response = requests.get(url, headers=headers, timeout=SCRAPER_CONFIG["timeout"])
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def extract_content(soup: BeautifulSoup, url: str) -> dict:
    """Extract title, body text, and metadata from a parsed page."""
    title = soup.title.string.strip() if soup.title else "Untitled"

    # Remove scripts, styles, nav, footer noise
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    body_text = soup.get_text(separator="\n", strip=True)
    # Collapse excessive blank lines
    body_text = re.sub(r"\n{3,}", "\n\n", body_text)

    return {
        "url": url,
        "title": title,
        "content": body_text,
        "scraped_at": datetime.utcnow().isoformat() + "Z",
    }


def save_page(page_data: dict) -> str:
    """Save extracted page content as markdown and return file path."""
    safe_name = re.sub(r"[^\w\-]", "_", page_data["title"])[:60]
    md_path = PAGES_DIR / f"{safe_name}.md"

    md_content = f"""---
title: {page_data['title']}
url: {page_data['url']}
scraped_at: {page_data['scraped_at']}
---

{page_data['content']}
"""
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    md_path.write_text(md_content, encoding="utf-8")
    print(f"[OK] Saved: {md_path.name}")
    return str(md_path)


def update_index(pages: list[dict]):
    """Write/update the master index.json with all scraped pages."""
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    index = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "source": SCRAPER_CONFIG["base_url"],
        "total_pages": len(pages),
        "pages": [
            {
                "title": p["title"],
                "url": p["url"],
                "file": f"pages/{re.sub(r'[^\w\-]', '_', p['title'])[:60]}.md",
                "scraped_at": p["scraped_at"],
            }
            for p in pages
        ],
    }
    INDEX_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Index updated: {len(pages)} page(s) indexed.")


def discover_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    """Collect internal links from a page."""
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/") or href.startswith(base_url):
            full = href if href.startswith("http") else base_url.rstrip("/") + href
            links.add(full.split("#")[0])  # strip anchors
    return list(links)


def run():
    """Main scrape-and-sync entry point."""
    base_url = SCRAPER_CONFIG["base_url"]
    visited = set()
    queue = [base_url]
    all_pages = []

    print(f"[START] Scraping: {base_url}")

    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        soup = fetch_page(url)
        if not soup:
            continue

        page_data = extract_content(soup, url)
        save_page(page_data)
        all_pages.append(page_data)

        if SCRAPER_CONFIG.get("follow_links", True):
            new_links = discover_links(soup, base_url)
            for link in new_links:
                if link not in visited:
                    queue.append(link)

    update_index(all_pages)
    print(f"[DONE] Scraped {len(all_pages)} page(s).")


if __name__ == "__main__":
    run()
