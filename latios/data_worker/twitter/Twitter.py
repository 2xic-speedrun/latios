from abc import ABC, abstractmethod
from ...shared.Tweet import Tweet
from typing import List

class Twitter(ABC):
	@abstractmethod
	def fetch_timeline(self, since_id) -> List[Tweet]:
		pass

