from ..shared.Model import Model
from ..shared.Tweet import Tweet
import numpy as np
from typing import List
import chromadb
from collections import namedtuple

class Chroma:
    def __init__(self) -> None:
        self.client = chromadb.Client()
        self.model = Model.load()
        self.collection = self.client.create_collection(name="my_collection")

    def fit(self, tweets: List[Tweet]):
        #self.embedding.fit(tweets)
        pass

    def add_tweet(self, tweet: Tweet):
        embedding = self.model._get_embedding(tweet.text).astype(np.float32).toarray().tolist()[0]
        self.collection.add(
            embeddings=[
                embedding
            ],
            documents=[tweet.text],
            ids=[tweet.id]
        )

    def get_sim(self, tweet):
        embedding = self.model._get_embedding(tweet.text).astype(np.float32).toarray().tolist()[0]
        try:
            output = self.collection.query(
                query_embeddings=embedding,
                n_results=4
            )["ids"]
            doc = namedtuple('doc', ['id'])
            return list(map(lambda x: doc(x), output[0]))
        except Exception as e:
            print(e)
            return []
