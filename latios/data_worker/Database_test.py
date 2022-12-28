import unittest
from .Database import Database
from ..shared.Tweet import Tweet
import tempfile
from .query.Not import Not


class TestingDatabase(unittest.TestCase):
    def test_save_get(self):
        file = tempfile.NamedTemporaryFile()
        database = Database(file.name)
        database.save_tweet(Tweet(
            {
                "id": 10,
                "text": "test tweet"
            }
        ))
        tweets = database.get_all(since_id=0)
        assert len(tweets) == 1
        assert tweets[0].id == 10

        database.set_tweet_score(10, True)
        tweets = database.get_all(since_id=0)
        assert tweets[0].is_good == True

    def test_metadata_set_get(self):
        file = tempfile.NamedTemporaryFile()
        database = Database(file.name)
        database.set_metadata_key_value(
            "last_id",
            10
        )
        metadata_value = database.get_metadata_key("last_id")
        assert metadata_value == 10

        metadata_value = database.get_metadata_key("none")
        assert metadata_value == None

        database.set_metadata_key_value(
            "last_id",
            20
        )
        metadata_value = database.get_metadata_key("last_id")
        assert metadata_value == 20

    def test_get_not(self):
        file = tempfile.NamedTemporaryFile()
        database = Database(file.name)
        database.save_tweet(Tweet(
            {
                "id": 10,
                "text": "test tweet"
            }
        ))
        tweets = database.get_all()
        assert len(tweets) == 1

        tweets = database.get_all(
            model_version=Not(-1)
        )

        assert len(tweets) == 1

    def test_should_correctly_update(self):
        file = tempfile.NamedTemporaryFile()
        database = Database(file.name)
        results = database.save_url(
            "http://test.com/"
        )
        assert results["id"] == 1
        links = database.links.get_all(first=1)
        link = links[0]
        database.save_link_with_id(
            id=link["id"],
            netloc="test"
        )
        links = database.links.get_all(first=1)
        assert links[0]["netloc"] == "test"

if __name__ == '__main__':
    unittest.main()
