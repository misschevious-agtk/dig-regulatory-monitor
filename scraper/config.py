"""
config.py
Central configuration for the scraper and sync modules.
"""
 
SCRAPER_CONFIG = {
    "base_url": "https://misschevious-agtk.github.io/dig-regulatory-monitor/",
    "timeout": 15,
    "user_agent": "ToqanAgent/1.0 (+https://github.com/misschevious-agtk/dig-regulatory-monitor)",
    "trending_count": 5,
    "max_per_category": 20,
}
 
SOURCES = [
    {"label": "European Commission",    "url": "https://ec.europa.eu/commission/presscorner/home/en"},
    {"label": "Digital Watch Observatory", "url": "https://dig.watch/updates"},
    {"label": "ICO (UK)",               "url": "https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/"},
    {"label": "EDPB",                   "url": "https://www.edpb.europa.eu/news/news_en"},
    {"label": "Politico Tech",          "url": "https://www.politico.eu/section/technology/"},
]
 
CATEGORY_KEYWORDS = {
    "competition": [
        "competition law", "antitrust", "cartel", "abuse of dominance",
        "market power", "merger", "digital markets act", "DMA", "gatekeeper",
        "interoperability", "self-preferencing", "tying", "bundling",
        "price fixing", "market sharing", "bid rigging",
        "Competition Commission", "CCI", "FTC", "DOJ", "Bundeskartellamt", "CMA",
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
    "ai": [
        "artificial intelligence", "AI model", "machine learning", "large language model",
        "LLM", "generative AI", "foundation model", "AI Act", "AI governance",
        "AI regulation", "AI Office", "AI liability", "AI safety", "AI risk",
        "AI audit", "AI transparency", "AI bias", "deepfake", "autonomous system",
        "AI accountability", "AI enforcement", "AI compliance", "ChatGPT", "Claude",
        "Gemini", "Grok", "AI agent", "agentic", "AI standard", "ISO 42001",
    ],
    "regulatory": [
        "DSA", "digital services act", "regulation enters into force",
        "compliance deadline", "enforcement begins", "regulatory framework",
        "consultation", "legislative proposal", "delegated act", "implementing act",
        "guideline", "guidance", "ecommerce regulation", "platform regulation", "NIS2",
    ],
}
