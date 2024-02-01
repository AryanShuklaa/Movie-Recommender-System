import streamlit as st
import pickle
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Create a session with retry strategy to handle connection errors
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Function to fetch movie poster using the TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=03f18eee59077a13aaa2b8709ac8d7f3&language=en-US"
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions, such as connection errors
        st.error(f"Error fetching poster: {e}")
        return None
    except Exception as e:
        # Handle unexpected exceptions
        st.error(f"An unexpected error occurred: {e}")
        return None


# Load movie data and similarity matrix from pickle files
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Streamlit header for the Movie Recommender System
st.header("Movie Recommender System")

# Use st.selectbox to create a dropdown with movie options
selectvalue = st.selectbox("Select a movie from the dropdown", movies_list)

# Function to recommend movies based on selected movie
def recommend(movie):
    # Find the index of the selected movie in the DataFrame
    index = movies[movies['title'] == movie].index[0]
    
    # Calculate similarity and get top 5 recommendations
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommended_movie = []
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommended_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommended_movie, recommend_poster

# Display button to trigger movie recommendations
if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    
    # Display the recommendations in columns with movie names and images
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
