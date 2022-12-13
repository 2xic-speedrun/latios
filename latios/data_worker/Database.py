import sqlite3
from contextlib import contextmanager
from .Tweet import Tweet
from typing import List
import json

class Database:
    def __init__(self, filename):
        self.filename = filename
        self._setupDb()

    def _setupDb(self):
        with self.connection() as con:
            cur = con.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS tweets(id INTEGER PRIMARY KEY, json varchar, score int nullable)")

    def get_all(self) -> List[Tweet]:
        with self.connection() as con:
            cur = con.cursor()
            all = cur.execute("SELECT * from tweets")
            return list(map(lambda x: Tweet(json.loads(x['json'])), all))

    def save(self, tweet: Tweet):
        with self.connection() as con:
            cur = con.cursor()
            cur.execute(
                'INSERT INTO tweets (id, json) values (?, ?)', (
                    tweet.id, str(tweet),
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
