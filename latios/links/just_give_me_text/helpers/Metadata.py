from typing_extensions import TypedDict
from typing import Union

Metadata = TypedDict('Metadata', {'title': str, 'netloc': str, 'text': str, 'links': Union[str, None]})
