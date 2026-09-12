"""Cache SQLite avec TTL."""
import sqlite3
import json
import os
from datetime import datetime, timedelta
from src import config

def init_db():
    os.makedirs(os.path.dirname(config.CACHE_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(config.CACHE_DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_cached(key):
    try:
        conn = sqlite3.connect(config.CACHE_DB_PATH)
        row = conn.execute(
            "SELECT value, created_at FROM cache WHERE key = ?", (key,)
        ).fetchone()
        conn.close()
    except Exception:
        return None
    if not row:
        return None
    value, created_at = row
    age = datetime.now() - datetime.fromisoformat(created_at)
    if age > timedelta(days=config.CACHE_TTL_DAYS):
        return None
    return json.loads(value)

def set_cache(key, value):
    os.makedirs(os.path.dirname(config.CACHE_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(config.CACHE_DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO cache (key, value, created_at) VALUES (?, ?, ?)",
        (key, json.dumps(value, ensure_ascii=False), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
