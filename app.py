import streamlit as st
import pickle
import requests
from difflib import get_close_matches
from concurrent.futures import ThreadPoolExecutor
import time
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Cineflix Recommender",
    page_icon="🎬",
    layout="wide"
)

# ================= SESSION STATES =================
if "show_splash" not in st.session_state:
    st.session_state.show_splash = True

if "visible_count" not in st.session_state:
    st.session_state.visible_count = 5

# ================= SPLASH SCREEN =================
if st.session_state.show_splash:
    st.markdown("""
    <style>
    .splash {
        display:flex;
        justify-content:center;
        align-items:center;
        height:90vh;
        background:black;
        flex-direction:column;
        animation: fadeIn 1s ease-in-out;
    }
    .splash-logo {
        font-size:72px;
        font-weight:900;
        color:#E50914;
        letter-spacing:4px;
        animation: zoomIn 1.2s ease-in-out;
    }
    @keyframes zoomIn {
        from {transform: scale(0.5); opacity:0;}
        to {transform: scale(1); opacity:1;}
    }
    </style>

    <div class="splash">
        <div class="splash-logo">🎬 CINEFLIX</div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(2)
    st.session_state.show_splash = False
    st.rerun()

# ================= DOWNLOAD ARTIFACTS =================
def download_from_drive(file_id, filename):
    """Download a file from Google Drive if it doesn't exist locally."""
    import gdown

    # Ensure parent folder exists
    folder = os.path.dirname(filename)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(filename):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, filename, quiet=False)

# Google Drive IDs (replace with your actual file IDs)
movies_file_id = "1iSCzQTDOzZIi0Q3ZCc2YAgzdau-bcQcn"
similarity_file_id = "1IH11t_gVc8i1WELFp3ZuqJcFaYjz34Rj"

# Download artifacts
download_from_drive(movies_file_id, "artifacts/movies.pkl")
download_from_drive(similarity_file_id, "artifacts/similarity.pkl")

# ================= LOAD FILES =================
movies = pickle.load(open('artifacts/movies.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

API_KEY = "1506589622ad1e20c44c36f4ae8d32ae"
session = requests.Session()

# ================= CINEFLIX CSS =================
st.markdown("""
<style>
header[data-testid="stHeader"] {background-color: black !important;}
.block-container {padding-top: 1rem; max-width: 100%; padding-left: 2rem; padding-right: 2rem;}
.stApp {background: radial-gradient(circle at 50% -10%, rgba(229,9,20,0.35), transparent 40%), linear-gradient(to bottom, #0b0b0f 0%, #000000 60%); color: white;}
.navbar {display:flex; justify-content:space-between; align-items:center; padding: 12px 40px; background: rgba(0,0,0,0.6); backdrop-filter: blur(8px);}
.logo {font-size:28px; font-weight:bold; color:#E50914;}
.hero {text-align:center; padding-top: 40px; padding-bottom: 10px;}
.hero-title {font-size:56px; font-weight:800;}
.hero-sub {color:#b3b3b3; font-size:18px; margin-top:10px; margin-bottom:30px;}
.stSelectbox div[data-baseweb="select"] {background: rgba(255,255,255,0.97) !important; color: black !important; border-radius: 12px !important; font-weight: 600 !important;}
.stButton > button {background: rgba(255,255,255,0.9); color: black; border-radius: 10px; font-weight: 600;}
.card {background: rgba(255,255,255,0.05); backdrop-filter: blur(6px); border-radius:16px; padding:12px; text-align:center; margin-bottom:12px; transition: all 0.25s ease; border: 1px solid rgba(255,255,255,0.08);}
.card:hover {transform: scale(1.05);}
.scroll-container {display:flex; overflow-x:auto; gap:18px; padding-bottom:10px;}
.scroll-container::-webkit-scrollbar {height:8px;}
.scroll-container::-webkit-scrollbar-thumb {background:#E50914; border-radius:10px;}
</style>
""", unsafe_allow_html=True)

# ================= NAVBAR =================
st.markdown('<div class="navbar"><div class="logo">🎬 CINEFLIX</div></div>', unsafe_allow_html=True)

# ================= HERO =================
st.markdown("""
<div class="hero">
    <div class="hero-title">FIND YOUR NEXT MOVIE</div>
    <div class="hero-sub">Search for any movie and discover personalized recommendations</div>
</div>
""", unsafe_allow_html=True)

# ================= FETCH FUNCTIONS =================
@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        data = session.get(url, timeout=4).json()

        poster_path = data.get("poster_path")
        backdrop_path = data.get("backdrop_path")
        rating = data.get("vote_average", "N/A")
        overview = data.get("overview", "")

        poster_url = "https://image.tmdb.org/t/p/w500" + poster_path if poster_path else None
        backdrop_url = "https://image.tmdb.org/t/p/original" + backdrop_path if backdrop_path else None

        return poster_url, rating, backdrop_url, overview
    except:
        return None, "N/A", None, ""

@st.cache_data(show_spinner=False)
def fetch_trailer(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
        data = session.get(url, timeout=4).json()
        for v in data.get("results", []):
            if v["type"] == "Trailer" and v["site"] == "YouTube":
                return f"https://www.youtube.com/watch?v={v['key']}"
        return "https://www.youtube.com"
    except:
        return "https://www.youtube.com"

# ================= FAST TRENDING =================
@st.cache_data(show_spinner=False)
def get_trending_fast():
    trending = []
    idx = 0
    while len(trending) < 5 and idx < len(movies):
        movie = movies.iloc[idx]
        poster, rating, _, _ = fetch_movie_details(movie.movie_id)
        if poster:
            trailer = fetch_trailer(movie.movie_id)
            watch_link = f"https://www.google.com/search?q={movie.title}+watch+online"
            trending.append((movie.title, poster, rating, trailer, watch_link))
        idx += 1
    return trending

# ================= RECOMMEND FUNCTION =================
def recommend(movie):
    if movie not in movies['title'].values:
        closest = get_close_matches(movie, movies['title'].values, n=1, cutoff=0.6)
        if closest:
            movie = closest[0]
        else:
            return [], [], [], [], []

    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:30]

    names, posters, ratings, trailers, watch_links = [], [], [], [], []

    def fetch_all(i):
        movie_id = movies.iloc[i[0]].movie_id
        poster, rating, _, _ = fetch_movie_details(movie_id)
        trailer = fetch_trailer(movie_id)
        watch_link = f"https://www.google.com/search?q={movies.iloc[i[0]].title}+watch+online"
        return i, poster, rating, trailer, watch_link

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_all, movie_list)

    for result in results:
        i, poster, rating, trailer, watch_link = result
        if poster:
            names.append(movies.iloc[i[0]].title)
            posters.append(poster)
            ratings.append(rating)
            trailers.append(trailer)
            watch_links.append(watch_link)
        if len(names) >= 10:
            break

    return names, posters, ratings, trailers, watch_links

# ================= SEARCH =================
movie_list = ["Type here to search..."] + movies['title'].tolist()

selected_movie = st.selectbox("🔍 Movie Search", movie_list)

if selected_movie == "Type here to search...":
    selected_movie = ""

# ================= MAIN DISPLAY =================
if not selected_movie:
    st.subheader("🔥 Trending Movies")
    trending_movies = get_trending_fast()
    cols = st.columns(5)
    for i, movie in enumerate(trending_movies):
        title, poster, rating, trailer, watch_link = movie
        with cols[i]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.image(poster, use_container_width=True)
            st.caption(title)
            st.write(f"⭐ {rating}")
            st.link_button("▶ Watch Trailer", trailer)
            st.link_button("🍿 Where to Watch", watch_link)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    idx = movies[movies['title'] == selected_movie].index[0]
    movie_id = movies.iloc[idx].movie_id

    poster, rating, backdrop, overview = fetch_movie_details(movie_id)
    trailer = fetch_trailer(movie_id)
    watch_link = f"https://www.google.com/search?q={selected_movie}+watch+online"

    # ===== HERO BANNER =====
    st.markdown(f"""
    <style>
    .hero-banner {{
        position: relative;
        height: 420px;
        border-radius: 18px;
        overflow: hidden;
        margin-bottom: 25px;
        background-image: linear-gradient(to right, rgba(0,0,0,0.85), rgba(0,0,0,0.2)), url('{backdrop}');
        background-size: cover;
        background-position: center;
        display:flex;
        align-items:center;
        padding:40px;
    }}
    .hero-content {{max-width: 520px;}}
    .hero-movie-title {{font-size:48px; font-weight:900; margin-bottom:10px;}}
    .hero-overview {{color:#d1d1d1; font-size:15px; line-height:1.5;}}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-content">
            <div class="hero-movie-title">{selected_movie}</div>
            <div style="margin-bottom:10px;">⭐ {rating}</div>
            <div class="hero-overview">{overview[:220]}...</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.link_button("▶ Watch Trailer", trailer)
    with col2:
        st.link_button("🍿 Where to Watch", watch_link)

    # ================= SIMILAR MOVIES =================
    st.subheader("✨ Similar Movies")
    names, posters, ratings, trailers, watch_links = recommend(selected_movie)

    visible = min(st.session_state.visible_count, len(names))

    st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
    cols = st.columns(visible)
    for i in range(visible):
        with cols[i]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.image(posters[i], use_container_width=True)
            st.caption(names[i])
            st.write(f"⭐ {ratings[i]}")
            st.link_button("▶ Watch Trailer", trailers[i])
            st.link_button("🍿 Where to Watch", watch_links[i])
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if visible < len(names):
        if st.button("🔽 Load More"):
            st.session_state.visible_count += 5
            st.rerun()