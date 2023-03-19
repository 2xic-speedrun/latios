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

        with self.database.connection() as con:
            cur = con.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tweets(
                    id INTEGER PRIMARY KEY, 
                    json varchar, 
                    score int nullable, 
                    predicted_score REAL nullable, 
                    model_version int nullable,
                    added_timestamp text nullable,
                    conversation_id INTEGER nullable,
                    screen_name varchar nullable
                );
                """
            )
       # with self.database.connection() as con:
       #     cur = con.cursor()
       #     cur.execute("ALTER TABLE tweets add column screen_name varchar nullable;")

    def get_all(self, since_id=None, has_score=None, has_predicted_score=None, first=None, skip=None, order_by=None, direction=None, model_version=None, last_n_days=None, conversation_id=None, screen_name=None) -> List[Tweet]:
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

            if conversation_id is not None:
                query.and_where(
                    "conversation_id = ?",
                    conversation_id, 
                )
            if screen_name is not None:
                query.and_where(
                    "screen_name = ?",
                    screen_name, 
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

            if last_n_days is not None:
                assert type(last_n_days) == int or last_n_days.isnumeric()
                query.and_where(
                    # last two days of tweets
                    f"date('now', '-{last_n_days} days') <= DATETIME(added_timestamp)",
                )

            if first is not None:
                query.limit(first)
            if skip is not None:
                query.skip(skip)
            if order_by is not None:
                query.order_by(order_by, direction)

            print((
                str(query),
                query.args
            ))

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
                    'INSERT INTO tweets (id, json, added_timestamp, conversation_id, screen_name) values (?, ?, datetime(\'now\'), ?, ?)', (
                        tweet.id, json.dumps(tweet.json), tweet.conversation_id, tweet.username,
                    )
                )

    def group_users_by_field(self, field):
        group_by = "sum_predicted_score"
        if field != "score":
            group_by = "sum_score"
            
        with self.database.connection() as con:
            cur = con.cursor()
            sql = [
                "SELECT screen_name, sum(predicted_score) as \"sum_predicted_score\", sum(score) as \"sum_score\" from tweets",
                "where screen_name is not null",
                "group by screen_name",
                f"order by {group_by} desc",
                "limit 100"
            ]
            sql = " ".join(sql)
          #  print(sql)
            rows = cur.execute(sql, ())
            results = rows.fetchall()
         #   print(dict(results[0]))
            return list(map(dict, results))
