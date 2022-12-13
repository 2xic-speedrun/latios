import unittest
from .Database import Database
from .Tweet import Tweet
import tempfile


class TestingDatabase(unittest.TestCase):
    def test_split(self):
        file = tempfile.NamedTemporaryFile()
        database = Database(file.name)
        database.save(Tweet(
            {
                "id": 10,
                "text": "test tweet"
            }
        ))
        tweets = database.get_all()
        assert len(tweets) == 1
        assert tweets[0].id == 10


if __name__ == '__main__':
    unittest.main()
