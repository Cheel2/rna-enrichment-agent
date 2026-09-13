"""Point d'entree du pipeline d'enrichissement."""
import sys
import os
import time
import pandas as pd

sys.path.insert(0, '/app')

from src import config
from src.cache import init_db
from src.state_machine import enrich_one

INPUT = "/app/data/input/prospects_A_B.xlsx"
OUTPUT = "/app/data/output/prospects_enrichis.xlsx"

def main():
    print("=" * 70)
    print("ENRICHISSEMENT RNA - DEMARRAGE")
    print("=" * 70)

    init_db()

    if not os.path.exists(INPUT):
        print(f"Fichier introuvable : {INPUT}")
        print("   -> Copie prospects_A_B.xlsx dans data/input/")
        return

    df = pd.read_excel(INPUT, dtype=str).fillna('')
    total = len(df)
    print(f"{total} prospects a enrichir")
    print(f"Throttle : {config.THROTTLE_SECONDS}s | Max cycles : {config.MAX_FALLBACK_CYCLES}")
    print("=" * 70)

    results = []
    t0 = time.time()

    for i, (_, row) in enumerate(df.iterrows(), 1):
        asso = row.to_dict()
        result = enrich_one(asso)
        results.append(result)

        if i % 10 == 0 or i == total:
            elapsed = time.time() - t0
            rate = i / elapsed if elapsed > 0 else 0
            eta = (total - i) / rate if rate > 0 else 0
            accepted = sum(1 for r in results if r['status'] == 'ACCEPTED')
            gray = sum(1 for r in results if r['status'] == 'GRAY_ZONE')
            print(f"   [{i:>4}/{total}] {rate:.2f} asso/s | ETA {eta/60:.1f} min | OK{accepted} WARN{gray}")

    df_result = pd.DataFrame(results)
    df_merged = df.merge(
        df_result[['prospect_id', 'site_web', 'email', 'instagram',
                   'facebook', 'linkedin', 'tiktok', 'twitter', 'youtube', 'score', 'status', 'raisons']],
        on='prospect_id', how='left'
    )

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    df_merged.to_excel(OUTPUT, index=False)

    print("\n" + "=" * 70)
    print("RESULTATS")
    print("=" * 70)
    print(f"ACCEPTED     : {df_result['status'].eq('ACCEPTED').sum()}")
    print(f"GRAY_ZONE    : {df_result['status'].eq('GRAY_ZONE').sum()}")
    print(f"REJECTED     : {df_result['status'].eq('REJECTED').sum()}")
    print(f"NO_FOOTPRINT : {df_result['status'].eq('no_footprint').sum()}")
    print(f"\nAvec email   : {df_result['email'].astype(bool).sum()}")
    print(f"Avec Insta   : {df_result['instagram'].astype(bool).sum()}")
    print(f"Avec FB      : {df_result['facebook'].astype(bool).sum()}")
    print(f"\nExport : {OUTPUT}")

if __name__ == "__main__":
    main()
