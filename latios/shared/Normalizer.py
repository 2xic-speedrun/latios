import re

class Normalizer:
    def __init__(self) -> None:
        pass

    def __call__(self, text) -> str:
        return self.forward(text)

    def forward(self, text):
        mappers = [
            self._remove_url,
            self._remove_at,
            self._make_ascii
        ]
        for i in mappers:
            text = i(text)
        return text


    def _remove_url(self, text):
        return re.sub(r'^https?:\/\/.*[\r\n]*', '<link>', text, flags=re.MULTILINE)

    def _remove_at(self, text):
        return re.sub(r'@\S+', '@user', text, flags=re.MULTILINE)

    def _make_ascii(self, text):
        return text.encode("ascii", errors="ignore").decode()

