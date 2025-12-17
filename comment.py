import streamlit as st
from comments_db import add_comment, get_comments

def comment_section(movie_id, username):
    st.markdown("## 💬 Comments")

    comments = get_comments(movie_id)

    if len(comments) == 0:
        st.info("Belum ada komentar untuk film ini.")
    else:
        for (user, text, time) in comments:
            st.markdown(f"**{user}** — *{time}*")
            st.write(text)
            st.markdown("---")

    st.write("### Tambahkan Komentar")
    comment = st.text_area("Tulis komentar...")

    if st.button("Kirim Komentar"):
        if comment.strip():
            add_comment(movie_id, username, comment.strip())
            st.success("Komentar berhasil dikirim!")
            st.rerun()
        else:
            st.warning("Komentar tidak boleh kosong!")
