import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from .VocabEncoder import Vocab
from .helper.train_torch_model import train, test, get_dataset_split

torch.manual_seed(1)

class AttentionLayer(nn.Module):
    def __init__(self, size_in, size_out):
        super().__init__()
        #self.size_in, self.size_out = size_in, size_out

        self.q = nn.Linear(size_in, size_out, bias=False)
        self.k = nn.Linear(size_in, size_out, bias=False)
        self.v = nn.Linear(size_in, size_out, bias=False)
        #self.w = nn.Linear(size_out, size_out, bias=False)

    def forward(self, x):
        dot_attention = self.attention(
            torch.sigmoid(self.q(x)), 
            torch.sigmoid(self.k(x)), 
            torch.sigmoid(self.v(x))
        )
        return dot_attention

    def attention(self, q: torch.nn.Linear, k: torch.nn.Linear, v: torch.nn.Linear) -> torch.Tensor:
        results = torch.softmax(
            q @ k.T
            /
            k.shape[0],
            dim=1
        )
        return results @ v

class LinearLayer(nn.Module):
    def __init__(self, in_x, out_x):
        super(LinearLayer, self).__init__()
        self.f =  nn.Sequential(*(
         #   nn.Linear(in_x, out_x),
            AttentionLayer(in_x, out_x),
            nn.Sigmoid()
        ))

    def forward(self, x):
        return self.f(x)

        
class PositionEmbeddingModel(nn.Module):
    def __init__(self,
                 embedding_dim,
                 linear_shape,
                 vocab: Vocab
                ):
        super(PositionEmbeddingModel, self).__init__()

        self.word_embeddings = nn.Embedding(
            vocab.vocab_size,
            embedding_dim,
            padding_idx=vocab.PADDING_IDX
        )
        self.first_linear = linear_shape[0][0]

        self.mapper_layer = LinearLayer(
            280 * embedding_dim,
            self.first_linear
        )

        self.score = nn.Sequential(*(
            LinearLayer(*i)
            for i in linear_shape
        ))

    def forward(self, X):
        X = self.word_embeddings(X)
        X = X.view(X.shape[0], -1)
    #  print(X.shape)
        X = self.mapper_layer(X)
        return self.score(X)

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
        model = PositionEmbeddingModel(
            embedding_dim=8,
            vocab=vocab,
            linear_shape=linear_shape
        )
        print(model)

        model = train(model, docs, y_train)
        model.eval()
        acc = test(model, vocab.transform(X_test), y_test)

        print(index, acc)

     #   with open("embedding", "a") as file:
      #      file.write(f"{index} -> {acc}\n")
