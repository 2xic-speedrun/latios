import argparse
import os
import requests
from ..shared.Config import DATA_WORKER_HOST
"""
Simplify the feedback process, and solve the coldstart problem by giving the model some data 

"""
DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"

def load_file(path, is_good):
    if not os.path.isfile(path):
        raise Exception("File provided is not found!")
    with open(path, "r") as file:
        for i in file.read().split("\n"):
            if len(i) == 0:
                continue
            url = requests.post(f"{DATA_WORKER_URL}/save_url?url={i}")
            id = url.json()["id"]
            requests.post(f"{DATA_WORKER_URL}/link_feedback", json={
                "id": id,
                "is_good": is_good
            })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog = 'GiveMeTheMetadata'
    )
    parser.add_argument('-f', '--file')
    parser.add_argument('-g', '--is-good', type=bool)
    args = parser.parse_args()

    load_file(args.file, args.is_good)
