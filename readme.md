# Latios
Nice, and simple feed aggregator.

I love twitter, but the timeline is a mess (especially in the official app).
Hackernews is a great link aggregator, but I only care about certain articles, and the same is true for Reddit.

Latios is an attempt to aggregate and rank feeds by having a model learn your preference, and ranking links and tweets higher based on your feedback.

## How to use 
0. `pip3 install -r requirements.txt` and add twitter tokens to `.env`
1. `python3 -m latios.data_worker.Service` starts the data worker (fetches the twitter data, and handles the feedback from the client)
2. `python3 -m latios.client.Service` start the web interface
3. `python3 -m latios.ranker.Service` sets the predicted tweet score.
4. `python3 -m latios.ranker.Train` let's you train a TfIdf model for the feedback you have given in the client.
