"""
Extracts videos from youtube channel
"""
from ...shared.Config import DATA_WORKER_HOST
import requests
from youtube_dl import YoutubeDL
import urllib
import time

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"

urls = [
    "@jblow888/videos",
    "@realmartinshkreli/streams",
    "@lexfridman/videos",
    "@developertea1337/videos"
]

def get_last_id(username):
    username = username.split("/")[0]
    last_queued = requests.get(DATA_WORKER_URL + "key_value?key={username}").json()
    last_queued = last_queued["value"]
    last_queued = last_queued if last_queued is not None else 1

    return last_queued

def set_last_id(username, new_id):
    username = username.split("/")[0]
    requests.post(DATA_WORKER_URL + f"key_value?key={username}&value={new_id}").text

for user in urls:
    url = "https://www.youtube.com/" + user
    playlist_start = get_last_id(user)
    ydl_opts = {
        "playliststart": playlist_start,
        "playlistend": playlist_start + 30,
        "nocheckcertificate": True,
    }

    video_ids = []
    with YoutubeDL(ydl_opts) as ydl:
        obj = ydl.extract_info(url, download=False)
        for obj_vid in obj["entries"]:
            video_ids.append(
                "https://www.youtube.com/watch?v=" + obj_vid["webpage_url_basename"]
            )
    for url in video_ids:
        url = urllib.parse.quote(url, safe='')
        response = requests.post(DATA_WORKER_URL + f"save_url?url={url}")
        print(response)
    time.sleep(15 * 60)
    