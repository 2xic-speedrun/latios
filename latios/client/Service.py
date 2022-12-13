import requests
from ..shared.Tweet import Tweet
from flask import Flask, render_template, request, url_for, flash, redirect
import os

DATA_WORKER_URL = "http://localhost:8081/"
app = Flask(__name__, template_folder='template')


def get_tweets():
    return list(map(lambda x: Tweet(x["tweet"], x['is_good']), requests.get(DATA_WORKER_URL).json()))


@app.route('/')
def timeline():
    path = 'index.html'
    skip = int(request.args.get('skip', 0))
    first = 10

    return render_template(path, tweets=get_tweets()[skip:skip + first])


if __name__ == "__main__":
    app.run(port=8080)
