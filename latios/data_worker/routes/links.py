from ..Database import Database
from ...shared.Config import DB_NAME
from flask import Blueprint, request
import json
import sqlite3

link_blueprint = Blueprint('links', __name__)

@link_blueprint.route('/links')
def fetch():
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")
    direction = request.args.get("direction", "desc")

    database = Database(DB_NAME)
    links = database.links.get_all(
        first=first,
        skip=skip,
        order_by=order_by,
        direction=direction
    )
    print(links)
    def map_dict(item: sqlite3.Row):
        return {
            key: item[key] for key in item.keys()
        }

    return json.dumps(
        list(map(lambda x: map_dict(x), links))
    )

@link_blueprint.route('/save_url', methods=["POST"])
def save_url():
    url = request.args.get('url', None)
    assert url is not None
    Database(DB_NAME).save_url(
        url
    )
    return "OK"

@link_blueprint.route('/set_predict_link_score', methods=["POST"])
def score_url():
    data = json.loads(request.data)
    for entry in data:
        id = entry.get('id', None)
        score = entry.get('score', None)
        Database(DB_NAME).set_link_predicted_score(
            id, score
        )
    return "OK"
