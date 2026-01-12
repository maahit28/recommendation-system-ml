import os
import time
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

if not API_KEY:
    raise ValueError("TMDB API key not found in .env")

session = requests.Session()

retries = Retry(
    total=5,
    backoff_factor=1.5,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

GENRE_MAP = {
    "action": 28,
    "romance": 10749,
    "comedy": 35,
    "thriller": 53,
    "drama": 18,
    "sci-fi": 878,
    "documentary": 99,
    "horror": 27
}

LANGUAGE_MAP = {
    "hollywood": "en",
    "bollywood": "hi",
    "korean": "ko",
    "anime": "ja"
}

def infer_region(lang):
    return {
        "en": "hollywood",
        "hi": "bollywood",
        "ko": "korean",
        "ja": "anime"
    }.get(lang, "other")

def fetch_movies(content_type="movie", genre="action", region="hollywood", pages=2):

    endpoint = "discover/movie" if content_type == "movie" else "discover/tv"

    genre_id = GENRE_MAP.get(genre)
    language = LANGUAGE_MAP.get(region, "en")

    results = []

    for page in range(1, pages + 1):

        params = {
            "api_key": API_KEY,
            "sort_by": "popularity.desc",
            "page": page
        }

        if genre_id:
            params["with_genres"] = genre_id

        if language:
            params["with_original_language"] = language

        try:
            response = session.get(
                f"{BASE_URL}/{endpoint}",
                params=params,
                headers=HEADERS,
                timeout=10
            )

            response.raise_for_status()

            data = response.json().get("results", [])

            for item in data:
                lang = item.get("original_language")

                results.append({
                    "title": item.get("title") or item.get("name"),
                    "description": item.get("overview", ""),
                    "year": (item.get("release_date") or item.get("first_air_date", ""))[:4],
                    "genre": genre,
                    "region": infer_region(lang),
                    "content_type": content_type,
                    "popularity": item.get("popularity", 0),
                    "poster_url": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get("poster_path") else None
                })

            time.sleep(0.5)

        except Exception as e:
            print("Error fetching movies:", e)
            continue

    return pd.DataFrame(results)
