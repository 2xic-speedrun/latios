# Latios
Nice, and simple Tweet aggregator.

I love twitter, but the timeline is a mess.

I just want to read good tweets, not bad tweets.

## How to use 
0. `pip3 install -r requirments.txt` and add twitter tokens to `.env`
1. `python3 -m latios.data_worker.Service` starts the data worker (fetches the twitter data, and handles the feedback from the client)
2. `python3 -m latios.client.Service` start the web interface
3. (soon) `python3 -m latios.ranker.Service` sets the tweet score.
4. (soon) `python3 -m latios.ranker.Train` let's you train a TfIdf model for the feedback you have given in the client.

## TODO
- Add the ranker service, but need data first. 
- "Nice to have"
  - Option to view tweet on twitter
  - Group tweets in thread together
  - Show full link, and not twitter shortened link
  - 
