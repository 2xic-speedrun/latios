from .Database import Database
from .twitter.Twitter import Twitter


class DataWorker:
    def __init__(self, database: Database, twitter: Twitter) -> None:
        self.database = database
        self.twitter = twitter
        self.last_synchronized_timeline_tweet = "LAST_SYNCHRONIZED_TIMELINE_TWEET"
        self.last_viewed_timeline_tweet = "LAST_VIEWED_TIMELINE_TWEET"

    def get_timeline(self,
                     skip=None,
                     first=None,
                     order_by=None
                     ):
        since_id = self.database.get_metadata_key(
            self.last_viewed_timeline_tweet)
        return self.database.get_all(
            since_id=since_id,
            skip=skip,
            first=first,
            order_by=order_by,
            direction="DESC",
        )

    def update_timeline(self):
        since_id = self.database.get_metadata_key(
            self.last_synchronized_timeline_tweet)
        if since_id is None:
            since_id = 1602552509545041920
        tweets = self.twitter.fetch_timeline(
            since_id=since_id
        )
        print("Fetched tweets :)")
        max_tweet_id = None
        count = 0
        for i in tweets:
            self.database.save(i)
            if max_tweet_id is None:
                max_tweet_id = i.id
            else:
                max_tweet_id = max(max_tweet_id, i.id)
            count += 1
        print("Saved tweets :)")

        if max_tweet_id:
            self.database.set_metadata_key_value(
                self.last_synchronized_timeline_tweet, max_tweet_id)
        return count
