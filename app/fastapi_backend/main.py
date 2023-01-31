from fastapi import FastAPI, HTTPException
import pandas as pd
from models import ItemType, SearchedItem
from mal import AnimeSearch, MangaSearch, Anime, Manga
import json

app = FastAPI()

anime_df = pd.read_csv("../../data/AnimeList.csv")
anime_titles = anime_df["title_english"].dropna().tolist()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/animes/")
async def animes():
    return anime_titles


@app.get("/search/{item_type}/{searched_name}")
async def search(
    item_type: str,
    searched_name: str,
):

    if item_type not in ["anime", "manga"]:
        raise HTTPException(
            status_code=404, detail="Item Type can only be anime or manga"
        )

    searched_item = SearchedItem(
        item_type=item_type,
        name=searched_name,
    )

    if searched_item.item_type == ItemType.anime:
        search = AnimeSearch(searched_item.name)
        searched_item = Anime(search.results[0].mal_id)
    elif searched_item.item_type == ItemType.manga:
        search = MangaSearch(searched_item.name)
        searched_item = Manga(search.results[0].mal_id)
    else:
        raise HTTPException(
            status_code=404, detail="Item Type can only be anime or manga"
        )

    if len(search.results) == 0:
        raise HTTPException(status_code=404, detail="Item not found in MyAnimeList")

    item_info = {
        "title": searched_item.title_english,
        "url": searched_item.url,
        "image_url": searched_item.image_url,
        "score": searched_item.score,
        "synopsis": searched_item.synopsis,
    }

    return item_info
