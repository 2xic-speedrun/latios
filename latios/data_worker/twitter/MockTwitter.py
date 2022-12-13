from .Twitter import Twitter

class MockTwitter(Twitter):
    def __init__(self, example_tweets) -> None:
        self.example_tweets = example_tweets

    def fetch_timeline(self, since_id):
        if since_id is None:
            return self.example_tweets
        return list(
            filter(lambda x: since_id < x.id, self.example_tweets)
        )

        