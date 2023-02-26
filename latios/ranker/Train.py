from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBRegressor
from sklearn.metrics import accuracy_score
from ..shared.Model import Model
from ..shared.Config import DATA_WORKER_HOST
from ..shared.Normalizer import Normalizer
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from .GetDataset import get_dataset

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/dataset"
IS_DEV_MODE = True

def get_split_dataset(**kwargs):
    X, y = get_dataset(**kwargs)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42
    )

    options = {
        "max_features": 100,
        "input":'content',
        "encoding":'utf-8', 
        "decode_error":'replace', 
        "strip_accents":'unicode',
        "lowercase":True, 
        "analyzer":'word', 
        "stop_words":'english',
    }
    for key,value in kwargs.items():
        options[key] = value

    tf_idf = TfidfVectorizer(
        **options,
    )
    norm = Normalizer()

    X_train = tf_idf.fit_transform(list(map(lambda x: norm(x.text), X_train)))
    X_test = tf_idf.transform(list(map(lambda x: norm(x.text), X_test)))

    return tf_idf, (X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    best_model = None
    best_tfidf = None
    best_score = 0

    dataset_configs = [
        {
            "max_features":75
        },
        {
            "max_features":100
        },
        {
            "max_features":150
        },
        {
            "max_features":100,
        },
    ]
    for dataset_config in dataset_configs:
        print(dataset_config)
        tf_idf, (X_train, X_test, y_train, y_test) = get_split_dataset(**dataset_config)
        
        models = [
            XGBRegressor(),
            XGBRegressor(tree_method="hist"),
            RandomForestRegressor(max_depth=2, random_state=0),
            RandomForestRegressor(max_depth=8, random_state=0),
            RandomForestRegressor(max_depth=4, random_state=0),
            svm.SVR()
        ]
        for model in models:
            model.fit(X_train, y_train)
            accuracy = accuracy_score(y_test, list(map(lambda x: min(max(round(x), 0), 1), model.predict(X_test))))
            print(f"{model.__class__.__name__} -> accuracy: {accuracy}")

            if best_score < accuracy:
                best_score = accuracy
                best_tfidf = tf_idf
                best_model = model
        print("")
    print(f"Best model accuracy {best_score}")
    Model(
        best_tfidf,
        best_model,
        is_dev=IS_DEV_MODE
    ).save()

