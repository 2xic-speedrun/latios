import sqlite3
from flask import Flask
from .DataWorker import DataWorker
from .Database import Database
from .twitter.HttpTwitter import HttpTwitter

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


if __name__ == "__main__":
    app.run(port=8081)

