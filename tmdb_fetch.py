import requests

TMDB_ACCESS_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTgyZTVhYWZmNjI3NWRiODMxYmRhMGY1NGI3ZjQ5OSIsIm5iZiI6MTY4NzI0NTMyOS4zMjcwMDAxLCJzdWIiOiI2NDkxNTIxMTU1OWQyMjAxMWM0ZGY3OGMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.CAGZDH8VwFdHJ1IJ-O0Y8-jFcr-n_EWxuFOtS6M-sfU"

def get_poster_from_tmdb(title):
    print(title)
    print("FUNCTION LOADED")

    url = "https://api.themoviedb.org/3/search/movie"
    
    headers = {
        "Authorization": f"{TMDB_ACCESS_TOKEN}",
        "Content-Type": "application/json;charset=utf-8"
    }

    params = {
        "query": title,
        "include_adult": "false",
        "language": "en-US",
        "page": 1
    }

    r = requests.get(url, headers=headers, params=params)
    data = r.json()

    results = data.get("results", [])
    if not results:
        print("NO RESULTS", data)
        return "apps/empty.png"

    poster_path = results[0].get("poster_path")
    if not poster_path:
        return "apps/empty.png"

    return f"https://image.tmdb.org/t/p/w500{poster_path}"

def get_movie_id_from_title(title):
    url = "https://api.themoviedb.org/3/search/movie"
    headers = {
        "Authorization": TMDB_ACCESS_TOKEN,
        "Content-Type": "application/json;charset=utf-8"
    }
    params = {"query": title, "language": "en-US"}

    r = requests.get(url, headers=headers, params=params)
    data = r.json()

    results = data.get("results", [])
    if not results:
        return None

    return results[0].get("id")
