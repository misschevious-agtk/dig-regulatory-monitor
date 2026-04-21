"""
scraper.py
Fetches regulatory news articles, categorises them, and outputs
content/index.json in the format expected by the DIG Regulatory Monitor site.
"""
 
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from pathlib import Path
from scraper.config import SCRAPER_CONFIG, CATEGORY_KEYWORDS, SOURCES
 
CONTENT_DIR = Path(__file__).parent.parent / "content"
PAGES_DIR = CONTENT_DIR / "pages"
INDEX_FILE = CONTENT_DIR / "index.json"
SYNC_FILE = CONTENT_DIR / "sync_summary.json"
 
 
# ── HTTP ───────────────────────────────────────────────────────────────────────
 
def fetch_page(url: str) -> BeautifulSoup | None:
    try:
        headers = {"User-Agent": SCRAPER_CONFIG["user_agent"]}
        r = requests.get(url, headers=headers, timeout=SCRAPER_CONFIG["timeout"])
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except requests.RequestException as e:
        print(f"[ERROR] {url}: {e}")
        return None
 
 
# ── Article extraction ─────────────────────────────────────────────────────────
 
def extract_articles_from_page(soup: BeautifulSoup, source_label: str, url: str) -> list[dict]:
    """
    Try multiple common article-listing patterns.
    Returns a list of raw article dicts with title, body, source, date, url.
    """
    articles = []
 
    # Pattern 1: <article> tags
    items = soup.find_all("article")
 
    # Pattern 2: common card class patterns
    if not items:
        items = soup.find_all(class_=re.compile(r"(card|post|entry|article|item)", re.I))
 
    # Pattern 3: fallback — treat each <h2>/<h3> block as an article
    if not items:
        for heading in soup.find_all(["h2", "h3"]):
            title_text = heading.get_text(strip=True)
            if len(title_text) < 20:
                continue
            # Grab the next sibling paragraph as body
            body = ""
            sib = heading.find_next_sibling()
            while sib and sib.name in ["p", "div", "span"]:
                body += sib.get_text(" ", strip=True) + " "
                sib = sib.find_next_sibling()
            articles.append({
                "title": title_text,
                "body": body.strip(),
                "source": source_label,
                "date": _today_str(),
                "url": url,
            })
        return articles
 
    for item in items:
        title_el = item.find(["h1", "h2", "h3", "h4"])
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        if len(title) < 20:
            continue
 
        # Body: all <p> text inside the item
        body_parts = [p.get_text(" ", strip=True) for p in item.find_all("p")]
        body = " ".join(body_parts).strip()
 
        # Date: look for <time> or text matching date patterns
        date = _today_str()
        time_el = item.find("time")
        if time_el:
            date = time_el.get_text(strip=True) or time_el.get("datetime", date)
        else:
            raw = item.get_text(" ")
            m = re.search(r"\b(\d{1,2}\s+\w+\s+\d{4}|\d{4}-\d{2}-\d{2})\b", raw)
            if m:
                date = m.group(1)
 
        # Source attribution
        source = source_label
        src_el = item.find(class_=re.compile(r"(source|byline|author|publisher)", re.I))
        if src_el:
            source = src_el.get_text(strip=True) or source_label
 
        articles.append({
            "title": title,
            "body": body,
            "source": source,
            "date": date,
            "url": url,
        })
 
    return articles
 
 
# ── Categorisation ─────────────────────────────────────────────────────────────
 
def categorise(article: dict) -> str:
    """Return the best matching category key based on title + body keywords."""
    text = (article["title"] + " " + article["body"]).lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                scores[cat] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "regulatory"
 
 
def infer_tags(article: dict) -> list[str]:
    """Generate display tags from content."""
    text = (article["title"] + " " + article["body"]).lower()
    tags = []
 
    type_map = {
        "Antitrust": ["antitrust", "competition law", "abuse of dominance"],
        "AI / Antitrust": ["ai antitrust", "ai / antitrust", "ai assistant", "gatekeeper"],
        "Cartel": ["cartel", "price fixing", "market sharing"],
        "GDPR": ["gdpr", "data protection regulation"],
        "Data & Privacy": ["data protection", "personal data", "privacy", "dpa"],
        "IP Law": ["intellectual property", "copyright", "patent", "trademark"],
        "AI Act": ["ai act", "artificial intelligence act"],
        "DMA": ["digital markets act", "dma"],
        "DSA": ["digital services act", "dsa"],
        "Under Investigation": ["investigation", "probe", "charge sheet", "statement of objections"],
        "Fine": ["fined", "fine of", "penalty of", "€"],
    }
 
    geo_map = {
        "EU": ["european commission", "eu ", "cjeu", "ecj", "dma", "dsa", "ai act"],
        "UK": ["uk ", "ico ", "cma ", "united kingdom"],
        "US": ["ftc ", "doj ", "united states", "us "],
        "IN": ["india", "cci ", "meity"],
        "DE": ["germany", "bundeskartellamt"],
        "FR": ["france", "cnil"],
        "NL": ["netherlands", "dutch", "ap "],
        "SG": ["singapore", "pdpc"],
        "CN": ["china", "samr", "cyberspace administration"],
    }
 
    for tag, kws in type_map.items():
        if any(kw in text for kw in kws):
            tags.append(tag)
            if len(tags) >= 3:
                break
 
    for geo, kws in geo_map.items():
        if any(kw in text for kw in kws):
            tags.append(geo)
            break  # max one geo tag
 
    return tags if tags else ["Regulatory"]
 
 
# ── Trending selection ─────────────────────────────────────────────────────────
 
def select_trending(categorised: dict, n: int = 5) -> list[dict]:
    """Pick the n most recent articles across all categories as trending."""
    all_articles = []
    for articles in categorised.values():
        all_articles.extend(articles)
    # Deduplicate by title
    seen = set()
    unique = []
    for a in all_articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
    return unique[:n]
 
 
# ── Markdown save ──────────────────────────────────────────────────────────────
 
def save_markdown(article: dict, category: str):
    safe_name = re.sub(r"[^\w\-]", "_", article["title"])[:60]
    md_path = PAGES_DIR / f"{category}_{safe_name}.md"
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    md_path.write_text(
        f"---\ntitle: {article['title']}\ncategory: {category}\n"
        f"source: {article['source']}\ndate: {article['date']}\n"
        f"url: {article.get('url','')}\ntags: {', '.join(article.get('tags',[]))}\n---\n\n"
        f"{article['body']}\n",
        encoding="utf-8",
    )
 
 
# ── Main ───────────────────────────────────────────────────────────────────────
 
def _today_str() -> str:
    return datetime.utcnow().strftime("%-d %B %Y")
 
 
def run():
    print(f"[START] Scraping {len(SOURCES)} source(s)...")
    raw_articles = []
 
    for source in SOURCES:
        soup = fetch_page(source["url"])
        if not soup:
            continue
        articles = extract_articles_from_page(soup, source["label"], source["url"])
        print(f"  [{source['label']}] {len(articles)} article(s) found")
        raw_articles.extend(articles)
 
    # Categorise and tag
    categorised = {cat: [] for cat in CATEGORY_KEYWORDS}
    for article in raw_articles:
        cat = categorise(article)
        article["tags"] = infer_tags(article)
        categorised[cat].append(article)
        save_markdown(article, cat)
 
    # Enforce max_per_category
    max_per = SCRAPER_CONFIG.get("max_per_category", 20)
    for cat in categorised:
        categorised[cat] = categorised[cat][:max_per]
 
    # Build final index
    index = {
        "trending": select_trending(categorised, n=SCRAPER_CONFIG.get("trending_count", 5)),
        "competition": categorised["competition"],
        "privacy": categorised["privacy"],
        "ip": categorised["ip"],
        "regulatory": categorised["regulatory"],
    }
 
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
 
    # Sync summary
    total = sum(len(v) for v in categorised.values())
    summary = {
        "last_sync": datetime.utcnow().isoformat() + "Z",
        "total_articles": total,
        "by_category": {cat: len(articles) for cat, articles in categorised.items()},
    }
    SYNC_FILE.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
 
    print(f"[DONE] {total} article(s) indexed across {len(categorised)} categories.")
 
 
if __name__ == "__main__":
    run()
