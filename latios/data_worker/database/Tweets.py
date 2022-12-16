from .Database import Database
from ..query.SimpleQueryBuilder import SimpleQueryBuilder
from ..query.Not import Not
from ...shared.Tweet import Tweet
import json
from ...shared.Config import MODEL_VERSION
from typing import List

class Tweets:
    def __init__(self, database: Database):
        self.database = database

    def get_all(self, since_id=None, has_score=None, has_predicted_score=None, first=None, skip=None, order_by=None, direction=None, model_version=None) -> List[Tweet]:
        with self.database.connection() as con:
            cur = con.cursor()
            query = SimpleQueryBuilder().select(
                "tweets"
            )

            if since_id is not None:
                query.and_where(
                    f"id > {since_id}"
                )
            if has_score is not None:
                if has_score == True:
                    query.and_where(
                        f"score is not null"
                    )
                else:
                    query.and_where(
                        f"score is null"
                    )
            if has_predicted_score is not None:
                if has_predicted_score == True:
                    query.and_where(
                        f"predicted_score is not null"
                    )
                else:
                    query.and_where(
                        f"predicted_score is null"
                    )

            if model_version is not None:
                if type(model_version) == int:
                    query.and_where(
                        "model_version = ?",
                        model_version
                    )
                elif isinstance(model_version, Not):
                    query.and_where(
                        f"(model_version != ? or model_version is null)",
                        model_version.value
                    )
                else:
                    raise Exception("Unknown")

            if first is not None:
                query.limit(first)
            if skip is not None:
                query.skip(skip)
            if order_by is not None:
                query.order_by(order_by, direction)

            all = cur.execute(
                str(query),
                query.args
            ).fetchall()

            return list(map(lambda tweet: Tweet(
                tweet_object=json.loads(tweet['json']), is_good=tweet['score']), all)
            )
        
    def set_tweet_predicted_score(self, id, score):
        with self.database.connection() as con:
            cur = con.cursor()
            cur.execute(
                'UPDATE tweets set predicted_score = ?, model_version=? where id = ?', (
                    score, MODEL_VERSION, id,
                )
            )

    def set_tweet_score(self, id, is_good):
        with self.database.connection() as con:
            cur = con.cursor()
            score = 1 if is_good else 0
            cur.execute(
                'UPDATE tweets set score = ? where id = ?', (
                    score, id,
                )
            )

    def save_tweet(self, tweet: Tweet):
        with self.database.connection() as con:
            cur = con.cursor()
            rows = cur.execute(
                "SELECT * from tweets where id = ?", (tweet.id, ))
            results = rows.fetchone()

            if results is None:
                cur.execute(
                    'INSERT INTO tweets (id, json) values (?, ?)', (
                        tweet.id, json.dumps(tweet.json),
                    )
                )
