from .openai_embeddings import get_embeddings
import numpy as np

class OpenAiEmbeddings:
    def __init__(self, model):
        self.model = model

    def fit_transform(self, X):
        output = []
        for i in X:
            output.append(get_embeddings(
                text=i,
                model=self.model,
            )["data"][0]["embedding"])
        return np.asarray(output)
    
    def transform(self, X):
        output = []
        for i in X:
            output.append(get_embeddings(
                text=i,
                model=self.model,
            )["data"][0]["embedding"])
        return np.asarray(output)
