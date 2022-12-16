from flask import Flask, request, jsonify
from .DataWorker import DataWorker
from .Database import Database
from .twitter.HttpTwitter import HttpTwitter
import json
from ..shared.Config import DB_NAME, MODEL_VERSION
from .query.Not import Not

app = Flask(__name__)


@app.route('/fetch')
def fetch():
    data_worker = DataWorker(
        Database(DB_NAME),
        HttpTwitter()
    )
    return str(data_worker.update_timeline())


@app.route('/set_predict_score', methods=["POST"])
def set_predicted_score():
    scores = json.loads(request.data)
    dataset = Database(DB_NAME)
    for i in scores:
        dataset.set_tweet_predicted_score(i["id"], i["score"])
    return "OK"


@app.route('/predict_score_queue')
def predict_score_queue():
    dataset = Database(DB_NAME).get_all(
        #   has_predicted_score=False,
        model_version=Not(MODEL_VERSION),
        first=10
    )
    return json.dumps(list(map(lambda x: x.__dict__(), dataset)))


@app.route('/dataset')
def dataset():
    dataset = Database(DB_NAME).get_all(
        has_score=True
    )
    return json.dumps(list(map(lambda x: x.__dict__(), dataset)))


@app.route('/key_value', methods=["GET"])
def get_key_value():
    key = request.args.get('key', None)
    assert key is not None
    value = Database(DB_NAME).get_metadata_key(
        key
    )
    return jsonify({
        "value": value
    })


@app.route('/key_value', methods=["POST"])
def set_key_value():
    key = request.args.get('key', None)
    value = request.args.get('value', None)
    assert key is not None and value is not None
    value = Database(DB_NAME).set_metadata_key_value(
        key,
        value
    )
    return "OK"


@app.route('/save_url', methods=["POST"])
def save_url():
    url = request.args.get('url', None)
    assert url is not None
    Database(DB_NAME).save_url(
        url
    )
    return "OK"


@app.route('/')
def timeline():
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")

    data_worker = DataWorker(
        Database(DB_NAME),
        HttpTwitter()
    )
    return str(data_worker.get_timeline(
        skip,
        first,
        order_by,
    ))


@app.route('/feedback', methods=['POST'])
def feedback():
    feedback = json.loads(request.data)
    Database(DB_NAME).set_tweet_score(
        id=int(feedback["id"]),
        is_good=feedback["is_good"]
    )
    return "OK"


if __name__ == "__main__":
    app.run(port=8081, host='0.0.0.0')
