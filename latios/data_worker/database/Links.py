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
                    model_version int nullable,
                    netloc text nullable,
                    added_timestamp text nullable
                );
                """
            )
        """
        with self.database.connection() as con:
            cur = con.cursor()
            try:
                cur.execute(
                    "ALTER TABLE links add column added_timestamp text nullable;"
                )
            except Exception as e:
                print(e)
                pass
        """
        
    def get_all(self, first=None, skip=None, order_by=None, direction=None, last_n_days=None):
        with self.database.connection() as con:
            cur = con.cursor()
            query = SimpleQueryBuilder().select(
                "links"
            )
            if first is not None:
                query.limit(first)
            if skip is not None:
                query.skip(skip)

            if last_n_days is not None:
                assert type(last_n_days) == int or last_n_days.isnumeric()
                query.and_where(
                    # last two days of links
                    f"date('now', '-{last_n_days} days') <= DATETIME(added_timestamp)",
                )

            if order_by is not None:
                #if order_by == "predicted_score":
                #    query.and_where("predicted_score is not null")
                query.order_by(order_by, direction)
            print(str(query))

            all = cur.execute(
                str(query),
                query.args
            ).fetchall()

            return all

    def save_url(self, url):
        url = urllib.parse.unquote(url)
        with self.database.connection() as con:
            cur = con.cursor()
            found = cur.execute("SELECT * from links where url = ?", (url, )).fetchall()
            if len(found):
                return found[0]                
            else:
                cur.execute(
                    'INSERT INTO links (url, added_timestamp) values (?, datetime(\'now\'))', (
                        url,
                    )
                )
            found = cur.execute("SELECT * from links where url = ?", (url, )).fetchall()
            return found[0]

    def set_link_predicted_score(self, id, score):
        print((id, score))
        with self.database.connection() as con:
            cur = con.cursor()
            cur.execute(
                'UPDATE links set predicted_score = ?, model_version=? where id = ?', (
                    score, MODEL_VERSION, id,
                )
            )

    def set_link_score(self, id, is_good):
        with self.database.connection() as con:
            cur = con.cursor()
            score = 1 if is_good else 0
            cur.execute(
                'UPDATE links set score = ? where id = ?', (
                    score, id,
                )
            )

    def save_link_with_id(self, id, netloc=None, predicted_score=None, title=None, description=None):
        with self.database.connection() as con:
            cur = con.cursor()
            update = SimpleQueryBuilder()
            update.update("links")
            update.set_value_if_not_none("netloc", netloc)
            update.set_value_if_not_none("title", title)
            update.set_value_if_not_none("predicted_score", predicted_score)
            update.set_value_if_not_none("description", description)
            update.and_where(
                'id = ?',
                id
            )
            cur.execute(str(update), update.args)
