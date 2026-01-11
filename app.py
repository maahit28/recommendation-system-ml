import streamlit as st
import pandas as pd
from hybrid import HybridMovieRecommender

# Page config MUST be first
st.set_page_config(page_title="Global Movie Recommender", layout="wide")

# App title
st.title("🎬 Global Movie Recommendation System")
st.markdown("Discover movies from across the world using AI.")

# Sidebar controls
st.sidebar.header("🎯 Preferences")

content_type = st.sidebar.selectbox(
    "Content Type",
    ["movie", "series"]
)

region = st.sidebar.selectbox(
    "Region",
    ["hollywood", "bollywood", "korean", "anime"]
)

genre = st.sidebar.selectbox(
    "Genre",
    ["action", "romance", "thriller", "comedy", "sci-fi", "drama", "documentary", "horror"]
)

top_n = st.sidebar.slider(
    "Number of recommendations",
    5, 20, 10
)

# User input
user_text = st.text_input(
    "🧠 What are you in the mood for?",
    placeholder="e.g. action hollywood movie"
)

# Load model once
@st.cache_resource
def load_model():
    return HybridMovieRecommender()

model = load_model()

# Button action
if st.button("🎯 Get Recommendations"):

    results = model.recommend(
        user_text=user_text,
        content_type=content_type,
        region=region,
        genre=genre,
        top_n=top_n
    )

    # Show detected intent
    if hasattr(model, "last_intent"):
        st.info(
            f"Detected Intent → "
            f"Genre: {model.last_intent['genre'].title()}, "
            f"Region: {model.last_intent['region'].title()}, "
            f"Type: {model.last_intent['content_type'].title()}"
        )

    # No results case
    if results.empty:
        st.error("No results found. Try different keywords.")
    else:
        st.success("✨ Recommended for you")

        # Display each movie
        for _, row in results.iterrows():

            # Two-column layout (poster | text)
            col1, col2 = st.columns([1, 4], gap="large")

            # Poster column
            with col1:
                if pd.notna(row["poster_url"]):
                    st.image(row["poster_url"], width=220)
                else:
                    st.image(
                        "https://via.placeholder.com/300x450?text=No+Poster",
                        width=220
                    )

            # Text column
            with col2:
                short_desc = " ".join(row["description"].split()[:35]) + "..."

                st.markdown(f"""
                <div style="padding-top:10px;">
                    <h3 style="margin-bottom:5px;">🎬 {row['title']} ({row['year']})</h3>
                    <p style="color:gray; font-size:14px; margin-top:0;">
                        {row['genre'].title()} | {row['region'].title()}
                    </p>
                    <p style="font-size:13px; line-height:1.6;">
                        {short_desc}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # Divider between movies
            st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)
