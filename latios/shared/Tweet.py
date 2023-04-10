import json

class Tweet:
    def __init__(self, tweet_object, is_good=None, predicted_score=None):
        self.json = tweet_object
        self.id = self.json['id']
        self.text = self.json["text"]
        self.user = self.json.get("user", {
            "username": None,
            "profile_image_url": None,
        })
        self.username = self.user["username"]
        self.author_id = self.json.get("author_id", None)
        self.created_at = self.json.get("created_at", None)
        self.conversation_id = self.json.get("conversation_id", None)
        self.profile_image_url = self.user.get("profile_image_url", None)
        if self.profile_image_url is not None:
            self.profile_image_url = self.profile_image_url.replace("_normal", "")
        self.is_good = is_good
        self.tweet_url = f"https://twitter.com/{self.username}/status/{self.id}"

        self.entities = self.json.get("entities", {
            "urls": []
        })
        self.html_text = self.text

        moved_index = 0
        for i in self.entities.get("mentions", []):
            start, end, user = i["start"], i["end"], i["username"]

            mention_url = f"<a href=\"https://twitter.com/{user}\">{user}</a>"
            self.html_text = self.html_text[:start + moved_index] + \
                            mention_url +\
                            self.html_text[moved_index + end:]
            moved_index += len(mention_url) - (i["end"] - i["start"])

        for (short_url, expanded_url) in self.urls():
            self.html_text = self.html_text.replace(short_url, 
                "<a href=\"{link}\">{link}</a>".format(link=expanded_url)
            )

        self.predicted_score = predicted_score

    def urls(self):
        return list(map(lambda i: (i["url"], i["expanded_url"]), self.entities.get("urls", [])))    

    def __str__(self) -> str:
        return json.dumps(self.__dict__())

    def __dict__(self):
        return {
            "tweet": self.json,
            "is_good": self.is_good,
            "predicted_score": self.predicted_score,
        }

    def __repr__(self) -> str:
        return self.__str__()

