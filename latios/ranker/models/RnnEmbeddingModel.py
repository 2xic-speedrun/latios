import torch
import torch.nn as nn
import torch.nn.functional as F
from .VocabEncoder import Vocab
from .helper.train_torch_model import train, test, get_dataset_split

torch.manual_seed(1)

class LinearLayer(nn.Module):
    def __init__(self, in_x, out_x):
        super(LinearLayer, self).__init__()
        self.f =  nn.Sequential(*(
            nn.Linear(in_x, out_x),
            nn.Sigmoid()
        ))

    def forward(self, x):
        return self.f(x)

class RnnEmbeddingModel(nn.Module):
    def __init__(self,
                 embedding_dim,
                 linear_shape,
                 vocab: Vocab
                ):
        super(RnnEmbeddingModel, self).__init__()

        self.word_embeddings = nn.Embedding(
            vocab.vocab_size,
            embedding_dim,
            padding_idx=vocab.PADDING_IDX
        )
        self.first_linear = linear_shape[0][0]
        self.lstm = nn.LSTM(
            embedding_dim * 280,
            self.first_linear,
        )
        self.score = nn.Sequential(*(
            LinearLayer(*i)
            for i in linear_shape
        ))

    def forward(self, X):
        hidden = (torch.randn(1, 1, self.first_linear),
                  torch.randn(1, 1, self.first_linear))

        X = self.word_embeddings(X)
        inputs = X.view(X.shape[0], 1, -1)
        hidden = (torch.randn(1, 1, self.first_linear), torch.randn(1, 1, self.first_linear))
        out, hidden = self.lstm(inputs, hidden)

        row_indices = torch.arange(0, X.size(0)).long()
        normalized_tensor = out[row_indices, :, :]
        normalized_tensor = torch.mean(normalized_tensor, dim=1)

        return self.score(normalized_tensor)

if __name__ == "__main__":

    model_structure = [
        [
            (256, 128),
            (128, 1)
        ],
        [
            (128, 64),
            (64, 1)
        ],
        [
            (512, 256),
            (256, 128),
            (128, 1)
        ]
    ]

    (
        X_train,
        y_train,
        X_test,
        y_test
    ) =  get_dataset_split()

    vocab = Vocab().fit(X_train)
    docs = vocab.transform(X_train)
    
    for index, linear_shape in enumerate(model_structure):
        model = RnnEmbeddingModel(
            embedding_dim=8,
            vocab=vocab,
            linear_shape=linear_shape
        )
        print(model)

        model = train(model, docs, y_train)
        model.eval()
        acc = test(model, vocab.transform(X_test), y_test)

        with open("embedding", "a") as file:
            file.write(f"{index} -> {acc}\n")
