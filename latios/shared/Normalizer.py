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
            self._make_ascii,
            self._make_lower_case,
            self._remove_noisy_chars,
            self._remove_numbers,
        ]
        for i in mappers:
            text = i(text)
        return text

    def _remove_numbers(self, text):
        return re.sub("\d+", "<num>", text)

    def _remove_noisy_chars(self, text):
        for i in [",", ".", ":", '"', "'", "!"]:
            text = text.replace(i, " ")
        return re.sub(' +', ' ', text.strip())

    def _make_lower_case(self, text):
        return text.lower()

    def _remove_url(self, text):
        for i in text.split(" "):
            if "http" in i:
                text = text.replace(i, "<link>")
        return text

    def _remove_at(self, text):
        return re.sub(r'@\S+', '@user', text, flags=re.MULTILINE)

    def _make_ascii(self, text):
        return text.encode("ascii", errors="ignore").decode()
