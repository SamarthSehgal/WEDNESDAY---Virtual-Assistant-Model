import json
import os

CACHE_FILE = "search_cache.json"

def load_cache():
    """Load cached search results from disk."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_cache(cache):
    """Save cache to disk."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_cached_answer(query):
    """Retrieve cached answer for a query if it exists."""
    cache = load_cache()
    return cache.get(query.lower())

def store_cached_answer(query, answer):
    """Store a query-answer pair in cache."""
    cache = load_cache()
    cache[query.lower()] = answer
    save_cache(cache)
