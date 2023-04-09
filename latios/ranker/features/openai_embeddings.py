import os
import requests
from dotenv import load_dotenv
import json
from .cache_embeddings import CacheEmbeddings
load_dotenv()

cache_handler = CacheEmbeddings()

def save_json(name, data):
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        name
    )
    with open(path, "w") as file:
        file.write(json.dumps(data))

def get_models():
    token = os.getenv("OPEN_AI_API_KEY")
    results = requests.get("https://api.openai.com/v1/models", 
        headers={
            "Authorization": f"Bearer {token}" 
        }
    )
    print(results)
    print(results.text)
    save_json(
        "models.json",
        results.json()
    )

def get_embeddings(text, model):
    token = os.getenv("OPEN_AI_API_KEY")
    payload = {
            "input": text,
            "model": model
    }
    cache = cache_handler.load(**payload)
    if cache is not None:
        print("cache")
        return cache
    
    print(payload)
    results = requests.post("https://api.openai.com/v1/embeddings?model", 
        json=payload,
        headers={
            "Authorization": f"Bearer {token}" 
        }
    )
    cache_handler.save(
        payload=payload,
        results=results.json()
    )
    return results.json()

if __name__ == "__main__":
#    get_models()
    get_embeddings("this is some text")
