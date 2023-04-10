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
from .DataPipeline import DataPipeline
from .features.OpenAiEmbeddings import OpenAiEmbeddings
import matplotlib.pyplot as plt
import os

#DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/dataset"
DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/dataset?INCLUDE_LINKS=True"
IS_DEV_MODE = True


if __name__ == "__main__":
    X, y = get_dataset()

    X_train_original, X_test_original, y_train_original, y_test_original = train_test_split(
        X, y, test_size=0.33, random_state=42
    )

    best_model = None
    best_tfidf = None
    best_score = 0

    model_pipeline_configs = {
        "tf_idf": [
            {
                "feature_encoder":{
                    "max_features":75,
                    "encoder": TfidfVectorizer,
                },
                "feature_normalizer": Normalizer,
            },
            {
                "feature_encoder":{
                    "max_features":100,
                    "encoder": TfidfVectorizer,
                },
                "feature_normalizer": Normalizer,
            },
            {
                "feature_encoder":{
                    "max_features":150,
                    "encoder": TfidfVectorizer,
                },
                "feature_normalizer": Normalizer,
            },
            {
                "feature_encoder":{
                    "max_features":100,
                    "encoder": TfidfVectorizer,
                },
                "feature_normalizer": Normalizer,
            },
        ],
        "tf_idf raw": [
            {
                "feature_encoder":{
                    "max_features":100,
                    "encoder": TfidfVectorizer,
                },
                "feature_normalizer": None,
            },
        ],
        "open_ai":[
            {
                "feature_encoder":{
                    "encoder": OpenAiEmbeddings,
                    "model": "text-embedding-ada-002"
                },
                "feature_normalizer": Normalizer,
            }
        ],
        "open_ai_raw": [
            {
                "feature_encoder":{
                    "encoder": OpenAiEmbeddings,
                    "model": "text-embedding-ada-002",
                },
                "feature_normalizer": None,
            }
        ]
    }
    results = {}
    for base_config_name in model_pipeline_configs:
        best_local_config_score = 0
        best_local_config_string = None
        for dataset_config in model_pipeline_configs[base_config_name]:
            print(dataset_config)
            tf_idf, (X_train, X_test, y_train, y_test) = DataPipeline(dataset_config).fit(
                X_train_original, X_test_original, y_train_original, y_test_original
            )
            
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
                best_local_config_score = max(best_local_config_score, (accuracy * 100))
                best_local_config_string = f"{model.__class__.__name__} + {base_config_name}"
            print("")
        results[best_local_config_string] = best_local_config_score
    print(f"Best model accuracy {best_score}")
    Model(
        best_tfidf,
        best_model,
        is_dev=IS_DEV_MODE
    ).save()

    config_name = list(results.keys())
    values = list(results.values())
    fig = plt.figure(figsize = (10, 5))
    plt.bar(config_name, values,width = 0.4)
    plt.xlabel("Config name")
    plt.ylabel("Accuracy %")
    plt.ylim([50, 100])
    plt.title("Results")
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "ResultsRankerTrain.png"
    )
    plt.savefig(path)
