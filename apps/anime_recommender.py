import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.title('Anime Recommender')

dataset_path = '../data/score_matrix.parquet'
anime_img_path = '../data/AnimeList.csv'


@st.cache
def load_data(path):
    score_matrix_df = pd.read_parquet(path)
    return score_matrix_df


@st.cache
def load_data_images(path):
    anime_images_df = pd.read_csv(path, usecols=["title", "image_url"])
    return anime_images_df


@st.cache
def recommendation_system(anime_name, score_matrix_df):
    # grab user ratings for the a certain anime
    anime_user_ratings = score_matrix_df[anime_name]

    # Use Corrwith as a method to get user correlation
    similar_to_anime = score_matrix_df.corrwith(anime_user_ratings)

    # Clean the null values from both movies
    corr_anime = pd.DataFrame(similar_to_anime, columns=['Correlation'])

    # corr_anime.dropna(inplace=True)
    return corr_anime.sort_values('Correlation', ascending=False).head(10).rename_axis('anime').reset_index()


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(dataset_path)
data_images = load_data_images(anime_img_path)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")


anime = st.text_input("Check for Similar Animes", placeholder='Anime Name')
button_search = st.button("Search")

if button_search or anime:
    recommendation_df = recommendation_system(anime, data)
    st.header('People Also Liked... (No Machine Learning)')
    st.dataframe(recommendation_df)

    for num in range(len(recommendation_df)):
        anime_title = recommendation_df.iloc[num]['anime']
        img_url = data_images[data_images.title ==
                              anime_title]['image_url'].item()
        print(img_url)
        st.image(img_url, caption=anime_title)
