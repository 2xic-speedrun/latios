import tweepy
from dotenv import load_dotenv
import os
from .Twitter import Twitter
from ...shared.Tweet import Tweet

load_dotenv()

class HttpTwitter(Twitter):
	def __init__(self) -> None:
		access_token = os.getenv("TWITTER_TOKEN")
		access_token_secret = os.getenv("TWITTER_TOKEN_SECRET")
		consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
		consumer_key_secret = os.getenv("TWITTER_CONSUMER_KEY_SECRET")

		self.client = tweepy.Client(
			consumer_key=consumer_key,
			consumer_secret=consumer_key_secret,
			access_token=access_token,
			access_token_secret=access_token_secret
		)

		self.tweet_fields = ["author_id", "text",
								"conversation_id", 
								"created_at", 
								"in_reply_to_user_id",
								"referenced_tweets",
								"entities",
								"context_annotations",
								"attachments"]
		self.user_fields = ["username", "profile_image_url"]
		self.expansions = ["referenced_tweets.id.author_id", "entities.mentions.username", "referenced_tweets.id", "in_reply_to_user_id"]

	def fetch_timeline(self, since_id):
		for response in tweepy.Paginator(self.client.get_home_timeline, since_id=since_id, expansions=self.expansions, tweet_fields=self.tweet_fields, user_fields=self.user_fields, max_results=100):
			for tweet in self._convert_tweet_response(response):
				yield tweet

	def _convert_tweet_response(self, response):
		tweets = response.data
		include = response.includes.get("users", [])
		users_mapping = {
			int(user["id"]): user.data for user in include
		}
		if type(tweets) == None:
			return []
		elif type(tweets) != list:
			tweets = [tweets]

		response = []
		for tweet in tweets:
			if tweet is None:
				break
			data = tweet.data
			author_id = data.get("author_id", None)
			if author_id:
				author_id = int(author_id)
				if author_id in users_mapping:
					data["user"] = users_mapping[author_id]
			response.append(Tweet(data))
		return response
