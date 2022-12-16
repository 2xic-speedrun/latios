from abc import ABC, abstractmethod
from typing import List
import sqlite3

class Database(ABC):
	@abstractmethod
	def connection(self) -> sqlite3.Connection:
		pass

