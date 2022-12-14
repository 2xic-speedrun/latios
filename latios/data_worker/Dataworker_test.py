import unittest
from .Database import Database
from ..shared.Tweet import Tweet
from .twitter.MockTwitter import MockTwitter
import tempfile
from .DataWorker import DataWorker

class TestingDataWorker(unittest.TestCase):
    def test_save_get(self):
        file = tempfile.NamedTemporaryFile()
        database = Database(file.name)
        twitter = MockTwitter([
            Tweet({
                "id": 5,
                "text": "test"
            })
        ])
        data_worker = DataWorker(
            database=database,
            twitter=twitter
        )
        database.set_metadata_key_value(
            data_worker.last_synchronized_timeline_tweet,
            0
        )
        assert 1 == data_worker.update_timeline()
        assert 0 == data_worker.update_timeline()

if __name__ == '__main__':
    unittest.main()
