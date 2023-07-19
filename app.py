import pandas as pd
from service_class.dataset_service import DATASET

data = pd.read_csv("processed.cleveland.csv", header=None)

dataset = DATASET(data)
dataset.clean_data()
print(dataset.getter_data())

