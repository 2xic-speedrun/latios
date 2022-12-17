

class Link:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs["id"]
        self.url = kwargs["url"]
        self.predicted_score = kwargs["predicted_score"]
