"""
Extracts links from tweets
"""
from ...shared.Config import DATA_WORKER_HOST
import requests
from ..just_give_me_text.GiveMeTheMetadata import GiveMeTheMetadata
from ...shared.Link import Link
from ...shared.Model import Model
from typing import List
import time
import random

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"
DATA_LINKS = DATA_WORKER_URL + "links"
SUBMIT_DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/save_link_with_id"

def submit_score(id, score, title, netloc, description):
    requests.post(SUBMIT_DATA_WORKER_URL, json=[
        {
            "id": id,
            "predicted_score": float(score),
            "netloc": netloc,
            "title": title,
            "description": description
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
        try:
            print(f"Checking link {link.url}")
            metadata = GiveMeTheMetadata().get_metadata(link.url)
            if metadata is None:
                continue
            score = model(metadata["text"])
            submit_score(
                id=link.id,
                title=metadata["title"],
                score=score,
                netloc=metadata["netloc"],
                description=metadata["text"][:300]
            )
            time.sleep(random.randint(3, 5))
        except Exception as e:
            print(e)

    new_id = last_queued + len(links)
   # if len(links) == 0:
    #    new_id = 0
    requests.post(DATA_WORKER_URL + f"key_value?key={key}&value={new_id}").text
    
if __name__ == "__main__":
    fetch()
