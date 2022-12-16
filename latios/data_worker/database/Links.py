from .Database import Database
import urllib

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
                    predicted_score REAL nullable
                );
                """
            )


    def save_url(self, url):
        url = urllib.parse.unquote(url)
        with self.database.connection() as con:
            cur = con.cursor()
            cur.execute(
                'INSERT INTO links (url) values (?)', (
                    url
                )
            )
