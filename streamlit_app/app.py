import streamlit as st
import requests

API_URL = "https://movie-recommendation-system-2-2.onrender.com"

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>

div[data-testid="stMetric"]{
    background-color:#1e293b;
    padding:15px;
    border-radius:12px;
}

.stProgress > div > div > div > div {
    border-radius:10px;
}

.stButton > button{
    width:100%;
    height:50px;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
}

/* Fixed-size poster images */
div[data-testid="stImage"] img {
    width: 220px;
    height: 330px;
    object-fit: cover;
    border-radius: 8px;
    display: block;
    margin: 0 auto;
}

/* Equal height cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    height: 100%;
}

</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommendation System")
st.markdown("Get personalized movie recommendations instantly!")


@st.cache_data
def get_movie_list():
    response = requests.get(f"{API_URL}/movies")
    return response.json()["movies"]


def get_recommendations(movie_title, num_recommendations):
    response = requests.get(
        f"{API_URL}/recommend/{movie_title}",
        params={"num_recommendations": num_recommendations}
    )
    if response.status_code == 200:
        return response.json()["recommendations"], None
    else:
        return None, response.json().get("detail", "Something went wrong")


movie_list = get_movie_list()

selected_movie = st.selectbox(
    "Search Movie",
    movie_list
)

num_recommendations = st.number_input(
    "Number of Recommendations",
    min_value=1,
    max_value=20,
    value=5,
    step=1
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Movies", len(movie_list))
col2.metric("Recommendations", num_recommendations)
col3.metric("Algorithm", "Content-Based")
col4.metric("Backend", "FastAPI")

st.sidebar.info("""
### 👨‍💻 Developer

**Koushal Vaswani**

🚀 Machine Learning Student

🧠 Content-Based Filtering

📊 Count Vectorizer

📐 Cosine Similarity

🔌 Served via FastAPI REST API

""")

st.sidebar.link_button(
    "🟦 LinkedIn",
    "https://www.linkedin.com/in/koushal-vaswani-56dg65/"
)

st.sidebar.link_button(
    "🐙 GitHub",
    "https://github.com/KoushalVaswani"
)

if st.button("🎬 Get Recommendations"):

    with st.spinner("Finding similar movies... 🎬"):
        recommendations, error = get_recommendations(selected_movie, num_recommendations)

    if error:
        st.error(f"⚠️ {error}")
    else:
        st.subheader("🎬 Recommended Movies")
        st.success(f"Showing top {num_recommendations} recommendations for '{selected_movie}'")

        for movie in recommendations:
            with st.container(border=True):
                if movie["poster"] and movie["poster"] != "N/A":
                    st.image(movie["poster"])

                st.markdown(f"**{movie['title']}** ({movie['year']})")
                st.write(f"🎯 Match Score: {movie['match_score']}%")
                st.progress(movie['match_score'] / 100)

                if movie["rating"]:
                    st.write(f"⭐ IMDb: {movie['rating']}")

                with st.expander("Plot"):
                    st.write(movie["plot"])
