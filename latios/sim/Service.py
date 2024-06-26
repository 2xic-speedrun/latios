import requests
from ..shared.Config import DATA_WORKER_HOST
from ..shared.Tweet import Tweet
from .Redis import Redis
import numpy as np
from .Chroma import Chroma

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"


def fetch_more_tweets(first=50):
    crawl_key = "last_sim_id"
    last_queued = requests.get(DATA_WORKER_URL + f"key_value?key={crawl_key}").json()
    last_queued = last_queued["value"]
    last_queued = last_queued if last_queued is not None else 0

    tweets = requests.get(DATA_WORKER_URL + f"?skip={last_queued}&direction=asc&first={first}").json()
    tweets = list(map(lambda x: Tweet(x["tweet"], x['is_good']), tweets))

    for i in tweets:
        yield i

    new_id = last_queued + len(tweets)
    print(new_id)
    requests.post(DATA_WORKER_URL + f"key_value?key={crawl_key}&value={new_id}").text
    return new_id

if __name__ == "__main__":
#    vector_db = Redis()
    vector_db = Chroma()

    for i in fetch_more_tweets():
        #i = np.random.rand(128).astype(np.float32).tobytes()
        #print(i)
        vector_db.add_tweet(i)
        print(i.id)
        for i in vector_db.get_sim(i):
            print(f"\t{i.id}")

