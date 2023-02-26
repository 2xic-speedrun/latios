import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from .Normalizer import Normalizer

class Model:
    def __init__(self, tf_idf, model, is_dev=False) -> None:
        self.model = model
        self.tf_idf: TfidfVectorizer = tf_idf
        self.is_dev = is_dev

    @property
    def feature_encoder_name(self):
        name = ""
        if self.is_dev:
            name += "dev_"
        return name + "vectorizer.pk"

    @property
    def model_name(self):
        name = ""
        if self.is_dev:
            name += "dev_"
        return name + "model.pk"

    def save(self):
        if self.is_dev:
            print("Saving dev model")
        with open(self.feature_encoder_name, 'wb') as fp:
            pickle.dump(self.tf_idf, fp)
        with open(self.model_name, 'wb') as fp:
            pickle.dump(self.model, fp)

    @staticmethod
    def load(is_dev=False):
        tf_idf = None
        model = None
        return Model(
            tf_idf=tf_idf,
            model=model,
            is_dev=is_dev,
        )._load()
    
    def _load(self):
        with open(self.feature_encoder_name, 'rb') as fp:
            self.tf_idf = pickle.load(fp)
        with open(self.model_name, 'rb') as fp:
            self.model = pickle.load(fp)
        return self
    
    def __call__(self, text):
        if type(text) == str:
            text = Normalizer()(text)
            transformed = self.tf_idf.transform([text])
            return self.model.predict(transformed)[0]
        else:
            raise Exception("Not handled")
