"""Scoring d'un candidat (0-40 points)."""
from src import config

def score_candidate(signals, asso_name, ville):
    score = 0
    details = []

    nom_slug = (asso_name or "").lower().replace(' ', '')[:10]
    if nom_slug and nom_slug in signals.get("domain", "").lower():
        score += config.WEIGHTS["domain_match"]
        details.append(f"domain_match:+{config.WEIGHTS['domain_match']}")

    if signals.get("name_on_page"):
        score += config.WEIGHTS["name_on_page"]
        details.append(f"name_on_page:+{config.WEIGHTS['name_on_page']}")

    if signals.get("city_on_page"):
        score += config.WEIGHTS["city_on_page"]
        details.append(f"city_on_page:+{config.WEIGHTS['city_on_page']}")

    if signals.get("is_association"):
        score += config.WEIGHTS["is_association"]
        details.append(f"is_association:+{config.WEIGHTS['is_association']}")

    if signals.get("emails"):
        score += config.WEIGHTS["has_email"]
        details.append(f"has_email:+{config.WEIGHTS['has_email']}")

    if signals.get("instagram"):
        score += config.WEIGHTS["has_instagram"]
        details.append(f"has_instagram:+{config.WEIGHTS['has_instagram']}")

    if signals.get("facebook"):
        score += config.WEIGHTS["has_facebook"]
        details.append(f"has_facebook:+{config.WEIGHTS['has_facebook']}")

    return min(score, config.SCORE_MAX), details

def classify(score):
    if score >= config.SCORE_ACCEPT_THRESHOLD:
        return "ACCEPTED"
    elif score >= config.SCORE_GRAY_ZONE_MIN:
        return "GRAY_ZONE"
    else:
        return "REJECTED"
