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
            moved_index += len(mention_url) - len(user)

        for i in self.entities.get("urls", []):
            self.html_text = self.html_text.replace(i["url"], 
                "<a href=\"{link}\">{link}</a>".format(link=i["expanded_url"])
            )

    def __str__(self) -> str:
        return json.dumps(self.__dict__())

    def __dict__(self):
        return {
            "tweet": self.json,
            "is_good": self.is_good,
        }

    def __repr__(self) -> str:
        return self.__str__()

