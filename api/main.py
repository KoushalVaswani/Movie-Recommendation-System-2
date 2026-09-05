from fastapi import FastAPI, HTTPException
import pickle
import os
import requests
from dotenv import load_dotenv
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

app = FastAPI(title="Movie Recommender API")

movies = pickle.load(open("data/movies.pkl", "rb"))
vectors = sparse.load_npz("data/tfidf_vectors.npz")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")


def get_movie_details(title: str):
    url = "http://www.omdbapi.com/"
    params = {"apikey": OMDB_API_KEY, "t": title}
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("Response") == "True":
        return {
            "poster": data.get("Poster"),
            "plot": data.get("Plot"),
            "rating": data.get("imdbRating"),
            "year": data.get("Year")
        }
    else:
        return {
            "poster": None,
            "plot": "Details not found",
            "rating": None,
            "year": None
        }


@app.get("/")
def home():
    return {"message": "Movie Recommender API is running"}


@app.get("/movies")
def get_all_movies():
    return {"movies": movies['title'].tolist()}


@app.get("/recommend/{movie_title}")
def recommend(movie_title: str, num_recommendations: int = 5):
    if movie_title not in movies['title'].values:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_title}' not found")

    movie_index = movies[movies['title'] == movie_title].index[0]

    # Compute similarity on demand instead of loading a precomputed matrix
    distances = cosine_similarity(vectors[movie_index], vectors).flatten()

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:num_recommendations + 1]

    max_score = movies_list[0][1] if movies_list else 1
    results = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        score = round((i[1] / max_score) * 100, 2)
        details = get_movie_details(title)

        results.append({
            "title": title,
            "match_score": score,
            "poster": details["poster"],
            "plot": details["plot"],
            "rating": details["rating"],
            "year": details["year"]
        })

    return {
        "movie": movie_title,
        "recommendations": results
    }