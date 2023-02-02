import pandas as pd

# recomedation system for similar anime, no ML, just correlation based on user ratings
def recommendation_system(
    anime_name: str, score_matrix_df: pd.DataFrame
) -> pd.DataFrame:

    # grab user ratings for the a certain anime
    anime_user_ratings = score_matrix_df[anime_name]

    # Use Corrwith as a method to get user correlation
    similar_to_anime = score_matrix_df.corrwith(anime_user_ratings)

    # Clean the null values from both movies
    corr_anime = pd.DataFrame(similar_to_anime, columns=["Correlation"])

    # sort dataframe by correlation and choosing only the top 10 anime
    return corr_anime.sort_values("Correlation", ascending=False).head(10).reset_index()
