import pandas as pd
import pickle
from dataset_service import DATASET
from feature_selection import  FEATURE_SELECTION
from sklearn.svm import SVC
import numpy as np

label_value = ['Age', 'Sex', 'Cp', 'Trestbps', 'Chol', 'Fbs', 'Restecg', 'Thalch', 'Exang', 'Oldpeak', 'Slope',
               'Ca', 'Thal']


class Hpred:
    def __init__(self, inputs, state):
        self.inputs = inputs
        self.state = state
        self.index = 0
        self.saved_naive_classifier = pickle.load(open('finalize_naive.sav', 'rb+'))
        self.saved_dt_classifier = pickle.load(open('finalize_dt.sav', 'rb+'))
        self.saved_svm = pickle.load(open('finalize_svm.sav', 'rb+'))
        if self.state == 'S':
            self.array_values = np.zeros((1, 11))
        else:
            self.array_values = np.zeros((1, 13))

    def check_value_validation(self):
        if self.state == 'N' or self.state == 'D':
            for key, value in self.inputs.items():
                try:
                    val = float(value)
                except ValueError:
                    return ['val error', key, self.index]
                else:
                    if key == 'Age' and val in np.arange(1, 90):
                        self.array_values[0][self.index] = val
                    elif key == 'Sex' and val in np.arange(0, 2):
                        self.array_values[0][self.index] = val
                    elif key == 'Cp' and val in np.arange(1, 6):
                        self.array_values[0][self.index] = val
                    elif key == 'Trestbps' and val in np.arange(94, 202):
                        self.array_values[0][self.index] = val
                    elif key == 'Chol' and val in np.arange(126, 566):
                        self.array_values[0][self.index] = val
                    elif key == 'Fbs' and val in np.arange(0, 2):
                        self.array_values[0][self.index] = val
                    elif key == 'Restecg' and val in np.arange(0, 3):
                        self.array_values[0][self.index] = val
                    elif key == 'Thalch' and val in np.arange(71, 203):
                        self.array_values[0][self.index] = val
                    elif key == 'Exang' and val in np.arange(0, 2):
                        self.array_values[0][self.index] = val
                    elif key == 'Oldpeak' and val in np.round(np.arange(0, 6, 0.1, dtype=float), decimals=1):
                        self.array_values[0][self.index] = val
                    elif key == 'Slope' and val in np.arange(1, 4):
                        self.array_values[0][self.index] = val
                    elif key == 'Ca' and val in np.arange(0, 4):
                        self.array_values[0][self.index] = val
                    elif key == 'Thal' and val in (3.0, 6.0, 7.0):
                        self.array_values[0][self.index] = val
                    else:
                        return ['not in range', key, self.index]
                    self.index += 1

            if self.state == 'N':
                prediction = self.saved_naive_classifier.predict(self.array_values)
                return prediction
            if self.state == 'D':
                prediction = self.saved_dt_classifier.predict(self.array_values)
                return prediction

        if self.state == 'S':
            for key, value in self.inputs.items():
                try:
                    val = float(value)
                except ValueError:
                    return ['val error', key, self.index]
                else:
                    if key == 'Age' and val in np.arange(1, 90):
                        self.array_values[0][self.index] = val
                    elif key == 'Cp' and val in np.arange(1, 6):
                        self.array_values[0][self.index] = val
                    elif key == 'Trestbps' and val in np.arange(94, 202):
                        self.array_values[0][self.index] = val
                    elif key == 'Chol' and val in np.arange(126, 566):
                        self.array_values[0][self.index] = val
                    elif key == 'Restecg' and val in np.arange(0, 3):
                        self.array_values[0][self.index] = val
                    elif key == 'Thalch' and val in np.arange(71, 203):
                        self.array_values[0][self.index] = val
                    elif key == 'Exang' and val in np.arange(0, 2):
                        self.array_values[0][self.index] = val
                    elif key == 'Oldpeak' and val in np.round(np.arange(0, 6, 0.1, dtype=float), decimals=1):
                        self.array_values[0][self.index] = val
                    elif key == 'Slope' and val in np.arange(1, 4):
                        self.array_values[0][self.index] = val
                    elif key == 'Ca' and val in np.arange(0, 4):
                        self.array_values[0][self.index] = val
                    elif key == 'Thal' and val in (3.0, 6.0, 7.0):
                        self.array_values[0][self.index] = val
                    else:
                        return ['not in range', key, self.index]
                    self.index += 1
            prediction = self.saved_svm.predict(self.array_values)
            return prediction

    def check_csv_validation(self):

        data = pd.read_csv(self.inputs, header=None)
        dataset = DATASET(data)
        dataset.clean_data()
        if self.state == 'N':
            X = dataset.getter_data().iloc[:, 0:13]
            self.array_values = X.to_numpy()
            prediction = self.saved_naive_classifier.predict(self.array_values)
            return prediction
        if self.state == 'D':
            X = dataset.getter_data().iloc[:, 0:13]
            self.array_values = X.to_numpy()
            prediction = self.saved_dt_classifier.predict(self.array_values)
            return prediction
        if self.state == 'S':
            selected_feature = FEATURE_SELECTION(dataset, 11)
            selected_feature.select_feature()
            df = selected_feature.getter()
            X = df.iloc[:, 0:11]
            self.array_values = X.to_numpy()
            prediction = self.saved_svm.predict(self.array_values)
            return prediction


# file_name_sv = 'finalize_svm.sav'
# data = pd.read_csv('processed.cleveland.csv', header=None)
# dataset = DATASET(data)
# dataset.clean_data()
#
# selected_feature = FEATURE_SELECTION(dataset, 13)
# selected_feature.select_feature()
# df = selected_feature.getter()
#
# X, y = df.iloc[:, 0:11], df['target']
# xa = X.to_numpy()
# ya = y.to_numpy()
#
# SVM = SVC(kernel='linear')
#
# SVM.fit(xa, ya)
# pickle.dump(SVM, open(file_name_sv, 'wb'))


# label_value_S = ['Age', 'Cp', 'Trestbps', 'Chol', 'Restecg', 'Thalch', 'Exang', 'Oldpeak', 'Slope', 'Ca', 'Thal']
# n = np.array([[63, 1, 145, 1, 2, 150, 0, 2.3, 3, 0, 6]])
