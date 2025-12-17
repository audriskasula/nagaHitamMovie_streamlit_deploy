import streamlit as st
import google.generativeai as genai
from darkmode import apply_theme

st.markdown("""
    <style>
    /* Chat container */
    .chat-container {
        padding: 10px 15px;
        border-radius: 12px;
        margin: 10px 0;
        max-width: 80%;
        word-wrap: break-word;
    }

    /* User bubble */
    .user-msg {
        background-color: #2b2b2b;
        align-self: flex-end;
        border-radius: 50px;
    }

    </style>
""", unsafe_allow_html=True)

# LOGOUT
if st.sidebar.button("Logout"):
    st.session_state["user"] = None
    st.rerun()

# HIDE DETAILS DI SIDEBAR
st.markdown("""
<style>
[data-testid="stSidebarNav"] ul li:nth-child(3) {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# DarkMode
apply_theme()

API_KEY = "AIzaSyDvi_Yd3YOuocMeGInsyylRdcMwAYvJouk"
genai.configure(api_key=API_KEY)

# TITLE
st.title("🤖 Chat AI")
st.write("Tanyakan apa saja ke AI di bawah ini.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# SHOW CHAT HISTORY
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    align = "flex-end" if msg["role"] == "user" else "flex-start"

    st.markdown(
        f"""
        <div style="display: flex; justify-content: {align};">
            <div class="chat-container {role_class}">
                {msg['content']}
        </div>
        """,
        unsafe_allow_html=True
    )

# INPUT USER
has_user_chat = any(m["role"] == "user" for m in st.session_state.messages)

prompt = st.chat_input("Tulis pesan...")

if "pending_message" in st.session_state:
    prompt = st.session_state.pop("pending_message")

if not has_user_chat:
    st.write("### 🔥 Template Chat Cepat")

    templates = [
        "Film action yang menarik dong",
        "Rekomendasi film sedih yang bisa bikin nangis",
        "Film romance tapi endingnya bahagia",
        "Film sci-fi yang mindblowing",
        "Kasih aku film mirip Interstellar",
    ]

    cols = st.columns(3)

    for i, t in enumerate(templates):
        with cols[i % 3]:
            if st.button(t, key=f"tmpl_{i}"):
                st.session_state["pending_message"] = t

if "pending_message" in st.session_state:
    prompt = st.session_state.pop("pending_message")

user_sent_now = prompt is not None

has_user_chat = any(m["role"] == "user" for m in st.session_state.messages)

show_templates = not (user_sent_now or has_user_chat)


if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end;">
            <div class="chat-container user-msg">{prompt}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.spinner("AI sedang mengetik..."):
        model = genai.GenerativeModel(
            "models/gemini-2.5-flash",
            system_instruction="KAMU ADALAH BOT YANG HANYA MENJAWAB SESUATU TENTANG FILM. Apabila user menanyakan sesuatu yang di luar topik film, anda tidak perlu menjawab pertanyaan tersebut, tolak secara halus."
        )

        response = model.generate_content(prompt)

    ai_reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-start;">
            <div class="chat-container ai-msg">{ai_reply}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.rerun()