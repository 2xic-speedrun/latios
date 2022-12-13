import json


class Tweet:
    def __init__(self, tweet_object):
        self.json = tweet_object
        self.id = self.json['id']
        self.text = self.json["text"]
        self.user = self.json.get("user", {
            "username": None
        })["username"]
        self.author_id = self.json.get("author_id", None)
        self.created_at = self.json.get("created_at", None)
        self.conversation_id = self.json.get("conversation_id", None)

    def __str__(self) -> str:
        return json.dumps(self.json)

    def __repr__(self) -> str:
        return self.__str__()
