"""Client SearXNG avec throttling et cache."""
import time
import requests
from src import config
from src.cache import get_cached, set_cache

_last_request = [0]

def _throttle():
    elapsed = time.time() - _last_request[0]
    if elapsed < config.THROTTLE_SECONDS:
        time.sleep(config.THROTTLE_SECONDS - elapsed)
    _last_request[0] = time.time()

def search(query, max_results=None):
    max_results = max_results or config.MAX_RESULTS_PER_QUERY
    cache_key = f"search:{query}"
    cached = get_cached(cache_key)
    if cached is not None:
        return cached

    _throttle()
    try:
        resp = requests.get(
            f"{config.SEARXNG_URL}/search",
            params={"q": query, "format": "json", "language": "fr"},
            timeout=config.REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for r in data.get("results", [])[:max_results]:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", ""),
            })
        set_cache(cache_key, results)
        return results
    except Exception as e:
        print(f"   WARN Search error '{query}': {e}")
        return []

def multi_dork_search(nom_clean, ville, max_cycles=config.MAX_FALLBACK_CYCLES):
    all_results = []
    for i, pattern in enumerate(config.DORK_PATTERNS[:max_cycles + 2]):
        query = pattern.format(nom=nom_clean, ville=ville)
        results = search(query)
        if results:
            all_results.extend(results)
            if len(all_results) >= 5:
                break
    return all_results
