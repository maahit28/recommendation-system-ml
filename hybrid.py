import pandas as pd
from recommender.recommender.filter import filter_movies
from similarity import TextSimilarityRecommender


class HybridMovieRecommender:
    def __init__(self, data_path="data/movies.csv"):
        # Load dataset
        self.df = pd.read_csv(data_path)

    def recommend(
        self,
        user_text,
        content_type=None,
        region=None,
        genre=None,
        top_n=15
    ):
        """
        Hybrid recommendation:
        1. Filter by preferences
        2. Rank by text similarity
        """

        # Step 1: Filter dataset
        filtered_df = filter_movies(
            self.df,
            content_type=content_type,
            region=region,
            genre=genre
        )

        # If no movies left after filtering
        if filtered_df.empty:
            return pd.DataFrame()

        # Step 2: Similarity ranking
        similarity_model = TextSimilarityRecommender(filtered_df)
        results = similarity_model.recommend(
            user_text=user_text,
            top_n=top_n
        )

        return results
