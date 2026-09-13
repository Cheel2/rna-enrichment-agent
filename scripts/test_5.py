import sys
sys.path.insert(0, '/app')
import pandas as pd
from src.state_machine import enrich_one
df = pd.read_excel('/app/data/input/test_5.xlsx', dtype=str).fillna('')
for i, row in df.iterrows():
    r = enrich_one(row.to_dict())
    n = str(r.get('nom_organisation',''))[:40]
    s = r.get('status','')
    sc = r.get('score',0)
    tt = bool(r.get('tiktok'))
    tw = bool(r.get('twitter'))
    yt = bool(r.get('youtube'))
    print(f'[{i+1}/5] {n} -> {s} (score {sc}) | TT:{tt} TW:{tw} YT:{yt}')
