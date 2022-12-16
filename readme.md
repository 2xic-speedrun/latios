# Latios
Nice, and simple Tweet aggregator.

I love twitter, but the timeline is a mess (especially in the official app).

Latios is an attempt to solve this by having a model learn your tweet preference, and ranking them higher based on your tweet feedback.

## How to use 
0. `pip3 install -r requirments.txt` and add twitter tokens to `.env`
1. `python3 -m latios.data_worker.Service` starts the data worker (fetches the twitter data, and handles the feedback from the client)
2. `python3 -m latios.client.Service` start the web interface
3. `python3 -m latios.ranker.Service` sets the predicted tweet score.
4. `python3 -m latios.ranker.Train` let's you train a TfIdf model for the feedback you have given in the client.

## TODO
- "Nice to have"
  - Group tweets in thread together
  - i.e https://twitter.com/proofofjake_/status/1603076919800778752

