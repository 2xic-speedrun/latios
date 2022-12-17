from ..shared.Tweet import Tweet
import requests
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBRegressor
from sklearn.metrics import accuracy_score
from ..shared.Model import Model
from ..shared.Config import DATA_WORKER_HOST
from ..shared.Normalizer import Normalizer
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/dataset"

def get_dataset():
    tweets = list(map(lambda x: Tweet(x["tweet"], x['is_good']), requests.get(DATA_WORKER_URL).json()))

    good_tweets = list(filter(lambda x: x.is_good == True, tweets))
    bad_tweets = list(filter(lambda x: x.is_good == False, tweets))

    size = min(len(good_tweets), len(bad_tweets))

    good_tweets = good_tweets[:size]
    bad_tweets = bad_tweets[:size]

    X = good_tweets + bad_tweets
    y = [1, ] * size + [0, ] * size

    print(f"Training on {size*2} samples")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42
    )

    tf_idf = TfidfVectorizer(
        max_features=150,
        input='content',
        encoding='utf-8', 
        decode_error='replace', 
        strip_accents='unicode',
        lowercase=True, 
        analyzer='word', 
        stop_words='english',
    )
    norm = Normalizer()

    print(norm(X_train[0].text), X_train[0].text)
    print(norm(X_train[10].text), X_train[10].text)

    X_train = tf_idf.fit_transform(list(map(lambda x: norm(x.text), X_train)))
    X_test = tf_idf.transform(list(map(lambda x: norm(x.text), X_test)))

    return tf_idf, (X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    tf_idf, (X_train, X_test, y_train, y_test) = get_dataset()
    
    models = [
        XGBRegressor(),
        XGBRegressor(tree_method="hist"),
        RandomForestRegressor(max_depth=2, random_state=0),
        RandomForestRegressor(max_depth=8, random_state=0),
        svm.SVR()
    ]
    best_model = None
    best_score = 0
    for model in models:
        model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, list(map(lambda x: round(x), model.predict(X_test))))
        print(f"accuracy: {accuracy}")
        if best_score < accuracy:
            best_score = accuracy
            best_model = model

    Model(
        tf_idf,
        best_model
    ).save()

