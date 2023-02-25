import requests
from ..shared.Tweet import Tweet
from flask import Flask, render_template, request, url_for, flash, redirect
from ..shared.Config import DATA_WORKER_HOST
from ..shared.Link import Link
from ..shared.Model import Model

DATA_WORKER_URL = f"http://{DATA_WORKER_HOST}:8081/"
app = Flask(__name__, template_folder='template')

model = Model.load()

def get_url_text(url):
    return requests.get(DATA_WORKER_URL + f"link_text?url={url}").text

def get_tweets(
    skip,
    first,
    order_by,
    last_n_days,
    conversation_id=None,
    direction=None,
    screen_name=None,
    has_score=None
):
    """
        TODO: Use a cleaner url builder.
    """
    url = DATA_WORKER_URL + "?" + \
        f"skip={skip}&first={first}&order_by={order_by}"
    if last_n_days is not None:
        url += f"&last_n_days={last_n_days}"

    if conversation_id is not None:
        url += f"&conversation_id={conversation_id}"
    
    if screen_name is not None:
        url += f"&screen_name={screen_name}"

    if direction is not None:
        url += f"&direction={direction}"
    
    if has_score is not None:
        url += f"&has_score={has_score}"

    return list(map(lambda x: Tweet(x["tweet"], x['is_good']), requests.get(url).json()))


def get_links(
    skip,
    first,
    order_by,
    last_n_days,
    direction
):
    url = DATA_WORKER_URL + "links?" + \
        f"skip={skip}&first={first}&order_by={order_by}&last_n_days={last_n_days}&direction={direction}"
    return list(list(map(lambda x: Link(**x), requests.get(url).json())))

@app.route('/')
def tweets():
    path = 'index.html'
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "predicted_score")
    last_n_days = request.args.get('last_n_days', 1)
    has_score = request.args.get('has_score', False)

    return render_template(path, tweets=get_tweets(skip=skip, first=first, order_by=order_by, last_n_days=last_n_days, has_score=has_score))


@app.route('/links')
def links():
    path = 'links.html'
    skip = int(request.args.get('skip', 0))
    first = int(request.args.get('first', 10))
    order_by = request.args.get('order_by', "id")
    direction = request.args.get("direction", "desc")
    last_n_days = request.args.get('last_n_days', 1)

    return render_template(path, links=get_links(
        skip=skip, 
        first=first, 
        order_by=order_by,
        direction=direction,
        last_n_days=last_n_days,
    ))

@app.route('/link_text')
def link_text():
    url = request.args.get('url', None)
    words = get_url_text(url).split(" ")

    batch_size = 128

    text = [
        " ".join(words[i:i+batch_size]) 
        for i in range(0, len(words), batch_size)    
    ]
    text_score = [
        (i, model(i), ("green" if model(i) > 0.7 else "red")) for i in text
    ]

    return "<br>".join(
        f"<p style=\"color: {color} \">{text} ({score})</p>" 
        for (text, score, color) in text_score
    )

@app.route('/conversation')
def conversation():
    path = 'index.html'
    conversation_id = int(request.args.get('conversation_id', 0))

    return render_template(path, tweets=get_tweets(skip=0, first=1_00, order_by="id", direction="asc", last_n_days=None, conversation_id=conversation_id))

@app.route('/user')
def user():
    path = 'index.html'
    screen_name = request.args.get('screen_name', None)

    return render_template(path, tweets=get_tweets(
            skip=0, 
            first=1_00, 
            order_by="id", 
            direction="asc", 
            last_n_days=None, 
            conversation_id=None,
            screen_name=screen_name,
        )
    )

@app.route('/users')
def users():
    url = DATA_WORKER_URL + "users"
    users = requests.get(url).json()
    users = list(map(lambda x: f"<a href=\"/user?screen_name={x['screen_name']}\">{x['screen_name']}</a> sum_predicted_score : {x['sum_predicted_score']}", users))
    return "<br>".join(users)    

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(port=8080, host='0.0.0.0')
