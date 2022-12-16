import sqlite3
from contextlib import contextmanager
from ..shared.Tweet import Tweet
from typing import List
import json
from .query.SimpleQueryBuilder import SimpleQueryBuilder
from .query.Not import Not
from ..shared.Config import MODEL_VERSION


class Database:
    def __init__(self, filename):
        self.filename = filename
        self._setupDb()

    def _setupDb(self):
        with self.connection() as con:
            cur = con.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS tweets(id INTEGER PRIMARY KEY, json varchar, score int nullable, predicted_score int nullable, model_version int nullable);"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS metadata (key varchar PRIMARY KEY, value int);"
            )

        with self.connection() as con:
            try:
                cur.execute(
                    "ALTER TABLE tweets ADD COLUMN predicted_score int nullable;")
            except Exception as e:
                pass

        with self.connection() as con:
            try:
                cur.execute(
                    "ALTER TABLE tweets ADD COLUMN model_version int nullable;")
            except Exception as e:
                pass

    def get_all(self, since_id=None, has_score=None, has_predicted_score=None, first=None, skip=None, order_by=None, direction=None, model_version=None) -> List[Tweet]:
        with self.connection() as con:
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

    def get_metadata_key(self, key):
        with self.connection() as con:
            cur = con.cursor()
            rows = cur.execute("SELECT * from metadata where key = ?", (key, ))
            rows = rows.fetchall()
            if len(rows) == 0:
                return None
            return rows[0]["value"]

    def set_metadata_key_value(self, key, value):
        with self.connection() as con:
            cur = con.cursor()
            rows = cur.execute("SELECT * from metadata where key = ?", (key, ))
            rows = rows.fetchall()

            if len(rows):
                cur.execute(
                    'UPDATE metadata set value = ? where key = ?', (
                        value, key,
                    )
                )
            else:
                cur.execute(
                    'INSERT INTO metadata (key, value) values (?, ?)', (
                        key, value,
                    )
                )

    def set_predicted_score(self, id, score):
        with self.connection() as con:
            cur = con.cursor()
            cur.execute(
                'UPDATE tweets set predicted_score = ?, model_version=? where id = ?', (
                    score, MODEL_VERSION, id,
                )
            )

    def set_score(self, id, is_good):
        with self.connection() as con:
            cur = con.cursor()
            score = 1 if is_good else 0
            cur.execute(
                'UPDATE tweets set score = ? where id = ?', (
                    score, id,
                )
            )

    def save(self, tweet: Tweet):
        with self.connection() as con:
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
