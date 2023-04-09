from sklearn.feature_extraction.text import TfidfVectorizer

class DataPipeline:
    def __init__(self, options):
        self.options = options
        self.feature_encoder_options = options["feature_encoder"]

        self.tf_idf_encoder_options = {
            "max_features": 100,
            "input":'content',
            "encoding":'utf-8', 
            "decode_error":'replace', 
            "strip_accents":'unicode',
            "lowercase":True, 
            "analyzer":'word', 
            "stop_words":'english',
        }

    def preprocess(self, X):
        return self

    def encode(self, X):
        pass
    
    def fit(self, X_train, X_test, y_train, y_test):
        options = {}
        if self.feature_encoder_options["encoder"] == TfidfVectorizer:
            options = self.tf_idf_encoder_options
        
        for key,value in self.feature_encoder_options.items():
            if key in ["encoder"]:
                continue
            options[key] = value

        encoder = self.feature_encoder_options["encoder"](
            **options,
        )

        norm = self.options["feature_normalizer"]
        if norm is not None:
            norm = self.options["feature_normalizer"]()
            X_train = encoder.fit_transform(list(map(lambda x: norm(x.text), X_train)))
            X_test = encoder.transform(list(map(lambda x: norm(x.text), X_test)))
        else:
            X_train = encoder.fit_transform(list(map(lambda x: x.text, X_train)))
            X_test = encoder.transform(list(map(lambda x: x.text, X_test)))
        return encoder, (X_train, X_test, y_train, y_test)
