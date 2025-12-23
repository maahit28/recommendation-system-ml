import streamlit as st
from recommender import recommend_movie, recommend_food
from ml.movie_ml import predict_genre

st.set_page_config(page_title="Recommendation System", layout="centered")

st.title("🎬🍔 Recommendation System")
st.write("Rule-based + ML-based Recommendation System")

option = st.selectbox(
    "Choose recommendation type",
    ("Movie (Rule-based)", "Food (Rule-based)", "Movie (ML-based)")
)

# Rule-based Movie
if option == "Movie (Rule-based)":
    genre = st.selectbox(
        "Select genre",
        ("action", "comedy", "romance", "thriller")
    )
    if st.button("Get Recommendations"):
        movies = recommend_movie(genre)
        if movies:
            st.subheader("Recommended Movies")
            for m in movies:
                st.write("•", m)
        else:
            st.warning("No recommendations found.")

# Rule-based Food
elif option == "Food (Rule-based)":
    taste = st.selectbox(
        "Select taste",
        ("spicy", "sweet", "salty")
    )
    if st.button("Get Recommendations"):
        foods = recommend_food(taste)
        if foods:
            st.subheader("Recommended Food Items")
            for f in foods:
                st.write("•", f)
        else:
            st.warning("No recommendations found.")

# ML-based Movie
else:
    description = st.text_input("Describe the movie you want to watch")
    if st.button("Predict & Recommend"):
        if description.strip():
            genre = predict_genre(description)
            st.success(f"Predicted genre: {genre}")
            movies = recommend_movie(genre)
            for m in movies:
                st.write("•", m)
        else:
            st.warning("Please enter a description.")
