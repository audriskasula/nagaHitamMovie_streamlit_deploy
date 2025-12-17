import streamlit as st
from login import login_page

st.set_page_config(page_title="History", layout="wide")

# LOGIN CHECK
if "user" not in st.session_state or st.session_state["user"] is None:
    login_page()
    st.stop()

st.title("📜 History")

# HAPUS SEMUA
if st.button("🗑️ Hapus Semua History"):
    st.session_state["history_stack"] = []
    st.toast("History berhasil dihapus")
    st.rerun()

history = st.session_state.get("history_stack", [])

if not history:
    st.info("Belum ada history.")
    st.stop()

# ===== TAMPIL PER BARIS =====
for idx, item in enumerate(reversed(history)):
    real_index = len(history) - 1 - idx

    st.markdown("---")

    col_img, col_info = st.columns([1, 5])

    with col_img:
        st.image(
            item.get("poster", "apps/empty.png"),
            width=120
        )

    with col_info:
        st.markdown(f"### {item.get('title', 'Untitled')}")

        # FIX timestamp (tidak jadi titik)
        st.caption(item.get("timestamp") or "Waktu tidak tersedia")


        if st.button("Detail", key=f"history_detail_{real_index}"):
            st.session_state.selected_movie = item["movie_id"]
            st.switch_page("pages/details.py")

        if st.button("❌ Hapus", key=f"history_delete_{real_index}"):
            st.session_state["history_stack"].pop(real_index)
            st.toast("History dihapus")
            st.rerun()
