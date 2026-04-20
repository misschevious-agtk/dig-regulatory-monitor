"""
sync.py
Detects changes since the last scrape and only re-fetches updated pages.
Run manually or let the GitHub Actions workflow call this automatically.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

CONTENT_DIR = Path(__file__).parent.parent / "content"
INDEX_FILE = CONTENT_DIR / "index.json"
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
    for md_file in pages_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        new_hash = hash_content(content)
        old_hash = cache.get(md_file.name)
        if new_hash != old_hash:
            changed.append(md_file.name)
            cache[md_file.name] = new_hash
    return changed


def run_sync():
    """Check for content changes and report a sync summary."""
    pages_dir = CONTENT_DIR / "pages"
    if not pages_dir.exists():
        print("[SYNC] No content yet. Run the scraper first.")
        return

    cache = load_cache()
    changed = detect_changes(pages_dir, cache)
    save_cache(cache)

    summary = {
        "synced_at": datetime.utcnow().isoformat() + "Z",
        "changed_files": changed,
        "total_changed": len(changed),
    }

    summary_path = CONTENT_DIR / "sync_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    if changed:
        print(f"[SYNC] {len(changed)} file(s) updated: {', '.join(changed)}")
    else:
        print("[SYNC] No changes detected. Content is up to date.")

    return summary


if __name__ == "__main__":
    run_sync()
