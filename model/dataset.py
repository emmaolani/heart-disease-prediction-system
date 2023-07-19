import numpy as np


class DATASET:
    def __init__(self):
        self.data = []
        self.columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope',
                   'ca',
                   'thal', 'target']

    def setter(self, data):
        self.data = data

    def getter_data(self):
        return self.data

    def getter_column(self):
        return self.columns
