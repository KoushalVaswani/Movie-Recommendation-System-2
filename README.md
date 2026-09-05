# 🎬 Movie Recommendation System

A content-based movie recommender with a FastAPI backend and Streamlit frontend, enriched with live data from the OMDb API.

## Architecture

Streamlit (frontend) → FastAPI (backend) → OMDb API (enrichment)
                              ↓
                    Precomputed similarity model
                    (TF-IDF + Cosine Similarity)

The recommendation logic runs entirely inside a FastAPI service, decoupled from the UI. Streamlit only calls the API and renders the response — it has no direct access to the model.

## Features

- Content-based filtering using genres, keywords, cast, and director metadata
- TF-IDF vectorization + cosine similarity for finding similar movies
- Live poster, plot, and rating enrichment via OMDb API
- REST API with interactive docs (`/docs`) built on FastAPI

## Tech Stack

- **Backend:** FastAPI, scikit-learn, pandas
- **Frontend:** Streamlit
- **External API:** OMDb
- **Dataset:** TMDB 5000 Movies Dataset

## Project Structure

    movie-recommender/
    ├── api/
    │   ├── main.py
    │   └── data/
    │       ├── movies.pkl
    │       └── similarity.pkl
    ├── streamlit_app/
    │   └── app.py
    ├── build_model.py
    ├── .env (not committed)
    ├── .gitignore
    └── requirements.txt

## Running Locally

1. Clone the repo and create a virtual environment

       python -m venv venv
       venv\Scripts\activate

2. Install dependencies

       pip install -r requirements.txt

3. Add your OMDb API key to a `.env` file in the root

       OMDB_API_KEY=your_key_here

4. Start the backend

       cd api
       uvicorn main:app --reload

5. In a separate terminal, start the frontend

       cd streamlit_app
       streamlit run app.py

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Health check |
| `GET /movies` | List all available movie titles |
| `GET /recommend/{movie_title}` | Get top-N similar movies with enriched details |

## Known Limitations

- Dataset is limited to ~4,800 movies (TMDB 5000), so recommendations for less mainstream titles can be weaker
- Genre-based similarity can sometimes overweight broad genre overlap; keyword and director signals are more discriminative but limited by dataset size

## Author

**Koushal Vaswani**
[LinkedIn](https://www.linkedin.com/in/koushal-vaswani-56dg65/) · [GitHub](https://github.com/KoushalVaswani)"# Movie-Recommendation-System-2" 
