from .just_give_me_text.helpers.Metadata import Metadata
import gzip
import gzip
import hashlib
import os
import json

class Cache:
    def save(self, url: str, metadata: Metadata):
        content = json.dumps(metadata)
        with gzip.open(self._get_location(url), 'wb') as f:
            f.write(content.encode())
    
    def load(self, url):
        with gzip.open(self._get_location(url), 'rb') as f:
            return json.loads(f.read())
    
    def _get_location(self, url):
        hash = hashlib.sha256(url.encode()).hexdigest()
        location = os.path.join(
            "~/",
            ".latios",
            "cache",
            hash
        )
        os.makedirs(os.path.dirname(location), exist_ok=True)
        print(location)
        return location
