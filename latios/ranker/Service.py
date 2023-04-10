from ..shared.Tweet import Tweet
import requests
from ..shared.Model import Model
from ..shared.Config import DATA_WORKER_HOST
import time

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/predict_score_queue"
SUBMIT_DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/set_predict_score"
FETCH_DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/fetch"

model = Model.load()

def fetch_more_tweets():
    return requests.get(FETCH_DATA_WORKER_URL).text

def submit_score(id, score):
    requests.post(SUBMIT_DATA_WORKER_URL, json=[
        {
            "id": id,
            "score": float(score)
        }
    ])

if __name__ == "__main__":
    start = 0

    while True:
        if 60 * 60 < (time.time() - start):
            new_tweets_count = fetch_more_tweets()
            print(f"Fetched {new_tweets_count} new tweets")
            start  = time.time()

        tweets = list(map(lambda x: Tweet(x["tweet"], x['is_good']), requests.get(DATA_WORKER_URL).json()))
        count = len(tweets)
        print(f"Scoring {count} tweets")
        for i in tweets:
            score = model(i.text)
            print(i.id)
            submit_score(i.id, score)

        time.sleep(30)
