import unittest
from .Database import Database
from .Tweet import Tweet
import tempfile


class TestingDatabase(unittest.TestCase):
    def test_save_get(self):
        file = tempfile.NamedTemporaryFile()
        database = Database(file.name)
        database.save(Tweet(
            {
                "id": 10,
                "text": "test tweet"
            }
        ))
        tweets = database.get_all(since_id=0)
        assert len(tweets) == 1
        assert tweets[0].id == 10

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


if __name__ == '__main__':
    unittest.main()
