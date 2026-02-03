import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_movies():
    return pickle.load(open("movies.pkl", "rb"))

movies = load_movies()

# --------------------------------------------------
# COMPUTE SIMILARITY (NO PKL FILE)
# --------------------------------------------------
@st.cache_resource
def compute_similarity(movies_df):
    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(movies_df["tags"]).toarray()
    similarity = cosine_similarity(vectors)
    return similarity

similarity = compute_similarity(movies)

# --------------------------------------------------
# TMDB CONFIG
# --------------------------------------------------
API_KEY = st.secrets["TMDB_API_KEY"]
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

# --------------------------------------------------
# FETCH MOVIE DETAILS
# --------------------------------------------------
@st.cache_data
def fetch_movie_details(movie_id):
    try:
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
        providers_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"

        details = requests.get(details_url).json()
        credits = requests.get(credits_url).json()
        providers = requests.get(providers_url).json()

        poster = (
            POSTER_BASE_URL + details["poster_path"]
            if details.get("poster_path")
            else None
        )

        genres = ", ".join([g["name"] for g in details.get("genres", [])])
        director = next(
            (c["name"] for c in credits.get("crew", []) if c["job"] == "Director"),
            "Unknown",
        )
        cast = ", ".join([c["name"] for c in credits.get("cast", [])[:5]])

        watch_link = None
        if "results" in providers and "IN" in providers["results"]:
            watch_link = providers["results"]["IN"].get("link")

        return poster, genres, director, cast, watch_link

    except Exception:
        return None, "N/A", "N/A", "N/A", None

# --------------------------------------------------
# RECOMMEND FUNCTION (FIXED COUNT)
# --------------------------------------------------
def recommend(movie_name, n=5):
    index = movies[movies["title"] == movie_name].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in distances[1 : n + 1]:
        recommendations.append(movies.iloc[i[0]])

    return recommendations

# --------------------------------------------------
# UI STYLING
# --------------------------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #0f0f0f;
        color: white;
    }
    .movie-card {
        background-color: #1c1c1c;
        padding: 10px;
        border-radius: 12px;
        transition: transform 0.3s;
    }
    .movie-card:hover {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# APP UI
# --------------------------------------------------
st.title("🎬 Movie Recommendation System")
st.caption("Netflix-style recommendations with rich details")

selected_movie = st.selectbox("Choose a movie", movies["title"].values)

if st.button("🚀 Recommend Movies"):
    recommendations = recommend(selected_movie, n=5)

    st.subheader("🔥 Recommended for you")

    cols = st.columns(5)

    for col, movie in zip(cols, recommendations):
        poster, genres, director, cast, watch_link = fetch_movie_details(
            movie.movie_id
        )

        with col:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)

            if poster:
                st.image(poster, use_container_width=True)

            st.markdown(f"**{movie.title}**")
            st.caption(f"🎭 {genres}")
            st.caption(f"🎬 Director: {director}")
            st.caption(f"👥 Cast: {cast}")

            if watch_link:
                st.markdown(f"[▶ Watch here]({watch_link})")

            st.markdown("</div>", unsafe_allow_html=True)
