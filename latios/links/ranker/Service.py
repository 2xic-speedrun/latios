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
from ..Cache import Cache

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"
DATA_LINKS = DATA_WORKER_URL + "links"
SUBMIT_DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/save_link_with_id"
LAST_RANKED_OFFSET_KEY = "last_ranked_link_offset"

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


def get_batch():
    last_queued = requests.get(DATA_WORKER_URL + f"key_value?key={LAST_RANKED_OFFSET_KEY}").json()
    last_queued = last_queued["value"]
    if last_queued is None:
        last_queued = 0

    links = requests.get(
        DATA_LINKS + f"?skip={last_queued}&order_by=id&direction=asc").json()
    links: List[Link] = list(map(lambda x: Link(**x), links))
   
    print(f"Ranking links from id :{last_queued}")

    return (
        links,
        last_queued
    )

def fetch():
    links, last_queued = get_batch()
    model = Model.load()

    cache = Cache()

    for link in links:
        try:
            print(f"Checking link {link.url}")
            metadata = GiveMeTheMetadata().get_metadata(link.url)
            if metadata is None:
                continue
            score = model(metadata["text"])
            submit_score(
                id=link.id,
                title=metadata.get("title", None),
                score=score,
                netloc=metadata["netloc"],
                description=metadata["text"][:300]
            )
            cache.save(
                link.url,
                metadata
            )
            time.sleep(random.randint(3, 5))
        except Exception as e:
            print(e)

    new_id = last_queued + len(links)
    requests.post(DATA_WORKER_URL + f"key_value?key={LAST_RANKED_OFFSET_KEY}&value={new_id}").text

if __name__ == "__main__":
    fetch()
