import pandas as pd
from model.dataset_service import DATASET
from model.kfold_service import KFOLD
from model.feature_selection import FEATURE_SELECTION

data = pd.read_csv("processed.cleveland.csv", header=None)

dataset = DATASET(data)
dataset.clean_data()

selected_feature = FEATURE_SELECTION(dataset, 6)
selected_feature.select_feature()

kfold = KFOLD(selected_feature.getter())
kfold.balance_data_set()
kfold.five_kfold()

# print(data)



