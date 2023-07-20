import pandas as pd
from model.dataset_service import DATASET
from model.kfold_service import KFOLD

data = pd.read_csv("processed.cleveland.csv", header=None)

dataset = DATASET(data)
dataset.clean_data()

kfold = KFOLD(dataset)
io = kfold.balance_data_set()
print(io)


