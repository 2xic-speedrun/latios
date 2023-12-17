import requests
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv()


def get_channel_messages(channel_id):
    headers = {
        "Cookie": os.getenv("DISCORD_COOKIE"),
        "Authorization": os.getenv("DISCORD_AUTHORIZATION")
    }
    print(headers)
    url =f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=50"
    print(url)
    messages = requests.get(url, headers=headers)
    data = json.loads(messages.text)
    links = []
    for i in data:
        for j in i["embeds"]:
            if j["type"] == "link":
                links.append(j["url"])
    print(links)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Expected: script.py [channelId]")
    get_channel_messages(sys.argv[-1])
