"""
Extracts links from tweets
"""
from ...shared.Config import DATA_WORKER_HOST
from ...shared.Tweet import Tweet
import requests
import urllib
import time
from ..just_give_me_text.GiveMeTheMetadata import GiveMeTheMetadata

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

    delta = time.time() - last_extracted_at
    if delta < (60 * 60):
        return None
    blacklist = [
        'reddit',
        'ycombinator',
        'github'
    ]
    for link in [
        'https://news.ycombinator.com/best'
        'https://old.reddit.com/r/LessWrong/'
    ]:
        metadata = GiveMeTheMetadata().get_metadata(link)
        links = metadata.get('links', None)
        if links is None:
            continue
        for i in links:
            for j in blacklist:
                if j in i:
                    break
            else:
                print((i))
            requests.post(DATA_WORKER_URL + f"save_url?url={url}")

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
#    source_extractor()
    fetch()

