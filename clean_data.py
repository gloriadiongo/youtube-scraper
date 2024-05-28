import pandas as pd

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
    return new_df
