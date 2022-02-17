import streamlit as st
import pandas as pd
import numpy as np

st.title('Anime Recommender')

dataset_path = '../data/score_matrix.parquet'


@st.cache
def load_data(path):
    score_matrix_df = pd.read_parquet(path)
    return score_matrix_df


@st.cache
def recommendation_system(anime_name, score_matrix_df):
    # grab user ratings for the a certain anime
    anime_user_ratings = score_matrix_df[anime_name]

    # Use Corrwith as a method to get user correlation
    similar_to_anime = score_matrix_df.corrwith(anime_user_ratings)

    # Clean the null values from both movies
    corr_anime = pd.DataFrame(similar_to_anime, columns=['Correlation'])

    # corr_anime.dropna(inplace=True)
    return corr_anime.sort_values('Correlation', ascending=False).head(10)


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(dataset_path)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")


anime = st.text_input("", "Search...")

if st.button("OK"):
    st.dataframe(recommendation_system(anime, data))
