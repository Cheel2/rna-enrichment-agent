"""Analyse des pages web : detection pieges + extraction signaux."""
import re
import requests
import tldextract
from bs4 import BeautifulSoup
from src import config

def get_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain

def is_blacklisted(url):
    domain = get_domain(url)
    return any(b in domain or b in url for b in config.BLACKLIST_DOMAINS)

def is_parking_page(html):
    html_lower = html.lower()
    return any(sig in html_lower for sig in config.PARKING_SIGNATURES)

def is_coming_soon(html):
    html_lower = html.lower()
    return any(sig in html_lower for sig in config.COMING_SOON_SIGNATURES)

def fetch_page(url):
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; RNAEnricher/1.0)"},
            timeout=config.REQUEST_TIMEOUT,
            allow_redirects=True
        )
        if resp.status_code == 200 and "text/html" in resp.headers.get("content-type", ""):
            return resp.text
    except Exception:
        pass
    return ""

def analyze_page(url, asso_name, ville):
    html = fetch_page(url)
    if not html:
        return {"url": url, "valid": False, "reason": "no_response"}

    if is_parking_page(html):
        return {"url": url, "valid": False, "reason": "parking"}

    if is_coming_soon(html):
        return {"url": url, "valid": False, "reason": "coming_soon"}

    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text().lower()

    signals = {
        "url": url,
        "valid": True,
        "name_on_page": asso_name.lower()[:30] in text if asso_name else False,
        "city_on_page": ville.lower() in text if ville else False,
        "is_association": "association" in text or "asso " in text,
        "emails": [],
        "instagram": None,
        "facebook": None,
        "linkedin": None,
        "domain": get_domain(url),
    }

    emails = set(re.findall(config.EMAIL_REGEX, html))
    signals["emails"] = [e for e in emails if not e.endswith(('.png', '.jpg', '.gif'))][:5]

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "instagram.com/" in href and not signals["instagram"]:
            signals["instagram"] = href
        elif "facebook.com/" in href and "sharer" not in href and not signals["facebook"]:
            signals["facebook"] = href
        elif "linkedin.com/company/" in href and not signals["linkedin"]:
            signals["linkedin"] = href

    return signals
