from .GetDataset import get_dataset
from ..shared.Normalizer import Normalizer

X, y = get_dataset()

norm = Normalizer()
with open(".debug.txt", "w") as file:
    for i in X:
        noisy = i.text.replace("\n", " ")
        normalized = norm(noisy)
        file.write(noisy)
        file.write("\n")
        file.write(normalized)
        file.write("\n")
        file.write("\n")
        