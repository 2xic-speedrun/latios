from flask import Flask, request, jsonify, current_app
from .Database import Database
from ..shared.Config import DB_NAME
from .routes.tweets import tweet_blueprint
from .routes.links import link_blueprint

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

if __name__ == "__main__":
    app.config.update({
        "DB_NAME": DB_NAME,
    })
    app.run(port=8081, host='0.0.0.0')
