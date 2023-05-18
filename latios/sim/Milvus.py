"""
# Ugh need to install the server https://milvus.io/docs/install_standalone-operator.md

from pymilvus import Collection
from pymilvus import connections
connections.connect(
  alias="default",
  user='username',
  password='password',
  host='localhost',
  port='19530'
)

# Get an existing collection.
collection = Collection("book", connection="default")
# Vector search with time travel
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = collection.search(
  data=[[0.1, 0.2]],
  anns_field="book_intro", 
  param=search_params, 
  limit=10,
)
"""