import torch
from ..shared.Normalizer import Normalizer

class Vocab:
    def __init__(self) -> None:
        self.word_idx = {}
        self.idx_word = {}

        self.PADDING_IDX = self.add_word("<PAD>")
        self.UNKNOWN_IDX = self.add_word("<UNKNOWN>")

    def add_word(self, word):
        idx = len(self.word_idx)
        self.word_idx[word] = idx
        self.idx_word[idx] = word
        return idx

    def get_idx(self, word):
        return self.word_idx.get(word, self.UNKNOWN_IDX)

    def fit(self, docs):
        for i in docs:
            i = Normalizer()(i)
            words = i.split(" ")
            for j in words:
                self.add_word(j)

        return self
        
    def transform(self, docs):
        max_len = 0
        docs_idx = []
        for i in docs:
            i = Normalizer()(i)
            words = i.split(" ")
            doc = []
            for j in words:
                doc.append(
                    self.get_idx(j)
                )
            docs_idx.append(doc)
            max_len = max(len(doc), max_len)

        # max tweet length
        tensor = torch.zeros((len(docs), 280), dtype=torch.long)
        for index, i in enumerate(docs_idx):
            tensor[index, :len(i)] = torch.tensor(i)
        return tensor

    @property
    def vocab_size(self):
        return len(self.word_idx) + 1
