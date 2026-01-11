import streamlit as st
import pandas as pd
from hybrid import HybridMovieRecommender
import streamlit.components.v1 as components

st.set_page_config(page_title="Global Movie Recommendation System", layout="wide")


st.markdown("""
<style>

body {
    background-color: #0f172a;
}

h1 {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(90deg, #ff7eb3, #65d6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stTextInput > div > div > input {
    border-radius: 12px;
    padding: 10px;
    font-size: 16px;
}

.stButton > button {
    background: linear-gradient(90deg, #ff7eb3, #65d6ff);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
}

.stButton > button:hover {
    transform: scale(1.05);
    transition: 0.2s;
}

.sidebar .sidebar-content {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

st.title("🎬 Global Movie Recommendation System")
st.markdown("Discover movies, series, and documentaries from across the world.")

# Sidebar
st.sidebar.header("🎯 Preferences")
content_type = st.sidebar.selectbox("Content Type", ["movie", "series"])
region = st.sidebar.selectbox("Region", ["hollywood", "bollywood", "korean", "anime"])
genre = st.sidebar.selectbox(
    "Genre",
    ["action", "romance", "thriller", "horror", "comedy", "sci-fi", "drama", "documentary"]
)
top_n = st.sidebar.slider("Number of recommendations", 5, 20, 10)

st.subheader("🧠 What are you in the mood for?")
user_text = st.text_input("Describe what you want to watch", placeholder="e.g. horror korean movies")

@st.cache_resource
def load_model():
    return HybridMovieRecommender()

model = load_model()

if st.button("🎯 Get Recommendations"):
    results = model.recommend(user_text, content_type, region, genre, top_n)

    if hasattr(model, "last_intent"):
        st.info(
            f"Detected Intent → "
            f"Genre: {model.last_intent['genre'].title()}, "
            f"Region: {model.last_intent['region'].title()}, "
            f"Type: {model.last_intent['content_type'].title()}"
        )

    if results.empty:
        st.error("No results found. Try changing preferences.")
    else:
        st.success("✨ Recommended for you")

        for _, row in results.iterrows():
            short_desc = " ".join(row["description"].split()[:40]) + "..."
            poster = row["poster_url"] if pd.notna(row["poster_url"]) else "https://via.placeholder.com/300x450?text=No+Poster"

            html = f"""
<div style="
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
    padding: 18px;
    background: linear-gradient(135deg, #1f2937, #111827);
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    color: white;
">

    <div style="flex: 0 0 200px;">
        <img src="{poster}" style="width:200px; border-radius:12px;" />
    </div>

    <div style="flex: 1;">
        <h3 style="margin-bottom:5px; color:#ffb6c1;">🎬 {row['title']} ({row['year']})</h3>

        <p style="color:#9ca3af; font-size:14px; margin-top:0;">
            {(row['genre'] or 'Unknown').title()} | {(row['region'] or 'Unknown').title()}
        </p>

        <p style="font-size:13px; line-height:1.6; color:#e5e7eb;">
            {short_desc}
        </p>
    </div>
</div>
"""
