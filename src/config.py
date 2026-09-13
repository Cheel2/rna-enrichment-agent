"""Configuration centrale de la machine d'enrichissement."""

SEARXNG_URL = "http://searxng:8080"
THROTTLE_SECONDS = 2
MAX_RESULTS_PER_QUERY = 10
MAX_FALLBACK_CYCLES = 2
REQUEST_TIMEOUT = 15

CACHE_DB_PATH = "/app/data/cache/enrichment.db"
CACHE_TTL_DAYS = 30

SCORE_ACCEPT_THRESHOLD = 20
SCORE_GRAY_ZONE_MIN = 12
SCORE_MAX = 40

WEIGHTS = {
    "domain_match": 10,
    "name_on_page": 8,
    "city_on_page": 6,
    "is_association": 5,
    "has_email": 5,
    "has_instagram": 3,
    "has_facebook": 3,
    "has_tiktok": 2,
    "has_twitter": 2,
    "has_youtube": 2,
}

BLACKLIST_DOMAINS = [
    "pagesjaunes.fr", "societe.com", "asso.fr", "francebenevolat.org",
    "recherchebenevole.org", "net1901.org", "journal-officiel.gouv.fr",
    "annuaire-entreprises.data.gouv.fr", "linkedin.com",
    "wikipedia.org", "youtube.com",
    "pappers.fr", "verif.com", "bodacc.fr",
]

PARKING_SIGNATURES = [
    "sedo.com", "bodis.com", "hugedomains", "godaddy.com",
    "this domain is for sale", "buy this domain", "domain for sale",
]

COMING_SOON_SIGNATURES = [
    "coming soon", "site en construction", "under construction",
    "ce site est en cours de creation", "page en construction",
]

DORK_PATTERNS = [
    "{nom} {ville} association",
    "{nom} {ville} site:facebook.com",
    "{nom} {ville} site:helloasso.com",
    "{nom} contact email",
]

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
GENERIC_PREFIXES = ["contact", "info", "bonjour", "hello", "asso", "administration"]
