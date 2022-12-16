from ..Database import Database
from ...shared.Config import DB_NAME
from flask import Blueprint, request
import json

link_blueprint = Blueprint('links', __name__)

@link_blueprint.route('/links')
def fetch():
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")

    database = Database(DB_NAME)
    links = database.links.get_all(
        first=first,
        skip=skip,
        order_by=order_by,
    )
    print(links)
    return json.dumps(
        list(map(lambda x: x['url'], links))
    )
