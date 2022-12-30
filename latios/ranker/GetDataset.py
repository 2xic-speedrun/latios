import requests
from ..shared.Config import DATA_WORKER_HOST
from ..shared.Tweet import Tweet
import requests

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/dataset"

def get_dataset(**kwargs):
    tweets = list(map(lambda x: Tweet(x["tweet"], x['is_good']), requests.get(DATA_WORKER_URL).json()))

    good_tweets = list(filter(lambda x: x.is_good == True, tweets))
    bad_tweets = list(filter(lambda x: x.is_good == False, tweets))

    size = min(len(good_tweets), len(bad_tweets))

    good_tweets = good_tweets[:size]
    bad_tweets = bad_tweets[:size]

    X = good_tweets + bad_tweets
    y = [1, ] * size + [0, ] * size

    print(f"Training on {size*2} samples")

    return X, y

