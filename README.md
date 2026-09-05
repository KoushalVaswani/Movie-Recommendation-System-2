# 🎬 CineMatch — Movie Recommendation System

A content-based movie recommendation engine with a decoupled architecture: a **FastAPI** backend serving the ML model, a **Streamlit** frontend for the UI, and live enrichment via the **OMDb API**.

🔗 **Live Demo:** [movie-recommendation-system-2-kv96.streamlit.app](https://movie-recommendation-system-2-kv96.streamlit.app)
🔗 **API Docs:** [movie-recommendation-system-2-2.onrender.com/docs](https://movie-recommendation-system-2-2.onrender.com/docs)

> Note: The backend is hosted on Render's free tier, which spins down after inactivity. The first request after idle time may take 20–30 seconds to wake up.

---

## 🧠 How It Works

1. Movies are represented as "tags" combining genres, keywords, cast, and director
2. **TF-IDF vectorization** converts these tags into numerical vectors
3. **Cosine similarity** finds the closest movies in that vector space
4. The FastAPI backend serves these recommendations as JSON
5. Each result is enriched in real time with posters, plot, and ratings from OMDb
6. Streamlit renders everything as an interactive UI — but never touches the model directly

```
┌─────────────┐        HTTP        ┌─────────────┐        HTTP        ┌─────────────┐
│  Streamlit  │ ─────────────────▶ │   FastAPI   │ ─────────────────▶ │    OMDb     │
│  (Frontend) │ ◀───────────────── │  (Backend)  │ ◀───────────────── │    (API)    │
└─────────────┘                    └─────────────┘                    └─────────────┘
                                          │
                                          ▼
                               TF-IDF + Cosine Similarity
                                (computed on demand)
```

---

## ✨ Features

- 🎯 Content-based recommendations using genre, keyword, cast, and director similarity
- ⚡ Fully decoupled REST API — model logic is independent of the UI
- 🖼️ Live poster, plot, and IMDb rating enrichment via OMDb
- 📖 Auto-generated interactive API docs (Swagger UI at `/docs`)
- 🎨 Responsive card-based UI with match-score visualization
- ☁️ Fully deployed — backend on Render, frontend on Streamlit Community Cloud

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Uvicorn |
| ML / Data | scikit-learn (TF-IDF, Cosine Similarity), pandas, scipy |
| Frontend | Streamlit |
| External API | OMDb |
| Dataset | TMDB 5000 Movies Dataset |
| Deployment | Render (backend), Streamlit Community Cloud (frontend) |

---

## 📁 Project Structure

```
movie-recommender/
├── api/
│   ├── main.py                 # FastAPI app & endpoints
│   ├── requirements.txt
│   └── data/
│       ├── movies.pkl          # Preprocessed movie metadata
│       └── tfidf_vectors.npz   # Sparse TF-IDF vectors
├── streamlit_app/
│   ├── app.py                  # Streamlit UI, calls the API
│   └── requirements.txt
├── build_model.py              # Model training / preprocessing script
├── .env                        # API keys (not committed)
├── .gitignore
└── README.md
```

---

## 🚀 Running Locally

**1. Clone and set up a virtual environment**
```bash
git clone https://github.com/KoushalVaswani/Movie-Recommendation-System-2.git
cd Movie-Recommendation-System-2
python -m venv venv
venv\Scripts\activate
```

**2. Install dependencies**
```bash
pip install -r api/requirements.txt
pip install -r streamlit_app/requirements.txt
```

**3. Add your OMDb API key**

Create a `.env` file in the root:
```
OMDB_API_KEY=your_key_here
```
Get a free key at [omdbapi.com](https://www.omdbapi.com/apikey.aspx)

**4. Start the backend**
```bash
cd api
uvicorn main:app --reload
```

**5. Start the frontend** (in a separate terminal)
```bash
cd streamlit_app
streamlit run app.py
```

> To run against the local backend instead of the deployed one, update `API_URL` in `streamlit_app/app.py` to `http://127.0.0.1:8000`

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/movies` | List all available movie titles |
| `GET` | `/recommend/{movie_title}` | Get top-N similar movies with enriched details |

**Example request:**
```
GET /recommend/Inception?num_recommendations=5
```

**Example response:**
```json
{
  "movie": "Inception",
  "recommendations": [
    {
      "title": "The Prestige",
      "match_score": 82.4,
      "poster": "https://...",
      "plot": "...",
      "rating": "8.5",
      "year": "2006"
    }
  ]
}
```

---

## ⚠️ Known Limitations

- Dataset is limited to ~4,800 movies (TMDB 5000), so recommendations for niche or newer titles may be weaker
- Genre-based similarity can overweight broad genre overlap between unrelated movies; keyword and director signals are more discriminative but constrained by dataset size
- No user-personalization yet — recommendations are purely content-based, not collaborative
- Render's free tier causes a cold-start delay after inactivity

---

## 🔮 Future Improvements

- Hybrid recommendations combining content-based + collaborative filtering
- Larger, more current movie dataset
- User accounts with rating history
- CI/CD pipeline via GitHub Actions for automated deployment

---

## 👨‍💻 Author

**Koushal Vaswani**
Machine Learning Student

[LinkedIn](https://www.linkedin.com/in/koushal-vaswani-56dg65/) · [GitHub](https://github.com/KoushalVaswani)