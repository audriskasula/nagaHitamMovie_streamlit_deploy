import streamlit as st 
from db import get_watchlist, delete_watchlist
from login import login_page
from recommend_ai import ai_recommend_movies
from tmdb_fetch import get_poster_from_tmdb
from darkmode import apply_theme

if st.session_state.get("user") is None:
    login_page()
    st.stop()

user = st.session_state["user"]

# SIDEBAR
if st.sidebar.button("Logout"):
    st.session_state["user"] = None
    st.rerun()

if "error_msg" in st.session_state:
    st.error(st.session_state["error_msg"])
    del st.session_state["error_msg"]

# HIDE DETAILS PAGE FROM SIDEBAR
st.markdown("""
<style>
[data-testid="stSidebarNav"] ul li:nth-child(3) {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# DarkMode
apply_theme()

st.header("⭐ Your Watchlist")

# GET WATCHLIST
watchlist = get_watchlist(user["id"])
# HINT Struktur:
# item[0] = id_watchlist
# item[1] = movie_id
# item[2] = movie_title
# item[3] = poster_url

if not watchlist:
    st.info("There are no movies in your watchlist yet 😢")
else:
    cols = st.columns(5)

    for index, item in enumerate(watchlist):
        id_watchlist = item[0]
        movie_id = item[1]
        title = item[2]
        poster = item[3]

        with cols[index % 5]:
            st.image(poster, use_container_width=True)
            st.markdown(f"*{title}*")

            if st.button("❌ Remove", key=f"del_{id_watchlist}"):
                delete_watchlist(id_watchlist)

                # Hapus dari saved_ids session_state supaya tombol save sinkron
                if movie_id in st.session_state.get("saved_ids", set()):
                    st.session_state["saved_ids"].remove(movie_id)

                st.session_state["error_msg"] = "Removed from Watchlist!"
                st.rerun()


st.write("---")
if not watchlist:
    st.stop()

prev_watchlist = st.session_state.get("prev_watchlist", None)

if prev_watchlist != watchlist:
    st.session_state.pop("ai_rekomendasi", None)

st.session_state.prev_watchlist = watchlist

if "ai_rekomendasi" not in st.session_state:
    watchlist_titles = [item[2] for item in watchlist]
    rekomendasi_strings = ai_recommend_movies(watchlist_titles)

    import re
    clean_titles = []
    for s in rekomendasi_strings:
        s = re.sub(r"^[\*\-\d\.\) ]+", "", s).strip()
        s = s.replace('"', "").replace("'", "")
        if s:
            clean_titles.append(s)

    # Cari poster TMDB dari judul
    rekomendasi = []
    for title in clean_titles:
        rekomendasi.append((title, get_poster_from_tmdb(title)))

    # SIMPAN DI SESSION 
    st.session_state.ai_rekomendasi = rekomendasi

# Get dari session
rekomendasi = st.session_state.ai_rekomendasi

st.write("## 🎥 Rekomendasi Film:")

if rekomendasi:
    cols = st.columns(5)

    for i, (title, poster_url) in enumerate(rekomendasi):
        with cols[i % 5]:
            st.image(poster_url, use_container_width=True)
            st.markdown(f"*{title}*")

            # BUTTON DETAIL
            if st.button("Detail", key=f"ai_detail_{i}"):
                from tmdb_fetch import get_movie_id_from_title
                movie_id = get_movie_id_from_title(title)

                if movie_id:
                    st.session_state.selected_movie = movie_id
                    st.switch_page("pages/details.py")
                else:
                    st.error("Gagal menemukan ID film.")