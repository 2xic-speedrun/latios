from flask import Flask, request, jsonify
from ..DataWorker import DataWorker
from ..Database import Database
from ..twitter.HttpTwitter import HttpTwitter
import json
from ...shared.Config import DB_NAME, MODEL_VERSION
from ..query.Not import Not
from flask import Blueprint

tweet_blueprint = Blueprint('tweets', __name__)

@tweet_blueprint.route('/fetch')
def fetch():
    data_worker = DataWorker(
        Database(DB_NAME),
        HttpTwitter()
    )
    return str(data_worker.update_timeline())


@tweet_blueprint.route('/set_predict_score', methods=["POST"])
def set_predicted_score():
    scores = json.loads(request.data)
    dataset = Database(DB_NAME)
    for i in scores:
        dataset.set_tweet_predicted_score(i["id"], i["score"])
    return "OK"


@tweet_blueprint.route('/predict_score_queue')
def predict_score_queue():
    dataset = Database(DB_NAME).get_all(
        #   has_predicted_score=False,
        model_version=Not(MODEL_VERSION),
        first=10
    )
    return json.dumps(list(map(lambda x: x.__dict__(), dataset)))


@tweet_blueprint.route('/dataset')
def dataset():
    dataset = Database(DB_NAME).get_all(
        has_score=True
    )
    return json.dumps(list(map(lambda x: x.__dict__(), dataset)))

@tweet_blueprint.route('/')
def timeline():
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")
    direction = request.args.get('direction', "DESC")

    data_worker = DataWorker(
        Database(DB_NAME),
        HttpTwitter()
    )
    return str(data_worker.get_timeline(
        skip,
        first,
        order_by,
        direction,
    ))


@tweet_blueprint.route('/feedback', methods=['POST'])
def feedback():
    feedback = json.loads(request.data)
    Database(DB_NAME).set_tweet_score(
        id=int(feedback["id"]),
        is_good=feedback["is_good"]
    )
    return "OK"
