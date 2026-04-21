"""
config.py
Central configuration for the scraper and sync modules.
"""
 
SCRAPER_CONFIG = {
    # ── Target ────────────────────────────────────────────────────────────────
    "base_url": "https://maleevskaina.github.io/dig-regulatory-monitor",
 
    # ── Behaviour ─────────────────────────────────────────────────────────────
    "timeout": 15,
    "user_agent": "ToqanAgent/1.0 (+https://github.com/maleevskaina/dig-regulatory-monitor)",
 
    # ── Output ────────────────────────────────────────────────────────────────
    "trending_count": 5,        # How many articles appear in Trending Today
    "max_per_category": 20,     # Max articles stored per category
}
 
# ── News sources to scrape ─────────────────────────────────────────────────────
# Add or remove sources here. Each entry needs a url and a display label.
SOURCES = [
    {
        "label": "European Commission",
        "url": "https://ec.europa.eu/commission/presscorner/home/en",
    },
    {
        "label": "Digital Watch Observatory",
        "url": "https://dig.watch/updates",
    },
    {
        "label": "ICO (UK)",
        "url": "https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/",
    },
    {
        "label": "EDPB",
        "url": "https://www.edpb.europa.eu/news/news_en",
    },
    {
        "label": "Politico Tech",
        "url": "https://www.politico.eu/section/technology/",
    },
    # Add more sources as needed:
    # { "label": "CCI India", "url": "https://cci.gov.in/press-release" },
    # { "label": "FTC", "url": "https://www.ftc.gov/news-events/news" },
]
 
# ── Category keyword matching ──────────────────────────────────────────────────
# The scraper scores each article against these keyword lists.
# The category with the most keyword matches wins.
CATEGORY_KEYWORDS = {
    "competition": [
        "competition law", "antitrust", "cartel", "abuse of dominance",
        "market power", "merger", "digital markets act", "DMA", "gatekeeper",
        "interoperability", "self-preferencing", "tying", "bundling",
        "price fixing", "market sharing", "bid rigging",
        "Competition Commission", "CCI", "FTC", "DOJ", "Bundeskartellamt",
        "CMA", "European Commission competition",
    ],
    "privacy": [
        "data protection", "personal data", "GDPR", "privacy", "consent",
        "data subject", "data controller", "data processor", "data breach",
        "supervisory authority", "DPA", "ICO", "CNIL", "AP ", "EDPB",
        "DPDPA", "LGPD", "PIPL", "UK GDPR", "data transfer", "SCCs",
        "adequacy decision", "cookie", "tracking",
    ],
    "ip": [
        "intellectual property", "copyright", "patent", "trademark",
        "trade secret", "design right", "database right", "infringement",
        "AI-generated", "authorship", "originality", "CJEU copyright",
        "USPTO", "EPO", "WIPO", "licensing", "fair use", "fair dealing",
    ],
    "regulatory": [
        "AI Act", "artificial intelligence regulation", "DSA", "digital services act",
        "regulation enters into force", "compliance deadline", "enforcement begins",
        "regulatory framework", "consultation", "legislative proposal",
        "delegated act", "implementing act", "guideline", "guidance",
        "ecommerce regulation", "platform regulation", "NIS2",
    ],
}
