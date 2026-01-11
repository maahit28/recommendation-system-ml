import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

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

def infer_region(language):
    return {
        "en": "hollywood",
        "hi": "bollywood",
        "ko": "korean",
        "ja": "anime"
    }.get(language, "other")

def fetch_movies(content_type="movie", genre="action", region="hollywood", pages=3):
    if not API_KEY:
        raise ValueError("TMDB_API_KEY environment variable is not set. Please check your .env file.")

    endpoint = "discover/movie" if content_type == "movie" else "discover/tv"

    genre_id = GENRE_MAP.get(genre)
    language = LANGUAGE_MAP.get(region, "en")

    results = []

    for page in range(1, pages + 1):
        params = {
            "api_key": API_KEY,
            "with_genres": genre_id,
            "with_original_language": language,
            "sort_by": "popularity.desc",
            "page": page
        }

        try:
            response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movies: {e}")
            continue

        for item in response.json().get("results", []):
            poster_path = item.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            results.append({
                "title": item.get("title") or item.get("name"),
                "description": item.get("overview", ""),
                "year": (item.get("release_date") or item.get("first_air_date", ""))[:4],
                "genre": genre,
                "region": infer_region(item.get("original_language")),
                "content_type": content_type,
                "popularity": item.get("popularity", 0),
                "poster_url": poster_url
            })

        time.sleep(0.3)

    return pd.DataFrame(results)
