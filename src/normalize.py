"""Normalisation des noms d'associations."""
import re
import unicodedata

STOP_WORDS = [
    r"\bASSOCIATION\b", r"\bAMICALE\b", r"\bFEDERATION\b",
    r"\bBUREAU DES ELEVES\b", r"\bBDE\b", r"\bCOMITE\b",
    r"\bCLUB\b", r"\bCOLLECTIF\b", r"\bUNION\b",
    r"\bDES\b", r"\bDE\b", r"\bDU\b", r"\bLA\b", r"\bLE\b", r"\bLES\b",
    r"\bET\b", r"\bEN\b", r"\bAU\b", r"\bAUX\b",
    r"\bLOI 1901\b", r"\b1901\b",
]

def strip_accents(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

def clean_name(name):
    """Nettoie un nom d'association pour la recherche web."""
    if not name:
        return ""
    name = str(name).upper()
    name = strip_accents(name)
    for pattern in STOP_WORDS:
        name = re.sub(pattern, ' ', name)
    name = re.sub(r'[^A-Z0-9\s\-]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name.lower()

def suggest_domains(clean_nom):
    """Suggère des domaines probables depuis le nom nettoyé."""
    slug = clean_nom.replace(' ', '-')
    slug_compact = clean_nom.replace(' ', '')
    return [
        f"{slug}.fr",
        f"{slug}.com",
        f"{slug}.org",
        f"{slug_compact}.fr",
        f"{slug_compact}.com",
    ]
