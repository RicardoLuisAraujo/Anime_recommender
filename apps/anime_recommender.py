import streamlit as st
import pandas as pd
import numpy as np
from mal import AnimeSearch

st.set_page_config(
    page_title="Anime Recommender App",
    page_icon="🧊",
    layout="centered",  # or centered
    initial_sidebar_state="expanded",
)

st.title("Anime Recommender")
st.write(
    "Use this site to search for Similar Anime or to find great anime especially for you!"
)

dataset_path = "../data/score_matrix.parquet"
anime_img_path = "../data/AnimeList.csv"


@st.cache
def load_data(path):
    score_matrix_df = pd.read_parquet(path)
    return score_matrix_df


@st.cache
def load_data_images(path):
    anime_images_df = pd.read_csv(path, usecols=["title", "image_url"])
    return anime_images_df


@st.cache
def get_image_url(anime_name):
    search = AnimeSearch(anime_name)
    img_url = search.results[0].image_url
    return img_url


@st.cache
def recommendation_system(anime_name, score_matrix_df):
    # grab user ratings for the a certain anime
    anime_user_ratings = score_matrix_df[anime_name]

    # Use Corrwith as a method to get user correlation
    similar_to_anime = score_matrix_df.corrwith(anime_user_ratings)

    # Clean the null values from both movies
    corr_anime = pd.DataFrame(similar_to_anime, columns=["Correlation"])

    # corr_anime.dropna(inplace=True)
    return (
        corr_anime.sort_values("Correlation", ascending=False)
        .head(10)
        .rename_axis("anime")
        .reset_index()
    )


# Create a text element and let the reader know the data is loading.
data_load_state = st.text("Loading data...")
# Load 10,000 rows of data into the dataframe.
data = load_data(dataset_path)
data_images = load_data_images(anime_img_path)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

anime = st.text_input("Check for Similar Animes", placeholder="Anime Name")
# button_search = st.button("Search")

if anime:

    img_url = get_image_url(anime)
    col1, col2, col3 = st.columns([1, 1, 1])
    col2.image(img_url, caption=anime)

    recommendation_df = recommendation_system(anime, data).iloc[1:]
    st.header("People Also Liked...")
    st.write("(No Machine Learning)")

    column = st.columns(len(recommendation_df))

    for num in range(len(recommendation_df)):
        anime_title = recommendation_df.iloc[num]["anime"]

        img_url = get_image_url(anime_title)

        with column[num]:
            st.image(img_url, caption=anime_title, use_column_width="always")

    st.header("Made for You...")
    st.write("(Collaborative Learner - FastAI Deep Learning Model)")
