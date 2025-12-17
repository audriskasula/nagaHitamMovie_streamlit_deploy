import streamlit as st
import requests
from db import add_watchlist, get_watchlist
from login import login_page
from darkmode import apply_theme
from datetime import datetime

st.set_page_config(page_title="Naga Hitam Movies", layout="wide")
st.markdown("""
    <style>
        .movie-poster {
            width: 100%;
            height: 320px; 
            object-fit: cover;   
            border-radius: 12px; 
        }
        .movie-title {
            font-weight: 600;
            font-size: 15px;
        }
    </style>
""", unsafe_allow_html=True)

API_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTgyZTVhYWZmNjI3NWRiODMxYmRhMGY1NGI3ZjQ5OSIsIm5iZiI6MTY4NzI0NTMyOS4zMjcwMDAxLCJzdWIiOiI2NDkxNTIxMTU1OWQyMjAxMWM0ZGY3OGMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.CAGZDH8VwFdHJ1IJ-O0Y8-jFcr-n_EWxuFOtS6M-sfU"


# LOGIN
if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
    login_page()
    st.stop()

user = st.session_state["user"]

# Sync saved IDs dari DB
watchlist_items = get_watchlist(user['id'])
st.session_state["saved_ids"] = {item[1] for item in watchlist_items}



# SIDEBAR
st.sidebar.success(f"Login sebagai: {user['username']}")
if st.sidebar.button("Logout"):
    st.session_state["user"] = None
    st.rerun()

# HIDE DETAILS PAGE FROM SIDEBAR
st.markdown("""
<style>
[data-testid="stSidebarNav"] ul li:nth-child(3) {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# Darkmode
apply_theme()


def push_history(movie_id, title, poster_url):
    if "history_stack" not in st.session_state:
        st.session_state["history_stack"] = []

    # hapus jika sudah ada (biar tidak double)
    st.session_state["history_stack"] = [
        m for m in st.session_state["history_stack"]
        if m["movie_id"] != movie_id
    ]

    # push ke atas
    st.session_state["history_stack"].append({
        "movie_id": movie_id,
        "title": title,
        "poster": poster_url,
        "timestamp": datetime.now().strftime("%d %b %Y • %H:%M:%S")
    })


def fetch_movies(url):
    headers = {
        "accept": "application/json",
        "Authorization": API_TOKEN
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        st.error("Failed to Retrieve Movie Data 😢")
        return []
    return resp.json().get("results", [])


# SEARCH
st.title(f"Hi, {user['username']}!")

# st.subheader("🔎 Cari Film")
query = st.text_input("Enter Your Film:")

def search_movies(query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "query": query,
        "language": "en-US",
        "include_adult": False
    }
    headers = {
        "accept": "application/json",
        "Authorization": API_TOKEN
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return []
    return response.json().get("results", [])

if query.strip():
    results = search_movies(query.strip())
    if results:
        st.write("### Hasil Pencarian")
        cols = st.columns(6)

        for idx, movie in enumerate(results):
            with cols[idx % 6]:
                poster = movie.get("poster_path")
                poster_url = f"https://image.tmdb.org/t/p/w500{poster}" if poster else "apps/empty.png"
                title = movie.get("title", "Untitled")
                movie_id = movie.get("id")

                st.markdown(f"<img src='{poster_url}' class='movie-poster'/>", unsafe_allow_html=True)
                st.markdown(f"**{title[:20]}{'...' if len(title) > 20 else ''}**")
                st.caption(f"⭐ {movie.get('vote_average', 0)} | 🗓️ {movie.get('release_date', 'N/A')}")

                if movie_id in st.session_state["saved_ids"]:
                    st.markdown("✅ Saved")
                else:
                    if st.button("⭐ Save", key=f"search_save_{movie_id}"):
                        add_watchlist(user['id'], movie_id, title, poster_url)
                        st.session_state["saved_ids"].add(movie_id)
                        st.toast("Added to Watchlist!")
                        st.rerun()

                if st.button("Detail", key=f"search_detail_{movie_id}"):
                    push_history(movie_id, title, poster_url)
                    st.session_state.selected_movie = movie_id
                    st.switch_page("pages/details.py")

        st.markdown("---")
    else:
        st.warning("Movie Not Found")

# FETCH MOVIE
def render_movie_list(movies, prefix):
    cols = st.columns(5)

    for i, movie in enumerate(movies[:15]):
        with cols[i % 5]:
            poster = movie.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster}" if poster else "empty.png"

            title = movie.get("title", "Untitled")
            movie_id = movie.get("id")

            st.markdown(f"<img src='{poster_url}' class='movie-poster'/>", unsafe_allow_html=True)
            st.markdown(f"**{title[:20]}{'...' if len(title) > 20 else ''}**")
            st.caption(f"⭐ {movie.get('vote_average', 0)} | 🗓️ {movie.get('release_date', 'N/A')}")

            if movie_id in st.session_state["saved_ids"]:
                st.markdown("✅ Saved")
            else:
                if st.button("⭐ Save", key=f"{prefix}_save_{movie_id}"):
                    add_watchlist(user['id'], movie_id, title, poster_url)
                    st.session_state["saved_ids"].add(movie_id)
                    st.toast("Added to Watchlist!")
                    st.rerun()

            if st.button("Detail", key=f"{prefix}_detail_{movie_id}"):
                push_history(movie_id, title, poster_url)
                st.session_state.selected_movie = movie_id
                st.switch_page("pages/details.py")


tab1, tab2, tab3, tab4 = st.tabs([
    "Now Playing",
    "Popular",
    "Top Rated",
    "Upcoming"
])

API_NOWPLAYING = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
API_POPULAR = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
API_TOPRATED = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
API_UPCOMING = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"


with tab1:
    st.header("Now Playing")
    render_movie_list(fetch_movies(API_NOWPLAYING), "now")

with tab2:
    st.header("Popular")
    render_movie_list(fetch_movies(API_POPULAR), "popular")

with tab3:
    st.header("Top Rated")
    render_movie_list(fetch_movies(API_TOPRATED), "toprated")

with tab4:
    st.header("Upcoming")
    render_movie_list(fetch_movies(API_UPCOMING), "upcoming")
