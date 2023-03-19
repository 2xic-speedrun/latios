"""
Should rank a link *instantly*
"""
from ..shared.Config import DATA_WORKER_HOST
import requests
from .just_give_me_text.GiveMeTheMetadata import GiveMeTheMetadata
from ..shared.Model import Model
from ..shared.Cache import Cache
from ..shared.GetDiskSpace import get_free_disk_space_in_gb

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"
DATA_LINKS = DATA_WORKER_URL + "links"
SAVE_URL_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/save_url"
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

def rank(url):
    model = Model.load()
    cache = Cache()

    response = requests.post(SAVE_URL_WORKER_URL + "?url=" + url)
    link_id = response.json()["id"]
    metadata = GiveMeTheMetadata().get_metadata(url)
    score = model(metadata["text"])
    submit_score(
        id=link_id,
        title=metadata.get("title", None),
        score=score,
        netloc=metadata["netloc"],
        description=metadata["text"][:300]
    )
    cache.save(
        url,
        metadata
    )
    print((url, score))

if __name__ == "__main__":
    if get_free_disk_space_in_gb() > 1:
        rank("https://machinelearning.apple.com/research/vision-inspired-method")
