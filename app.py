import streamlit as st
import pickle
import requests
import pandas as pd

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f03e5ee6ce01f7ef93dd3e43bca42332&language=en-US")
    data = response.json()
    poster_path = "http://image.tmdb.org/t/p/w500/" + data.get('poster_path')                 
    return poster_path
    
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movie_list:   
        recommended_movie_posters.append(fetch_poster(movies_df.iloc[i[0]].id)) 
        recommended_movies.append(movies_df.iloc[i[0]].title)
    return recommended_movies, recommended_movie_posters

movies_df = pickle.load(open('movie_list.pkl', 'rb'))
movies = movies_df['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommendation System")

selected_movie = st.selectbox(
    'Select a movie to get recommendations:',
    movies
)

if st.button('Recommend'):
    Names, Posters = recommend(selected_movie)
    st.write(f"Recommendations for '{selected_movie}':")
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(len(Names)):
        with col1:
            st.image(Posters[i])
            st.text(Names[i])