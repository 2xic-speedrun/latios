from abc import ABC, abstractmethod
from typing import Union
from ..helpers.Metadata import Metadata

class YouTube(ABC):
	@abstractmethod
	def fetch_transcript(self, url) -> Union[Metadata, None]:
		pass
