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
				"CREATE TABLE IF NOT EXISTS tweets(id INTEGER PRIMARY KEY, json varchar, score int nullable);"
			)
			cur.execute(
				"CREATE TABLE IF NOT EXISTS metadata (key varchar PRIMARY KEY, value int);"
			)

	def get_all(self, since_id) -> List[Tweet]:
		with self.connection() as con:
			cur = con.cursor()
			since_id =  since_id if since_id is not None else 0

			all = cur.execute("SELECT * from tweets where id > ?", (
				since_id,
			))
			return list(map(lambda x: Tweet(json.loads(x['json'])), all))

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

	def save(self, tweet: Tweet):
		with self.connection() as con:
			cur = con.cursor()
			rows = cur.execute("SELECT * from tweets where id = ?", (tweet.id, ))
			results = rows.fetchone()

			if results is None:
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