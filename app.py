import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f8cd1428e7058e4815868ad5a1634673'.format(movie_id))
    data = response.json()
    if 'poster_path' in data:
        poster_path = data['poster_path']
        return "https://image.tmdb.org/t/p/original/" + poster_path
    else:
        return None  # Return None if poster_path is not available for the movie

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list :
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster  


movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))
st.header('Movies Recommender System')

selected_movie_name=st.selectbox(
'Type or select a movie from the dropdown',
movies['title'].values)

if st.button("Show Recommend"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
