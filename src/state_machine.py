"""Orchestrateur : enrichit une association de bout en bout."""
from src import normalize, search_engine, web_analyzer, scorer
from src.cache import get_cached, set_cache

def enrich_one(asso):
    rna = str(asso.get('url_source', '')).replace('RNA:', '').strip()
    nom = asso.get('nom_organisation', '')
    ville = asso.get('ville', '')

    cache_key = f"enrich:{rna}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    result = {
        "prospect_id": asso.get('prospect_id', ''),
        "nom_organisation": nom,
        "ville": ville,
        "site_web": "",
        "email": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "score": 0,
        "status": "no_footprint",
        "raisons": "",
    }

    nom_clean = normalize.clean_name(nom)
    if not nom_clean:
        result["status"] = "invalid_name"
        set_cache(cache_key, result)
        return result

    candidates = search_engine.multi_dork_search(nom_clean, ville)
    if not candidates:
        set_cache(cache_key, result)
        return result

    best = None
    best_score = 0
    best_signals = None
    best_raisons = []

    for cand in candidates[:5]:
        url = cand.get("url", "")
        if not url or web_analyzer.is_blacklisted(url):
            continue
        signals = web_analyzer.analyze_page(url, nom_clean, ville)
        if not signals.get("valid"):
            continue
        score, raisons = scorer.score_candidate(signals, nom, ville)
        if score > best_score:
            best_score = score
            best_signals = signals
            best = url
            best_raisons = raisons

    if best and best_signals:
        result["site_web"] = best
        result["score"] = best_score
        result["raisons"] = "|".join(best_raisons)
        emails = best_signals.get("emails", [])
        if emails:
            generic = [e for e in emails if any(p in e.lower() for p in ["contact@", "info@", "bonjour@"])]
            result["email"] = generic[0] if generic else emails[0]
        result["instagram"] = best_signals.get("instagram") or ""
        result["facebook"] = best_signals.get("facebook") or ""
        result["linkedin"] = best_signals.get("linkedin") or ""
        result["status"] = scorer.classify(best_score)

    set_cache(cache_key, result)
    return result
