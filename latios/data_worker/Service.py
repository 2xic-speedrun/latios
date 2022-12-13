from flask import Flask, request
from .DataWorker import DataWorker
from .Database import Database
from .twitter.HttpTwitter import HttpTwitter
import json

app = Flask(__name__)

@app.route('/fetch')
def fetch():
    data_worker = DataWorker(
        Database("latios"),
        HttpTwitter()
    )
    return str(data_worker.update_timeline())

@app.route('/')
def timeline():
    data_worker = DataWorker(
        Database("latios"),
        HttpTwitter()
    )
    return str(data_worker.get_timeline())

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback = json.loads(request.data)
    Database("latios").give_feedback(
        id=int(feedback["id"]),
        is_good=feedback["is_good"]
    )
    return "OK"

if __name__ == "__main__":
    app.run(port=8081, host='0.0.0.0')

