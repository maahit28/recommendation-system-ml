import pandas as pd
import basic_recommender

def load_movies(path="data/movies.csv"):
    """
    Load movie dataset
    """
    return pd.read_csv(path)


def filter_movies(
    df,
    content_type=None,
    region=None,
    genre=None
):
    """
    Filter movies based on user preferences
    """
    filtered_df = df.copy()

    if content_type:
        filtered_df = filtered_df[
            filtered_df["content_type"] == content_type
        ]

    if region:
        filtered_df = filtered_df[
            filtered_df["region"] == region
        ]

    if genre:
        filtered_df = filtered_df[
            filtered_df["genre"] == genre
        ]

    return filtered_df
