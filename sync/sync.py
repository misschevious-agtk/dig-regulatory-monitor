"""
sync.py
Detects changes since the last scrape and updates sync_summary.json
in the format expected by the DIG Regulatory Monitor website.
"""
 
import json
import hashlib
from pathlib import Path
from datetime import datetime
 
CONTENT_DIR = Path(__file__).parent.parent / "content"
INDEX_FILE = CONTENT_DIR / "index.json"
SYNC_FILE = CONTENT_DIR / "sync_summary.json"
HASH_CACHE = CONTENT_DIR / ".hash_cache.json"
 
 
def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
 
 
def load_cache() -> dict:
    if HASH_CACHE.exists():
        return json.loads(HASH_CACHE.read_text(encoding="utf-8"))
    return {}
 
 
def save_cache(cache: dict):
    HASH_CACHE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
 
 
def detect_changes(pages_dir: Path, cache: dict) -> list[str]:
    """Return list of filenames whose content has changed since last run."""
    changed = []
    for md_file in sorted(pages_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        new_hash = hash_content(content)
        if new_hash != cache.get(md_file.name):
            changed.append(md_file.name)
            cache[md_file.name] = new_hash
    return changed
 
 
def count_by_category() -> dict:
    """Read index.json and return article counts per category."""
    if not INDEX_FILE.exists():
        return {}
    index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    return {
        cat: len(index.get(cat, []))
        for cat in ["competition", "privacy", "ip", "regulatory"]
    }
 
 
def run_sync():
    pages_dir = CONTENT_DIR / "pages"
 
    if not pages_dir.exists():
        print("[SYNC] No content yet — run the scraper first.")
        return
 
    cache = load_cache()
    changed = detect_changes(pages_dir, cache)
    save_cache(cache)
 
    now = datetime.utcnow().isoformat() + "Z"
    by_category = count_by_category()
    total = sum(by_category.values())
 
    # Write sync_summary.json — "last_sync" is what the website status bar reads
    summary = {
        "last_sync": now,               # ← website reads this field
        "changed_files": changed,
        "total_changed": len(changed),
        "total_articles": total,
        "by_category": by_category,
    }
 
    SYNC_FILE.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
 
    if changed:
        print(f"[SYNC] {len(changed)} file(s) updated: {', '.join(changed)}")
    else:
        print("[SYNC] No changes — content is up to date.")
 
    print(f"[SYNC] Total: {total} articles | {by_category}")
    return summary
 
 
if __name__ == "__main__":
    run_sync()
