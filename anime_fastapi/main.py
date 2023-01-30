from fastapi import FastAPI, Request, HTTPException
import pandas as pd

app = FastAPI()

anime_df = pd.read_csv("../data/AnimeList.csv")
anime_titles = anime_df["title_english"].dropna().tolist()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/animes/")
async def animes() -> list[str]:
    return anime_titles


@app.get("/animes/{anime_title}")
async def anime(anime_title: str) -> list:
    if anime_title in anime_titles:
        anime_info = anime_df[anime_df["title_english"] == anime_title].to_dict(
            orient="records"
        )
        return anime_info
    else:
        return HTTPException(status_code=404, detail="Anime not found")
