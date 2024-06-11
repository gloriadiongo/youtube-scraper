import pandas as pd
from openai import OpenAI
import streamlit as st

client = OpenAI(
    # This is the default and can be omitted
    api_key=st.secrets['OPENAI_KEY'],
)

def ep_to_season(ep_name):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"From this episode name {ep_name} return the title of the series. I only want the title of the series with no additional information",
            }
        ],
        model="gpt-4",
    )
    return chat_completion.choices[0].message.content

def get_season_name_from_episode(episodes: list):
    seasons = []
    for episode in episodes:
        season = ep_to_season(episode)
        seasons.append(season)
    return seasons

def check_str(x):
    eps = [
        " episode ",
        " épisode ",
        " ep ",
        " ép ",
        "(episode",
        "(épisode",
        "(ep",
        "(ép",
    ]
    for ep in eps:
        try:
            if ep in x.lower():
                return True
        except:
            return False
    return False

def main(df: pd.DataFrame):
    print('Starting processing')
    df.drop_duplicates(subset=["videoID"], inplace=True)
    df.drop(columns=["favoriteCount"], inplace=True)
    df["taukLikes"] = df["likeCount"].astype("float") / df["viewCount"].astype("float")
    df["tauxCommentaires"] = df["commentCount"].astype("float") / df["viewCount"].astype("float")
    df.rename(
        columns={
            "Handle": "Chaine",
            "title": "titreEpisode",
            "publishedAt": "DateVideo",
            "viewCount": "nbVues",
            "likeCount": "nbLikes",
            "commentCount": "nbCommentaires",
        },
        inplace=True,
    )
    df["is_episode"] = df["titreEpisode"].map(check_str)
    new_df = df[df["is_episode"]]
    season_names = get_season_name_from_episode(new_df['titreEpisode'].to_list())
    new_df['titreSerie'] = season_names
    return new_df
