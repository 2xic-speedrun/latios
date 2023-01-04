import torch
import torch.nn.functional as F
import random
from ..GetDataset import get_dataset
from optimization_utils.channel.WeightsSender import SendModel
from optimization_utils.channel.ParameterSender import SendParameters

X, y = None, None

def train(model, X, y):
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    model.train()

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
            SendModel("http://localhost:8080", model, epoch)
            SendParameters("http://localhost:8080", loss=loss.item())            

    return model

def get_dataset_split():
    global X, y 
    if X is None:
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
