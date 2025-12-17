import google.generativeai as genai

genai.configure(api_key="AIzaSyDvi_Yd3YOuocMeGInsyylRdcMwAYvJouk")

model = genai.GenerativeModel("models/gemini-2.5-flash")

def ai_recommend_movies(watchlist):

    prompt = f"""
    Pengguna memiliki watchlist film berikut: {watchlist}.
    Berikan 5 film lain yang mirip dari gaya, genre, atau vibes-nya. Balas hanya dengan format list. TANPA PENULISAN APAPUN< HANYA BERIKAN JUDUL FILM NYA SAJA DALAM LIST.
    """

    response = model.generate_content(prompt)

    hasil = response.text.split("\n")
    hasil = [h.replace("-", "").strip() for h in hasil if h.strip()]

    return hasil[:5]
