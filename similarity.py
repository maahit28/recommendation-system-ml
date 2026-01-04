import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextSimilarityRecommender:
    def __init__(self, df):
        """
        Initialize with movie dataframe
        """
        self.df = df.reset_index(drop=True)

        # TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        # Fit on movie descriptions
        # Create enriched text for better similarity
        self.df["combined_text"] = (
        self.df["genre"] + " " +
        self.df["region"] + " " +
        self.df["description"]
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(
        self.df["combined_text"]
        )


    def recommend(self, user_text, top_n=15):
        """
        Recommend top N movies based on free text
        """
        # Vectorize user input
        user_vec = self.vectorizer.transform([user_text])

        # Compute cosine similarity
        similarities = cosine_similarity(
            user_vec, self.tfidf_matrix
        ).flatten()

        # Add similarity scores to dataframe
        self.df["similarity_score"] = similarities

        # Sort by similarity
        results = self.df.sort_values(
            by="similarity_score",
            ascending=False
        )

        return results.head(top_n)