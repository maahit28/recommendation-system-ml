from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(df, user_text):
    texts = df["description"].fillna("").tolist()
    texts.append(user_text)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(texts)

    similarity_scores = cosine_similarity(tfidf[-1], tfidf[:-1])[0]
    df["similarity_score"] = similarity_scores

    return df
