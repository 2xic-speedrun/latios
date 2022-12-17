"""
Extracts links from tweets
"""
from ...shared.Config import DATA_WORKER_HOST
from ...shared.Tweet import Tweet
import requests
import urllib

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"

def fetch():
    last_queued = requests.get(DATA_WORKER_URL + "key_value?key=last_extracted_id").json()
    last_queued = last_queued["value"]
    last_queued = last_queued if last_queued is not None else 0

    tweets = requests.get(DATA_WORKER_URL + f"?skip={last_queued}").json()
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

    
if __name__ == "__main__":
    fetch()
