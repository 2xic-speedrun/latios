from .Database import Database

class KeyValue:
    def __init__(self, database: Database):
        self.database = database

    def get_metadata_key(self, key):
        with self.database.connection() as con:
            cur = con.cursor()
            rows = cur.execute("SELECT * from metadata where key = ?", (key, ))
            rows = rows.fetchall()
            if len(rows) == 0:
                return None
            return rows[0]["value"]

    def set_metadata_key_value(self, key, value):
        with self.database.connection() as con:
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
