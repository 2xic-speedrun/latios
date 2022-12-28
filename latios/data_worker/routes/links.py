from ..Database import Database
from flask import Blueprint, request, current_app, jsonify
import json
from ..helper.map_dict import map_dict
from ...shared.Cache import Cache

link_blueprint = Blueprint('links', __name__)


@link_blueprint.route('/links')
def fetch():
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")
    direction = request.args.get("direction", "desc")

    database = Database(current_app.config["DB_NAME"])
    links = database.links.get_all(
        first=first,
        skip=skip,
        order_by=order_by,
        direction=direction
    )
    print(links)

    return json.dumps(
        list(map(lambda x: map_dict(x), links))
    )

@link_blueprint.route('/save_url', methods=["POST"])
def save_url():
    url = request.args.get('url', None)
    assert url is not None
    return jsonify(map_dict(Database(current_app.config["DB_NAME"]).save_url(
        url
    )))


@link_blueprint.route('/save_link_with_id', methods=["POST"])
def predict_score_url():
    data = json.loads(request.data)
    for entry in data:
        id = entry.get('id', None)
        predicted_score = entry.get('score', None)
        title = entry.get('title', None)
        netloc = entry.get('netloc', None)
        description = entry.get('description', None)
        assert id is not None
        Database(current_app.config["DB_NAME"]).save_link_with_id(
            id=id,
            predicted_score=predicted_score,
            title=title,
            netloc=netloc,
            description=description,
        )
    return "OK"


@link_blueprint.route('/link_feedback', methods=["POST"])
def score_url():
    data = json.loads(request.data)
    id = data.get('id', None)
    score = data.get('is_good', None)
    assert type(score) != None
    assert type(id) != None

    Database(current_app.config["DB_NAME"]).set_link_score(
        id, score
    )
    return "OK"

@link_blueprint.route('/link_text', methods=["GET"])
def link_text():
    data = request.args
    url = data.get('url', None)

    if url is None:
        return "No url is set"
    results = Cache().load(url)
    if results is None:
        return "No url cache found"
    return results.get("text", None)
