"""
Experimental
"""
import redis
from redis.commands.search.field import VectorField
from redis.commands.search.query import Query
from ..shared.Model import Model
from ..shared.Tweet import Tweet
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List

class Redis:
    def __init__(self) -> None:
        self.r = redis.Redis(host='localhost', port=6379)
        #self.embedding = TfidfVectorizer(
        #    max_features=16
        #)
        self.model = Model.load()
        try:
            schema = VectorField("v", "HNSW", {
                "TYPE": "FLOAT32", 
                "DIM": 100, 
                "DISTANCE_METRIC": "L2"
            }),
            self.r.ft().create_index(schema)
        except Exception as e:
            print(e)

    def fit(self, tweets: List[Tweet]):
        #self.embedding.fit(tweets)
        pass

    def add_tweet(self, tweet: Tweet):
        embedding = self.model._get_embedding(tweet.text).astype(np.float32).toarray()[0].tobytes()
        self.r.hset(str(tweet.id), "v", embedding)

    def get_sim(self, tweet):
        embedding = self.model._get_embedding(tweet.text).astype(np.float32).toarray()[0].tobytes()
        q = Query("*=>[KNN 3 @v $vec]").return_field("__v_score").dialect(2)
        return self.r.ft().search(q, query_params={
            "vec": embedding
        })
