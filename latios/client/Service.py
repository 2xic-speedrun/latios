import requests
from ..shared.Tweet import Tweet
from flask import Flask, render_template, request, url_for, flash, redirect
from ..shared.Config import DATA_WORKER_HOST
from ..shared.Link import Link

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"
app = Flask(__name__, template_folder='template')

def get_tweets(
    skip,
    first,
    order_by
):
    url = DATA_WORKER_URL + "?" + f"skip={skip}&first={first}&order_by={order_by}"
    return list(map(lambda x: Tweet(x["tweet"], x['is_good']), requests.get(url).json()))

def get_links(
    skip,
    first,
    order_by
):
    url = DATA_WORKER_URL + "links?" + f"skip={skip}&first={first}&order_by={order_by}"
    return list(list(map(lambda x: Link(**x), requests.get(url).json())))

@app.route('/')
def tweets():
    path = 'index.html'
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")

    return render_template(path, tweets=get_tweets(skip=skip, first=first, order_by=order_by))

@app.route('/links')
def links():
    path = 'links.html'
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")

    return render_template(path, links=get_links(skip=skip, first=first, order_by=order_by))

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(port=8080, host='0.0.0.0')
