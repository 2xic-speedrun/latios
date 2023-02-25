from abc import ABC, abstractmethod
from typing import Union
from ..helpers.Metadata import Metadata

class Html(ABC):
	@abstractmethod
	def fetch_metadata(self, url) -> Union[Metadata, None]:
		pass
