import streamlit as st
import json
import requests

animes: list = requests.get(url="http://127.0.0.1:8000/animes").json()


st.set_page_config(
    page_title="Anime Recommender App",
    page_icon="🧊",
    layout="centered",  # or centered
    initial_sidebar_state="expanded",
)

st.title("Anime Wiki & Recommender")
st.write(
    "Use this site to search for more information on the anime you're looking for and to search for similar Anime especially for you!"
)

item_type = st.selectbox(
    "Select the Type of Item you want to search", ("anime", "manga")
)
item = st.selectbox(
    "Write the Anime or Manga you Want more Info and Recommendations", (animes)
)
search_button = st.button("Search")

if search_button:

    item_info = requests.get(
        url=f"http://127.0.0.1:8000/search/{item_type}/{item}"
    ).json()

    st.title(item_info.get("title"))
    st.image(
        item_info["image_url"], caption=item_info["title"], use_column_width="always"
    )
