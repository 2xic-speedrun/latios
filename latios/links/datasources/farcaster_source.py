import requests
import re
import validators

def get_farcaster_links(query):
    url = requests.get(f"https://searchcaster.xyz/api/search?text={query}").json()
    print(url.keys())
    for i in url["casts"]:
        text = i["body"]["data"]["text"]
        results = re.findall(r"\w+://\w+\.\w+\.\w+/?[\w\.\?=#]*", text)

        for i in results:
            if validators.url(i):
                print(i)
            else:
                print(i)

if __name__ == "__main__":
    get_farcaster_links("arxiv.org")

