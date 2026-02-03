import streamlit as st
import pickle
import requests

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide"
)

# =========================================================
# PREMIUM DARK UI (SAFE)
# =========================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0b0f19;
    color: #ffffff;
    font-family: "Segoe UI", system-ui, sans-serif;
}

.block-container {
    padding-top: 2.5rem;
}

#MainMenu, footer, header {visibility: hidden;}

.main-title {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 40px;
}

.stButton > button {
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    color: white;
    border-radius: 14px;
    height: 3.2em;
    font-size: 18px;
    font-weight: 700;
}

.movie-card {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 12px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
    transition: transform 0.25s ease;
}

.movie-card:hover {
    transform: translateY(-6px);
}

.movie-title {
    text-align: center;
    margin-top: 10px;
    font-weight: 600;
}

img {
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# =========================================================
# TMDB CONFIG
# =========================================================
API_KEY = st.secrets["a7d76988410a01cac355ee5334451679"]


def fetch_movie_details(movie_id):
    """
    Returns:
    poster_url, genres, director, top_cast
    """
    try:
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"

        movie_data = requests.get(movie_url, timeout=5).json()
        credits_data = requests.get(credits_url, timeout=5).json()

        poster_path = movie_data.get("poster_path")
        if not poster_path:
            return None, None, None, None

        poster_url = "https://image.tmdb.org/t/p/w500" + poster_path
        genres = ", ".join([g["name"] for g in movie_data.get("genres", [])])

        director = "Unknown"
        for crew in credits_data.get("crew", []):
            if crew.get("job") == "Director":
                director = crew.get("name")
                break

        cast = ", ".join([c["name"] for c in credits_data.get("cast", [])[:3]])

        if not genres or not cast:
            return None, None, None, None

        return poster_url, genres, director, cast

    except:
        return None, None, None, None


def watch_link(title):
    return "https://www.google.com/search?q=" + f"Watch {title} movie online".replace(" ", "+")

# =========================================================
# RECOMMENDER (ALWAYS RETURNS 5)
# =========================================================
def recommend(movie, n=5):
    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    results = []
    checked = 0
    MAX_CHECKS = 60  # safety guard

    for i, _ in distances[1:]:
        if checked >= MAX_CHECKS:
            break

        row = movies.iloc[i]
        checked += 1

        poster, genres, director, cast = fetch_movie_details(row.movie_id)

        if poster:
            results.append({
                "title": row.title,
                "poster": poster,
                "genres": genres,
                "director": director,
                "cast": cast,
                "watch": watch_link(row.title)
            })

        if len(results) == n:
            break

    return results

# =========================================================
# UI
# =========================================================
st.markdown("<div class='main-title'>🎬 Movie Recommendation System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Discover • Explore • Watch</div>", unsafe_allow_html=True)

selected_movie = st.selectbox(
    "🎥 Select a movie you like",
    movies["title"].values
)

if st.button("🚀 Recommend Movies"):
    with st.spinner("Finding the best movies for you..."):
        recommendations = recommend(selected_movie)

    st.subheader("🔥 Recommended for you")

    cols = st.columns(len(recommendations))
    for col, movie in zip(cols, recommendations):
        with col:
            st.markdown("<div class='movie-card'>", unsafe_allow_html=True)

            # Clickable poster
            st.markdown(f"""
            <a href="{movie['watch']}" target="_blank">
                <img src="{movie['poster']}" style="width:100%;">
            </a>
            """, unsafe_allow_html=True)

            st.markdown(f"<div class='movie-title'>{movie['title']}</div>", unsafe_allow_html=True)

            with st.expander("ℹ️ More info"):
                st.write(f"🎬 **Director:** {movie['director']}")
                st.write(f"🎭 **Top Cast:** {movie['cast']}")
                st.write(f"🏷️ **Genres:** {movie['genres']}")
                st.markdown(f"[▶️ **Where to watch**]({movie['watch']})")

            st.markdown("</div>", unsafe_allow_html=True)
