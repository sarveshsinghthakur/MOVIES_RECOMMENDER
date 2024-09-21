import numpy as np
import pandas as pd
import pickle
import streamlit as st
 
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(imdb_id):
    print(imdb_id)
    if pd.isna(imdb_id) or imdb_id == '':
        return None
    return f"https://imdb.com/title/tt{imdb_id}/mediaindex?ref_=tt_pv_mi_sm"

def recommend(movie):
    movie = movie.lower()
    matched_movies = movies[movies['tags'].str.lower().str.contains(movie)]
    
    if matched_movies.empty:
        return f"Movie '{movie}' not found in the dataset."
    
    index = matched_movies.index[0]
    
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommendations = []
    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].original_title
        imdb_id = movies.iloc[i[0]].id
        poster_url = fetch_poster(imdb_id)
        recommendations.append((movie_title, poster_url))
    
    return recommendations

st.title("Movie Recommendation System")
user_input = st.text_input("Enter a movie title:")

if user_input:
    recommendations = recommend(user_input)
    if isinstance(recommendations, str):
        st.write(recommendations)
    else:
        st.write(f"Movies similar to '{user_input}':")
        for title, poster in recommendations:
            st.write(title)
            if poster:
                st.image(poster, width=150)   
