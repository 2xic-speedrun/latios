from .Database import Database
from ..query.SimpleQueryBuilder import SimpleQueryBuilder

"""
TODO:
Link relation should be able to give a boost to a url
-> Count is a simplistic metric, but could maybe work
-> Source tweet or link is also important
"""

class LinksRelation:
    def __init__(self, database: Database):
        self.database = database

        with self.database.connection() as con:
            cur = con.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS link_relation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    urlId int,
                    linkId int nullable,
                    tweetId int nullable,
                    
                    constraint only_one_value 
                    check 
                    (        
                        (
                            linkId is null or tweetId is null
                        ) 
                        and 
                        not (
                            tweetId is null and linkId is null
                        )
                    )        
                );
                """
            )
            cur.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS uq_link_relation ON link_relation(urlId, linkId, tweetId);
                """    
            )
        
    def save(self, targetLinkId, tweetId=None, linkId=None):
        with self.database.connection() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO link_relation (urlId, linkId, tweetId) VALUES (?, ?, ?)",
                (targetLinkId, tweetId, linkId)
            )

    def get_all(self, first=None, skip=None, order_by=None):
        with self.database.connection() as con:
            cur = con.cursor()
            query = SimpleQueryBuilder().select(
                "link_relation"
            )
            if first is not None:
                query.limit(first)
            if skip is not None:
                query.skip(skip)

            all = cur.execute(
                str(query),
                query.args
            ).fetchall()

            return all
