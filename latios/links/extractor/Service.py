"""
Extracts links from tweets
"""
from ...shared.Config import DATA_WORKER_HOST
from ...shared.Tweet import Tweet
import requests
import urllib
import time
from ..just_give_me_text.GiveMeTheMetadata import GiveMeTheMetadata
from ...shared.GetDiskSpace import get_free_disk_space_in_gb
import os
DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"

def fetch():
    last_queued = requests.get(DATA_WORKER_URL + "key_value?key=last_extracted_id").json()
    last_queued = last_queued["value"]
    last_queued = last_queued if last_queued is not None else 0

    tweets = requests.get(DATA_WORKER_URL + f"?skip={last_queued}&direction=asc").json()
    tweets = list(map(lambda x: Tweet(x["tweet"], x['is_good']), tweets))

    print(f"Extracting links from id :{last_queued}")

    for tweet in tweets:
        for (_, link) in tweet.urls():
            if "twitter" in link:
                continue
            url = urllib.parse.quote(link, safe='')
            requests.post(DATA_WORKER_URL + f"save_url?url={url}")
            
    new_id = last_queued + len(tweets)
    requests.post(DATA_WORKER_URL + f"key_value?key=last_extracted_id&value={new_id}").text
    return new_id

def source_extractor():
    last_extracted_at = requests.get(DATA_WORKER_URL + "key_value?key=last_source_feed_extraction").json()
    last_extracted_at = last_extracted_at["value"]
    last_extracted_at = last_extracted_at if last_extracted_at is not None else 0

    path = os.path.join(os.path.dirname(__file__), "crawler.txt")
    if not os.path.isfile(path):
        print("No path file found!")
        return None

    now = time.time()
    delta = now - last_extracted_at
    one_hour = 60 * 60
    one_day = one_hour * 24
    if delta < one_day:
        return None
    blacklist = [
        'reddit',
        'ycombinator',
        'github',
        'apple.com'
    ]
    links = []
    with open(path) as file:
        links = file.read().split("\n")

    for link in links:
        if len(link) == 0:
            continue
        print(f"Checking {link}")
        metadata = GiveMeTheMetadata().get_metadata(link)
        if metadata is None:
            continue
        links = metadata.get('links', None)
        if links is None:
            continue
        for i in links:
            for j in blacklist:
                if j in i:
                    break
            else:
                print((i))
                requests.post(DATA_WORKER_URL + f"save_url?url={i}")
    requests.post(DATA_WORKER_URL + f"key_value?key=last_source_feed_extraction&value={now}").text

if __name__ == "__main__":
    """
    has_new = True
    last_id = None
    while has_new:
        new_id = fetch()
        if last_id != new_id:
            last_id = new_id
        else:
            break
    """
    if get_free_disk_space_in_gb() > 1:
        fetch()
        source_extractor()
    else:
        print("Not enough free space")
