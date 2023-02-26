import requests
from ..shared.Config import DATA_WORKER_HOST
from ..shared.Tweet import Tweet
from ..shared.Link import Link
import requests

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/dataset"
#DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/dataset?INCLUDE_LINKS=1"

def get_dataset(**kwargs):
  #  INCLUDE_LINKS = kwargs.get("INCLUDE_LINKS", False)
  #  URL = DATA_WORKER_URL + "?INCLUDE_LINKS=True" if INCLUDE_LINKS else DATA_WORKER_URL
    tweets = list(map(lambda x: 
        Tweet(x["tweet"], x['is_good'])\
        if x.get("is_tweet", True) == True else\
        Link(text=x["tweet"], score=x['is_good']), 
        requests.get(DATA_WORKER_URL).json()
    ))

    good_tweets = list(filter(lambda x: x.is_good == True, tweets))
    bad_tweets = list(filter(lambda x: x.is_good == False, tweets))

    size = min(len(good_tweets), len(bad_tweets))

    good_tweets = good_tweets[:size]
    bad_tweets = bad_tweets[:size]

    X = good_tweets + bad_tweets
    y = [1, ] * size + [0, ] * size

    print(f"Training on {size*2} samples")

    return X, y

