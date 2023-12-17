from flask import Flask, request, jsonify, current_app
from .Database import Database
from ..shared.Config import DB_NAME
from .routes.tweets import tweet_blueprint
from .routes.links import link_blueprint
import json
from ..shared.Cache import Cache

app = Flask(__name__)
app.register_blueprint(tweet_blueprint)
app.register_blueprint(link_blueprint)

@app.route('/key_value', methods=["GET"])
def get_key_value():
    key = request.args.get('key', None)
    assert key is not None
    value = Database(current_app.config["DB_NAME"]).get_metadata_key(
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
    value = Database(current_app.config["DB_NAME"]).set_metadata_key_value(
        key,
        value
    )
    return "OK"

@app.route('/dataset')
def dataset():
    INCLUDE_LINKS = bool(request.args.get('INCLUDE_LINKS', False))

    database = Database(current_app.config["DB_NAME"])
    tweet_dataset = database.get_all_tweets(
        has_score=True
    )
    tweet_dicts = list(map(lambda x: x.__dict__(), tweet_dataset))

    links = database.links.get_all(
        has_score=True,
        is_downloaded=True
    )
    # TODO: Just make the dataset consistent and move form tweet to text field
    link_dicts = []
    if INCLUDE_LINKS:
        link_dicts = list(map(lambda x: {
            "tweet": Cache().load(x["url"])["text"],
            "is_good": x["score"],
            "is_tweet": False,
            "url": x["url"],
        } if Cache().load(x["url"]) is not None else None, links))
        link_dicts = list(filter(lambda x: x is not None, link_dicts))

    dataset = tweet_dicts + link_dicts

    return json.dumps(dataset)

if __name__ == "__main__":
    app.config.update({
        "DB_NAME": DB_NAME,
    })
    app.run(port=8081, host='0.0.0.0')
