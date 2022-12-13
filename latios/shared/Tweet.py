import json


class Tweet:
    def __init__(self, tweet_object, is_good=None):
        self.json = tweet_object
        self.id = self.json['id']
        self.text = self.json["text"]
        self.user = self.json.get("user", {
            "username": None,
            "profile_image_url": None,
        })
        self.username = ["username"]
        self.author_id = self.json.get("author_id", None)
        self.created_at = self.json.get("created_at", None)
        self.conversation_id = self.json.get("conversation_id", None)
        self.profile_image_url = self.user.get("profile_image_url", None)
        self.is_good = is_good

    def __str__(self) -> str:
        return json.dumps({
            "tweet": self.json,
            "is_good": self.is_good,
        })

    def __repr__(self) -> str:
        return self.__str__()
