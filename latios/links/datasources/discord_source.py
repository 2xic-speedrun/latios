import requests
from dotenv import load_dotenv
import os
import sys

load_dotenv()


def get_channel_messages(channel_id):
    headers = {
        "Cookie": os.getenv("DISCORD_COOKIE"),
        "Authorization": os.getenv("DISCORD_AUTHORIZATION")
    }
    print(headers)
    url =f"https://discord.com/api/v9/channels/{channel_id}/messages?before=1097486945560571926&limit=50"
    print(url)
    messages = requests.get(url, headers=headers)
    print(messages.text)

if __name__ == "__main__":
    get_channel_messages(sys.argv[-1])
