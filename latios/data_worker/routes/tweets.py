from flask import Flask, request, jsonify, current_app
from ..DataWorker import DataWorker
from ..Database import Database
from ..twitter.HttpTwitter import HttpTwitter
import json
from ...shared.Config import MODEL_VERSION
from ..query.Not import Not
from flask import Blueprint

tweet_blueprint = Blueprint('tweets', __name__)

@tweet_blueprint.route('/fetch')
def fetch():
    data_worker = DataWorker(
        Database(current_app.config["DB_NAME"]),
        HttpTwitter()
    )
    return str(data_worker.update_timeline())

@tweet_blueprint.route('/set_predict_score', methods=["POST"])
def set_predicted_score():
    scores = json.loads(request.data)
    dataset = Database(current_app.config["DB_NAME"])
    for i in scores:
        dataset.set_tweet_predicted_score(i["id"], i["score"])
    return "OK"


@tweet_blueprint.route('/predict_score_queue')
def predict_score_queue():
    dataset = Database(current_app.config["DB_NAME"]).get_all_tweets(
        #   has_predicted_score=False,
        model_version=Not(MODEL_VERSION),
        first=10
    )
    return json.dumps(list(map(lambda x: x.__dict__(), dataset)))

@tweet_blueprint.route('/')
def timeline():
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")
    direction = request.args.get('direction', "DESC")
    last_n_days = request.args.get('last_n_days', None)
    conversation_id = request.args.get('conversation_id', None)
    screen_name = request.args.get('screen_name', None)
    has_score = request.args.get('has_score', None)

    if has_score is not None:
        has_score = has_score == "true"

    data_worker = DataWorker(
        Database(current_app.config["DB_NAME"]),
        HttpTwitter()
    )
    return str(data_worker.get_timeline(
        skip,
        first,
        order_by,
        direction,
        last_n_days,
        conversation_id,
        screen_name,
        has_score=has_score,
    ))


@tweet_blueprint.route('/feedback', methods=['POST'])
def feedback():
    feedback = json.loads(request.data)
    Database(current_app.config["DB_NAME"]).set_tweet_score(
        id=int(feedback["id"]),
        is_good=feedback["is_good"]
    )
    return "OK"

@tweet_blueprint.route('/users', methods=['GET'])
def users():
    users = Database(current_app.config["DB_NAME"]).get_users()
    return json.dumps(users)
