"""
Extracts links from tweets
"""
from ...shared.Config import DATA_WORKER_HOST
import requests
from ..just_give_me_text.GiveMeTheText import give_me_the_text
from ...shared.Link import Link
from ...shared.Model import Model
from typing import List
import time
import random

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"
DATA_LINKS = DATA_WORKER_URL + "links"
SUBMIT_DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/set_predict_link_score"

def submit_score(id, score):
    requests.post(SUBMIT_DATA_WORKER_URL, json=[
        {
            "id": id,
            "score": float(score)
        }
    ])

def fetch():
    key = "last_ranked_link_offset"
    last_queued = requests.get(DATA_WORKER_URL + f"key_value?key={key}").json()
    last_queued = last_queued["value"]
    last_queued = last_queued if last_queued is not None else 0

    links = requests.get(DATA_LINKS + f"?skip={last_queued}").json()
    links:List[Link] = list(map(lambda x: Link(**x), links))

    model = Model.load()

    print(f"Ranking links from id :{last_queued}")

    for link in links:
        text = give_me_the_text(link.url)
        if text is None:
            continue
        submit_score(link.id, model(text))
        time.sleep(random.randint(3, 5))

    new_id = last_queued + len(links)
    requests.post(DATA_WORKER_URL + f"key_value?key={key}&value={new_id}").text

    
if __name__ == "__main__":
    fetch()
