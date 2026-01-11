import streamlit as st
import pandas as pd
from hybrid import HybridMovieRecommender

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Global Movie Recommendation System", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #fff1eb, #e6f0ff);
    font-family: "Segoe UI", sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffe29f, #ffa99f);
}

/* Headings */
h1, h2, h3, h4 {
    color: #1f3c88;
}

/* Subtitle */
.subtitle {
    color: #000;
    font-size: 17px;
    font-weight: 600;
}

/* Button Animation */
.stButton > button {
    background: linear-gradient(90deg, #ff6ec4, #7873f5);
    color: white;
    border-radius: 25px;
    padding: 10px 24px;
    font-size: 16px;
    border: none;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.08);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.2);
}

/* Movie Card */
.movie-card {
    background: white;
    border-radius: 18px;
    padding: 15px;
    margin-bottom: 25px;
    box-shadow: 0px 6px 15px rgba(0,0,0,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.movie-card:hover {
    transform: translateY(-8px);
    box-shadow: 0px 12px 25px rgba(0,0,0,0.18);
}

/* Badges */
.badge {
    display: inline-block;
    background: #ffd6e8;
    color: #d63384;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 13px;
    margin-right: 8px;
}

/* Like Button */
.like-btn {
    background: #ffe6f0;
    border: none;
    border-radius: 20px;
    padding: 6px 12px;
    cursor: pointer;
    font-size: 14px;
}

.like-btn:hover {
    background: #ffb3d9;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1>🎬 Global Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>✨ Discover aesthetic movie vibes from across the world</p>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 🎯 Your Preferences")

content_type = st.sidebar.selectbox("🎞 Content Type", ["movie", "series"])
region = st.sidebar.selectbox("🌍 Region", ["hollywood", "bollywood", "korean", "anime"])
genre = st.sidebar.selectbox("🎭 Genre", ["action", "romance", "thriller", "comedy", "sci-fi", "drama", "documentary"])
top_n = st.sidebar.slider("🔢 Number of results", 5, 20, 10)

# ---------------- USER INPUT ----------------
st.markdown("## 🧠 What are you in the mood for?")
user_text = st.text_input("Describe what you want to watch", placeholder="e.g. romantic korean drama, action bollywood movie")

# ---------------- MODEL ----------------
@st.cache_resource
def load_model():
    return HybridMovieRecommender()

model = load_model()

# ---------------- SESSION STATE (LIKES) ----------------
if "liked_movies" not in st.session_state:
    st.session_state.liked_movies = set()

# ---------------- RECOMMEND BUTTON ----------------
if st.button("✨ Get Recommendations"):
    
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
        st.success("🌸 Recommended for you")

        for idx, row in results.iterrows():
            short_desc = " ".join(row["description"].split()[:35]) + "..."

            col1, col2 = st.columns([1, 3])

            with col1:
                if pd.notna(row["poster_url"]):
                    st.image(row["poster_url"], width=220)
                else:
                    st.image("https://via.placeholder.com/300x450?text=No+Poster", width=220)

            with col2:
                liked = row["title"] in st.session_state.liked_movies

                st.markdown(f"""
                <div class="movie-card">
                    <h3>🎬 {row['title']} ({row['year']})</h3>
                    <span class="badge">{row['genre'].title()}</span>
                    <span class="badge">{row['region'].title()}</span>
                    <p style="font-size:14px; margin-top:10px;">{short_desc}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button("💖 Like" if not liked else "💗 Liked", key=f"like_{idx}"):
                    st.session_state.liked_movies.add(row["title"])

# ---------------- LIKED MOVIES SECTION ----------------
if st.session_state.liked_movies:
    st.markdown("## 💖 Your Liked Movies")
    for movie in st.session_state.liked_movies:
        st.markdown(f"• {movie}")
