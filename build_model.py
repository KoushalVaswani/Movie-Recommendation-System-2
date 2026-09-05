import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse

# --- Load and merge ---
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title')

movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)


def parse_names(text):
    return [item['name'] for item in ast.literal_eval(text)]

def parse_top_cast(text, top_n=3):
    cast = ast.literal_eval(text)
    return [item['name'] for item in cast[:top_n]]

def get_director(text):
    crew = ast.literal_eval(text)
    for item in crew:
        if item['job'] == 'Director':
            return [item['name']]
    return []


movies['genres'] = movies['genres'].apply(parse_names)
movies['keywords'] = movies['keywords'].apply(parse_names)
movies['cast'] = movies['cast'].apply(parse_top_cast)
movies['crew'] = movies['crew'].apply(get_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())


def collapse_spaces(items):
    return [i.replace(" ", "") for i in items]

movies['genres'] = movies['genres'].apply(collapse_spaces)
movies['keywords'] = movies['keywords'].apply(collapse_spaces)
movies['cast'] = movies['cast'].apply(collapse_spaces)
movies['crew'] = movies['crew'].apply(collapse_spaces)


# --- Weighted tags ---
movies['tags'] = (
    movies['genres'] * 1 +
    movies['keywords'] * 3 +
    movies['cast'] * 2 +
    movies['crew'] * 5 +
    movies['overview']
)

movies['tags'] = movies['tags'].apply(lambda x: " ".join(x).lower())

new_df = movies[['movie_id', 'title', 'tags']].reset_index(drop=True)


# --- TF-IDF vectors (kept sparse — NOT converted to a dense similarity matrix) ---
tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = tfidf.fit_transform(new_df['tags'])

# --- Save ---
sparse.save_npz('tfidf_vectors.npz', vectors)
pickle.dump(new_df, open('movies.pkl', 'wb'))

print("Done. movies shape:", new_df.shape, "| vectors shape:", vectors.shape)