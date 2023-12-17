import requests
from ...shared.Config import DATA_WORKER_HOST
from ...shared.Link import Link
from typing import List
from ..just_give_me_text.GiveMeTheMetadata import GiveMeTheMetadata
import argparse 
import time

category_id = 0
last_queued = 0

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/links?category_id=0&order_by=id&direction=asc&skip={last_queued}"
SAVE_URL_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/save_url"

def get_link_batch():
    links = requests.get(DATA_WORKER_URL).json()
    links: List[Link] = list(map(lambda x: Link(**x), links))

def save_url(url):
    print(url)
    return requests.post(SAVE_URL_WORKER_URL + "?url=" + url + "&category_id=" + str(category_id)).text

def store_connected_links(url):
    metadata = GiveMeTheMetadata().get_metadata(url)
    save_url(url)
    if metadata is None:
        return None 
    for i in metadata.get("links", []):
        response = save_url(i)  
        print(response)
    time.sleep(3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog = 'CategoryCrawler'
    )
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-c', '--category-id', type=int, required=True)
    args = parser.parse_args()
    category_id = args.category_id

    with open(args.file, "r") as file:
        links = file.read().split("\n")
        for i in links:
            if len(i) == 0:
                continue
            store_connected_links(
                i
            )
