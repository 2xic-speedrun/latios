
class Link:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.get("id", None)
        self.url = kwargs.get("url", None)
        self.predicted_score = kwargs.get("predicted_score", None)
        self.score = kwargs.get("score", None)
        self.has_feedback = self.score is not None
        self.description = kwargs.get("description", None)
        self.title = kwargs.get("title", None)
        self.text = kwargs.get("text", None)

        self.is_good = self.score

        # TODO: Add thumbnail (?)
        # youtube can be fetched with http://www.get-youtube-thumbnail.com/
        # static html can be taken with a headless browser

    def __dict__(self):
        return {
            "tweet": self.text,
            "is_good": self.is_good,
        }
