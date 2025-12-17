import streamlit as st
from login import login_page

st.set_page_config(page_title="History", layout="wide")

if "user" not in st.session_state or st.session_state["user"] is None:
    login_page()
    st.stop()

st.title("📜 History (Stack - LIFO)")

if "history_stack" not in st.session_state:
    st.session_state["history_stack"] = []

stack = st.session_state["history_stack"]

if st.button("Delete/Pop (First Out)"):
    if stack:
        stack.pop()
        st.toast("History terakhir dihapus (LIFO)")
        st.rerun()

if not stack:
    st.info("Belum ada history.")
    st.stop()

for item in reversed(stack):
    st.markdown("---")

    col_img, col_info = st.columns([1, 5])

    with col_img:
        st.image(item.get("poster", "apps/empty.png"), width=120)

    with col_info:
        st.markdown(f"### {item.get('title', 'Untitled')}")
        st.caption(item.get("timestamp", "Waktu tidak tersedia"))

        if st.button("Detail", key=f"detail_{item['movie_id']}"):
            st.session_state.selected_movie = item["movie_id"]
            st.switch_page("pages/details.py")
