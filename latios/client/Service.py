import requests
from ..shared.Tweet import Tweet
from flask import Flask, render_template, request, url_for, flash, redirect
from ..shared.Config import DATA_WORKER_HOST
from ..shared.Link import Link

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"
app = Flask(__name__, template_folder='template')


def get_url_text(url):
    return requests.get(DATA_WORKER_URL + f"link_text?url={url}").text

def get_tweets(
    skip,
    first,
    order_by,
    last_n_days,
    conversation_id=None,
    direction=None
):
    url = DATA_WORKER_URL + "?" + \
        f"skip={skip}&first={first}&order_by={order_by}"
    if last_n_days is not None:
        url += f"&last_n_days={last_n_days}"

    if conversation_id is not None:
        url += f"&conversation_id={conversation_id}"

    if direction is not None:
        url += f"&direction={direction}"

   # print(url)
    return list(map(lambda x: Tweet(x["tweet"], x['is_good']), requests.get(url).json()))


def get_links(
    skip,
    first,
    order_by
):
    url = DATA_WORKER_URL + "links?" + \
        f"skip={skip}&first={first}&order_by={order_by}"
    return list(list(map(lambda x: Link(**x), requests.get(url).json())))


@app.route('/')
def tweets():
    path = 'index.html'
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")
    last_n_days = request.args.get('last_n_days', 2)

    return render_template(path, tweets=get_tweets(skip=skip, first=first, order_by=order_by, last_n_days=last_n_days))


@app.route('/links')
def links():
    path = 'links.html'
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")

    return render_template(path, links=get_links(skip=skip, first=first, order_by=order_by))

@app.route('/link_text')
def link_text():
    url = request.args.get('url', None)
    words = get_url_text(url).split(" ")

    batch_size = 128

    return "<br><br>".join([
        " ".join(words[i:i+batch_size]) for i in range(0, len(words), batch_size)    
    ])

@app.route('/conversation')
def conversation():
    path = 'index.html'
    conversation_id = int(request.args.get('conversation_id', 0))

    return render_template(path, tweets=get_tweets(skip=0, first=1_00, order_by="id", direction="asc", last_n_days=None, conversation_id=conversation_id))

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(port=8080, host='0.0.0.0')
