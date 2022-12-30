import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from .VocabEncoder import Vocab
from .GetDataset import get_dataset
import random

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

def train(model, X, y):
    optimizer = torch.optim.Adam(model.parameters())

    for epoch in range(1_000):
        y_pred = model(X)
        loss = F.binary_cross_entropy_with_logits(
            y_pred,
            y
        )
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print((epoch, loss))

    return model

def get_dataset_split():
    X, y = get_dataset()
    X = list(map(lambda x: x.text, X))

    Xy = list(zip(X, y))
    random.shuffle(Xy)

    X = [i[0] for i in Xy]
    y = [i[1] for i in Xy]

    test_size = 0.33

    split = (1 - test_size)
    train_size = int(len(X) * split)

    X_train = X[:train_size]
    y_train = y[:train_size]

    X_test = X[train_size:]
    y_test = y[train_size:]

    return (
        X_train,
        torch.tensor(y_train, dtype=torch.float).reshape((-1, 1)),
        X_test,
        torch.tensor(y_test, dtype=torch.float).reshape((-1, 1))
    )

def test(model, X, y):
    acc = (torch.round(model(X)) == y).sum() / X.shape[0]
    print(f"Accuracy {acc}")
    return acc

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
