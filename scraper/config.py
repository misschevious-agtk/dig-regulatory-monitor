"""
config.py
Central configuration for the scraper and sync modules.
Update BASE_URL to point to your live website.
"""

SCRAPER_CONFIG = {
    # ── Target website ────────────────────────────────────────────────────────
    "base_url": "https://maleevskaina.github.io/dig-regulatory-monitor",
    # Change to your live URL if different, e.g. a custom domain.

    # ── Scraper behaviour ─────────────────────────────────────────────────────
    "follow_links": True,        # Crawl internal links automatically
    "max_pages": 100,            # Safety cap – set to None for unlimited
    "timeout": 15,               # HTTP request timeout in seconds
    "user_agent": "ToqanAgent/1.0 (+https://github.com/maleevskaina/toqan-agent)",

    # ── Output ────────────────────────────────────────────────────────────────
    "output_format": "markdown",  # Options: "markdown" | "json"
}
