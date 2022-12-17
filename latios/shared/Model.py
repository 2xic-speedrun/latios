import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from .Normalizer import Normalizer

class Model:
    def __init__(self, tf_idf, model) -> None:
        self.model = model
        self.tf_idf: TfidfVectorizer = tf_idf

    def save(self):
        with open('vectorizer.pk', 'wb') as fp:
            pickle.dump(self.tf_idf, fp)
        with open('model.pk', 'wb') as fp:
            pickle.dump(self.model, fp)

    @staticmethod
    def load():
        tf_idf = None
        model = None
        with open('vectorizer.pk', 'rb') as fp:
            tf_idf = pickle.load(fp)
        with open('model.pk', 'rb') as fp:
            model = pickle.load(fp)
        return Model(
            tf_idf=tf_idf,
            model=model
        )
    
    def __call__(self, text):
        if type(text) == str:
            text = Normalizer()(text)
            transformed = self.tf_idf.transform([text])
            return self.model.predict(transformed)[0]
        else:
            raise Exception("Not handled")
