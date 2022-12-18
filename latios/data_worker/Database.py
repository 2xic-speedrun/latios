import sqlite3
from contextlib import contextmanager
from ..shared.Tweet import Tweet
from typing import List
import json
from ..shared.Config import MODEL_VERSION
from .database.KeyValue import KeyValue
from .database.Tweets import Tweets
from .database.Links import Links

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.key_value = KeyValue(self)
        self.tweets = Tweets(self)
        self.links = Links(self)
        self._setupDb()

    def _setupDb(self):
        with self.connection() as con:
            cur = con.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS metadata (
                    key varchar PRIMARY KEY, 
                    value int
                );
                """
            )

    def get_all(self, since_id=None, has_score=None, has_predicted_score=None, first=None, skip=None, order_by=None, direction=None, model_version=None, last_n_days=None) -> List[Tweet]:
        return self.tweets.get_all(
            since_id=since_id,
            has_score=has_score,
            has_predicted_score=has_predicted_score,
            first=first,
            skip=skip,
            order_by=order_by,
            direction=direction,
            model_version=model_version,
            last_n_days=last_n_days
        )

    def get_metadata_key(self, key):
        return self.key_value.get_metadata_key(key)

    def set_metadata_key_value(self, key, value):
        return self.key_value.set_metadata_key_value(key, value)

    def set_tweet_predicted_score(self, id, score):
        return self.tweets.set_tweet_predicted_score(id, score)

    def set_tweet_score(self, id, is_good):
        return self.tweets.set_tweet_score(id, is_good)

    def save_tweet(self, tweet: Tweet):
        return self.tweets.save_tweet(tweet)

    def save_url(self, url):
        return self.links.save_url(url)

    def set_link_predicted_score(self, id, score):
        return self.links.set_link_predicted_score(id, score)

    def set_link_score(self, id, score):
        return self.links.set_link_score(id, score)

    @contextmanager
    def connection(self):
        con = sqlite3.connect(f"{self.filename}.db")
        con.row_factory = sqlite3.Row
        try:
            yield con
        except BaseException as e:
            con.rollback()
            raise e
        else:
            con.commit()
