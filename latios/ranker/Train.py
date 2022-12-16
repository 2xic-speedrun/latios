from ..shared.Tweet import Tweet
import requests
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBRegressor
from sklearn.metrics import accuracy_score
from .Model import Model
from ..shared.Config import DATA_WORKER_HOST

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

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42
    )

    tf_idf = TfidfVectorizer(
        max_features=100
    )
    X_train = tf_idf.fit_transform(list(map(lambda x: x.text, X_train)))
    X_test = tf_idf.transform(list(map(lambda x: x.text, X_test)))

    return tf_idf, (X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    tf_idf, (X_train, X_test, y_train, y_test) = get_dataset()
    
    reg = XGBRegressor()
    reg.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, list(map(lambda x: round(x), reg.predict(X_test))))
    print(f"accuracy: {accuracy}")

    Model(
        tf_idf,
        reg
    ).save()

