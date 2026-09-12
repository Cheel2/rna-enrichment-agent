"""Test de connectivite SearXNG."""
import sys
sys.path.insert(0, '/app')
from src.search_engine import search

print("Test SearXNG...")
results = search("association maliens tours")
print(f"{len(results)} resultats")
for r in results[:3]:
    print(f"   - {r['title'][:60]} -> {r['url']}")
