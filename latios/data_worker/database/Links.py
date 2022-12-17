from .Database import Database
import urllib
from ..query.SimpleQueryBuilder import SimpleQueryBuilder
from ...shared.Config import MODEL_VERSION

class Links:
    def __init__(self, database: Database):
        self.database = database

        with self.database.connection() as con:
            cur = con.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    url varchar NOT NULL UNIQUE,
                    score int nullable, 
                    predicted_score REAL nullable,
                    model_version int nullable
                );
                """
            )

    def get_all(self, first=None, skip=None, order_by=None, direction=None):
        with self.database.connection() as con:
            cur = con.cursor()
            query = SimpleQueryBuilder().select(
                "links"
            )    
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

            return all

    def save_url(self, url):
        url = urllib.parse.unquote(url)
        with self.database.connection() as con:
            cur = con.cursor()
            cur.execute(
                'INSERT INTO links (url) values (?)', (
                    url,
                )
            )

    def set_link_predicted_score(self, id, score):
        print((id, score))
        with self.database.connection() as con:
            cur = con.cursor()
            cur.execute(
                'UPDATE links set predicted_score = ?, model_version=? where id = ?', (
                    score, MODEL_VERSION, id,
                )
            )
