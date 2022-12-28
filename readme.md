# Latios
Nice, and simple Tweet aggregator.

I love twitter, but the timeline is a mess (especially in the official app).

Latios is an attempt to solve this by having a model learn your tweet preference, and ranking them higher based on your tweet feedback.


## Evolution
Looks like Latios is evolving, Twitter is a great aggregator for other content, and not just tweets. Having a nice interface for links, and filtered links is even better. 

Moving forward various data sources might be added, and Latios will aggregate both tweets and various links.

One of the next datasources I'm thinking of adding is something like Hackernews / Reddit.

## How to use 
0. `pip3 install -r requirments.txt` and add twitter tokens to `.env`
1. `python3 -m latios.data_worker.Service` starts the data worker (fetches the twitter data, and handles the feedback from the client)
2. `python3 -m latios.client.Service` start the web interface
3. `python3 -m latios.ranker.Service` sets the predicted tweet score.
4. `python3 -m latios.ranker.Train` let's you train a TfIdf model for the feedback you have given in the client.
