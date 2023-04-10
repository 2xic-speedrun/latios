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
                     order_by=None,
                     direction=None,
                     last_n_days=None,
                     conversation_id=None,
                     screen_name=None,
                     has_score=None,
                     min_predicted_score=None,
        ):
        since_id = self.database.get_metadata_key(
            self.last_viewed_timeline_tweet)
        return self.database.get_all_tweets(
            since_id=since_id,
            skip=skip,
            first=first,
            has_score=has_score,
            order_by=order_by,
            direction=direction,
            last_n_days=last_n_days,
            conversation_id=conversation_id,
            screen_name=screen_name,
            min_predicted_score=min_predicted_score,
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
            self.database.save_tweet(i)
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
