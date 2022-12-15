from ..shared.Tweet import Tweet
import requests
from .Model import Model
from ..shared.Config import DATA_WORKER_HOST
import time

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/predict_score_queue"
SUBMIT_DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/set_predict_score"

model = Model.load()

def submit_score(id, score):
    requests.post(SUBMIT_DATA_WORKER_URL, json=[
        {
            "id": id,
            "score": float(score)
        }
    ])

while True:
    tweets = list(map(lambda x: Tweet(x["tweet"], x['is_good']), requests.get(DATA_WORKER_URL).json()))
    count = len(tweets)
    print(f"Scoring {count} tweets")
    for i in tweets:
        score = model(i.text)
        print(i.id)
        submit_score(i.id, score)

    time.sleep(30)
