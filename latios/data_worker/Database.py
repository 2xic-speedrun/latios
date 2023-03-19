import sqlite3
from contextlib import contextmanager
from ..shared.Tweet import Tweet
from typing import List
import json
from ..shared.Config import MODEL_VERSION
from .database.KeyValue import KeyValue
from .database.Tweets import Tweets
from .database.Links import Links
from .database.LinkRelation import LinksRelation

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.key_value = KeyValue(self)
        self.tweets = Tweets(self)
        self.links = Links(self)
        self.link_relation = LinksRelation(self)
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

    def get_tweets(self) -> Tweets:
        return self.tweets

    def get_all_tweets(self,
                since_id=None,
                has_score=None,
                has_predicted_score=None,
                first=None,
                skip=None,
                order_by=None,
                direction=None,
                model_version=None,
                last_n_days=None,
                conversation_id=None,
                screen_name=None,
            ) -> List[Tweet]:
        return self.tweets.get_all(
            since_id=since_id,
            has_score=has_score,
            has_predicted_score=has_predicted_score,
            first=first,
            skip=skip,
            order_by=order_by,
            direction=direction,
            model_version=model_version,
            last_n_days=last_n_days,
            conversation_id=conversation_id,
            screen_name=screen_name,
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

    def save_url(self, url, source=None):
        results = self.links.save_url(url)
        if source is not None:
            self.link_relation.save(
                targetLinkId=results['id'],
                **source,
            )
        return results

    def save_link_with_id(self, id, predicted_score=None, netloc=None, title=None, description=None):
        return self.links.save_link_with_id(
            id=id,
            predicted_score=predicted_score,
            netloc=netloc,
            title=title,
            description=description,
        )

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
