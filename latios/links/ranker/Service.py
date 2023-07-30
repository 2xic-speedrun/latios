"""
Scores links
"""
from ...shared.Config import DATA_WORKER_HOST
import requests
from ..just_give_me_text.GiveMeTheMetadata import GiveMeTheMetadata
from ...shared.Link import Link
from ...shared.Model import Model
from typing import List
import time
import random
from ...shared.Cache import Cache
from ...shared.GetDiskSpace import get_free_disk_space_in_gb
import time

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"
DATA_LINKS = DATA_WORKER_URL + "links"
SUBMIT_DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/save_link_with_id"
LAST_RANKED_OFFSET_KEY = "last_ranked_link_offset"

def submit_score(id, score, title, netloc, description):
    response = requests.post(SUBMIT_DATA_WORKER_URL, json=[
        {
            "id": id,
            "predicted_score": float(score),
            "netloc": netloc,
            "title": title,
            "description": description
        }
    ])
    print(response.text)


def get_links(query_args):
    url = DATA_LINKS + query_args
    print(url)
    links = requests.get(url).json()
    links: List[Link] = list(map(lambda x: Link(**x), links))
    return links
    
def get_batch():
    last_queued = requests.get(DATA_WORKER_URL + f"key_value?key={LAST_RANKED_OFFSET_KEY}").json()
    last_queued = last_queued["value"]
    if last_queued is None:
        last_queued = 0

    links = get_links(f"?skip={last_queued}&order_by=id&direction=asc")
    fresh_links = get_links(f"?order_by=id&direction=desc&has_predicted_score=false")
    new_id = last_queued + len(links)

    links += fresh_links
    
    print(f"Ranking links from id :{last_queued}")
    print(len(links))

    return (
        links,
        last_queued,
        new_id
    )

def fetch():
    links, last_queued, new_id = get_batch()
    model = Model.load()
    cache = Cache()

    for link in links:
        try:
            print(f"Checking link {link.url}")
            metadata = GiveMeTheMetadata().get_metadata(link.url)
            if metadata is None:
                continue
            print("Scoring site ...")
            score = model(metadata["text"])
            print(score)
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

    requests.post(DATA_WORKER_URL + f"key_value?key={LAST_RANKED_OFFSET_KEY}&value={new_id}").text
    print("Updated")
    
if __name__ == "__main__":
    while True:
        if get_free_disk_space_in_gb() > 1:
            fetch()
        else:
            print("Not enough free space")
            exit(0)
        print("Sleeping")
        time.sleep(30)
