import requests
from cache import get_cached_answer, store_cached_answer

def search_duckduckgo(query):
    """Search DuckDuckGo for a meaningful short answer with caching."""
    query = query.strip().lower()

    # 🔹 Step 1: Try to retrieve cached result
    cached_answer = get_cached_answer(query)
    if cached_answer:
        return f"(From cache) {cached_answer}"

    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
        response = requests.get(url, timeout=5)
        data = response.json()

        answer = None

        # 1️⃣ Prefer direct abstract
        if data.get("AbstractText"):
            answer = data["AbstractText"]

        # 2️⃣ Try related topics
        elif data.get("RelatedTopics"):
            for topic in data["RelatedTopics"]:
                if isinstance(topic, dict) and topic.get("Text"):
                    answer = topic["Text"]
                    break

        # 3️⃣ Try heading
        elif data.get("Heading"):
            answer = f"{data['Heading']} is related to {query}."

        # 4️⃣ If still nothing
        if not answer:
            answer = f"I looked online but couldn't find a detailed answer about {query}. It might need a more specific question."

        # 🔹 Step 2: Store result in cache
        store_cached_answer(query, answer)
        return answer

    except requests.exceptions.ConnectionError:
        # 🔹 Offline: Try cache again
        cached_answer = get_cached_answer(query)
        if cached_answer:
            return f"(Offline from cache) {cached_answer}"
        return "It seems there's no internet connection right now, and I couldn't find this in my cache."

    except Exception as e:
        print(f"⚠️ DuckDuckGo search failed: {e}")
        return "I'm having trouble accessing online results right now."
import wikipedia

def search_duckduckgo(query):
    query = query.strip().lower()

    # Try cache first (if using cache_manager)
    from cache import get_cached_answer, store_cached_answer
    cached = get_cached_answer(query)
    if cached:
        return f"(From cache) {cached}"

    try:
        # Try DuckDuckGo first
        import requests
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
        res = requests.get(url, timeout=5)
        data = res.json()

        if data.get("AbstractText"):
            answer = data["AbstractText"]
        elif data.get("RelatedTopics"):
            for topic in data["RelatedTopics"]:
                if isinstance(topic, dict) and topic.get("Text"):
                    answer = topic["Text"]
                    break
        else:
            # Fallback to Wikipedia
            try:
                answer = wikipedia.summary(query, sentences=2, auto_suggest=True)
            except Exception:
                answer = f"I couldn't find detailed information about {query} online."

        # Cache it
        store_cached_answer(query, answer)
        return answer

    except requests.exceptions.ConnectionError:
        cached = get_cached_answer(query)
        if cached:
            return f"(Offline from cache) {cached}"
        return "It seems there's no internet connection right now."

    except Exception as e:
        print(f"⚠️ Error: {e}")
        try:
            answer = wikipedia.summary(query, sentences=2)
            return answer
        except:
            return "I'm having trouble fetching online data right now."
