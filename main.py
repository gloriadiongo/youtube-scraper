from typing import Set, Generator
import glob

from googleapiclient.discovery import build, Resource
import pandas as pd
import dateparser
from datetime import datetime, timedelta

columns=[
    "videoID",
    "publishedAt",
    "title",
    "description",
    "viewCount",
    "likeCount",
    "favoriteCount",
    "commentCount",
    "Handle",
]

def get_video_details(youtube_client: Resource, video_id: str, handle: str):
    request = youtube_client.videos().list(part="snippet,statistics", id=video_id)

    video_details = request.execute()["items"][0]
    video_details_dict = {
        "videoID": video_id,
        "publishedAt": video_details["snippet"].get("publishedAt"),
        "title": video_details["snippet"].get("title"),
        "description": video_details["snippet"].get("description"),
        "viewCount": video_details["statistics"].get("viewCount"),
        "likeCount": video_details["statistics"].get("likeCount"),
        "favoriteCount": video_details["statistics"].get("favoriteCount"),
        "commentCount": video_details["statistics"].get("commentCount"),
        "Handle": handle,
    }

    return video_details_dict

def get_handle_uploaded_videos(
    youtube_client: Resource, handle: str, nextPageToken: str | None = None, days_back: int = 7
) -> Generator:

    tz = dateparser.parse("2024-05-25T07:30:07Z").tzinfo
    end_date = (datetime.now(tz) - timedelta(days=days_back)).date()
    print(f"Getting videos for {handle} handle")
    res = (
        youtube_client.channels().list(part="contentDetails", forHandle=handle)
    ).execute()
    uploads_id = res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    while True:
        videos = (
            youtube_client.playlistItems()
            .list(
                part="contentDetails",
                playlistId=uploads_id,
                maxResults=50,
                pageToken=nextPageToken,
            )
            .execute()
        )

        data = []
        subData = {}
        for video in videos["items"]:
            videoID = video["contentDetails"]["videoId"]

            subData = get_video_details(youtube_client, videoID, handle)
            if dateparser.parse(subData["publishedAt"]).date() < end_date:
                print(f'{subData["publishedAt"]} is past {days_back} days back')
                break
            else:
                data.append(subData)

        if nextPageToken is None:
            print(f'{videos["pageInfo"]["totalResults"]} videos to get their info')

        # if publishedAt is absent 1000, a very old date is used
        if dateparser.parse(subData.get("publishedAt", "1000")).date() < end_date:
            nextPageToken = None
        else:
            nextPageToken = videos.get("nextPageToken", None)

        yield data, nextPageToken
        if nextPageToken is None:
            return

def engine(yt_api_key: str, days_back: int, handles: list):
    youtube = build("youtube", "v3", developerKey=yt_api_key)
    #file_path = "youtube_handles_videos_data.csv"
    all_data = []
    for handle in handles:
        try:
            result_gen = get_handle_uploaded_videos(youtube, handle, days_back=days_back)
            while True:
                data, nextPageToken = next(result_gen)
                all_data.append(data)
                if nextPageToken is None:
                    break
        except TypeError:
            pass
    df = pd.DataFrame(data, columns=columns)
    return df
