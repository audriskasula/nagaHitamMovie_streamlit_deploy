import streamlit as st

def apply_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    def switch_theme():
        st.session_state.theme = (
            "light" if st.session_state.theme == "dark" else "dark"
        )

    dark_css = """
    <style>
    html, body, .main{
        background-color: #0e1117 !important;
        color: white !important;
    }
    </style>
    """

    light_css = """
    <style>
    html, body, .stApp, .stAppViewContainer, .main, [data-testid="stAppViewContainer"] * {
        background-color: white !important;
        color: black !important;
    }
    </style>
    """

    st.markdown(
        dark_css if st.session_state.theme == "dark" else light_css,
        unsafe_allow_html=True
    )

    with st.sidebar:
        # st.write("### 🌗 Theme Mode")

        if st.session_state.theme == "dark":
            st.button("☀️ Light", on_click=switch_theme)
        else:
            st.button("🌙 Dark", on_click=switch_theme)
