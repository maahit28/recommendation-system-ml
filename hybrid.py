from tmdb_client import fetch_movies
from similarity import compute_similarity

class HybridMovieRecommender:

    def recommend(self, user_text, content_type="movie", region="hollywood", genre="action", top_n=10):

        text = user_text.lower()

        INTENT_GENRE = {
            "romance": ["romantic", "love"],
            "action": ["action", "fight", "war"],
            "thriller": ["thriller", "crime", "mystery"],
            "sci-fi": ["sci-fi", "space", "future"],
            "documentary": ["documentary", "real"],
            "horror": ["horror", "scary", "ghost"]
        }

        INTENT_REGION = {
            "korean": ["korean", "k-drama"],
            "anime": ["anime"],
            "bollywood": ["bollywood", "hindi"],
            "hollywood": ["hollywood"]
        }

        for g, keys in INTENT_GENRE.items():
            if any(k in text for k in keys):
                genre = g
                break

        for r, keys in INTENT_REGION.items():
            if any(k in text for k in keys):
                region = r
                break

        if any(k in text for k in ["series", "show", "drama"]):
            content_type = "series"

        df = fetch_movies(content_type, genre, region)

        if df.empty:
            df = fetch_movies("movie", genre, "hollywood")

        if df.empty:
            return df

        df = compute_similarity(df, user_text)

        df["popularity_norm"] = df["popularity"] / df["popularity"].max()
        df["final_score"] = 0.8 * df["similarity_score"] + 0.2 * df["popularity_norm"]

        df = df.sort_values("final_score", ascending=False)

        self.last_intent = {
            "genre": genre,
            "region": region,
            "content_type": content_type
        }

        return df.head(top_n)
