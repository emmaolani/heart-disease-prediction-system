import math
import pandas as pd
from dataset_service import DATASET
from feature_selection import FEATURE_SELECTION
from sklearn.metrics import precision_score, recall_score, accuracy_score
import numpy as np
import pickle

label_value = ['Age', 'Sex', 'Cp', 'Trestbps', 'Chol', 'Fbs', 'Restecg', 'Thalch', 'Exang', 'Oldpeak', 'Slope',
               'Ca', 'Thal']


class Hpred:
    def __init__(self, inputs, state):
        self.per_pre = []
        self.inputs = inputs
        self.state = state
        self.index = 0
        self.saved_naive_classifier = pickle.load(open('finalize_naive.sav', 'rb+'))
        self.saved_dt_classifier = pickle.load(open('finalize_dt.sav', 'rb+'))
        self.saved_svm = pickle.load(open('finalize_svm.sav', 'rb+'))
        if self.state == 'SVM':
            self.array_values = np.zeros((1, 11))
        else:
            self.array_values = np.zeros((1, 13))

    def check_value_validation(self):
        if self.state == 'Naive Bayes' or self.state == 'Decision Tree':
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

            if self.state == 'Naive Bayes':
                prediction = self.saved_naive_classifier.predict(self.array_values)
                self.per_pre.append(prediction[0])
                self.per_pre.append(None)
                return self.per_pre
            if self.state == 'Decision Tree':
                prediction = self.saved_dt_classifier.predict(self.array_values)
                self.per_pre.append(prediction[0])
                self.per_pre.append(None)
                return self.per_pre

        if self.state == 'SVM':
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
            self.per_pre.append(prediction[0])
            self.per_pre.append(None)
            return self.per_pre

    def check_csv_validation(self, check_per):
        data = pd.read_csv(self.inputs, header=None)
        dataset = DATASET(data)
        dataset.clean_data()
        if self.state == 'Naive Bayes':
            X = dataset.getter_data().iloc[:, 0:13]
            y = dataset.getter_data()['target']
            self.array_values = X.to_numpy()
            prediction = self.saved_naive_classifier.predict(self.array_values)
            self.per_pre.append(prediction)

            if check_per:
                accuracy = accuracy_score(y, prediction)
                accuracy = math.trunc(accuracy * 100)

                precision = precision_score(y, prediction, average='weighted')
                precision = math.trunc(precision * 100)

                recall = recall_score(y, prediction, average='weighted')
                recall = math.trunc(recall * 100)

                per_score = [accuracy, precision, recall]
                self.per_pre.append(per_score)
            else:
                self.per_pre.append(None)

            return self.per_pre

        if self.state == 'Decision Tree':
            X = dataset.getter_data().iloc[:, 0:13]
            y = dataset.getter_data()['target']

            self.array_values = X.to_numpy()
            prediction = self.saved_dt_classifier.predict(self.array_values)

            self.per_pre.append(prediction)

            if check_per:
                accuracy = accuracy_score(y, prediction)
                accuracy = math.trunc(accuracy * 100)

                precision = precision_score(y, prediction, average='weighted')
                precision = math.trunc(precision * 100)

                recall = recall_score(y, prediction, average='weighted')
                recall = math.trunc(recall * 100)

                per_score = [accuracy, precision, recall]
                self.per_pre.append(per_score)
            else:
                self.per_pre.append(None)
            
            return self.per_pre

        if self.state == 'SVM':
            selected_feature = FEATURE_SELECTION(dataset, 11)
            selected_feature.select_feature()

            df = selected_feature.getter()
            X = df.iloc[:, 0:11]
            y = dataset.getter_data()['target']

            self.array_values = X.to_numpy()
            prediction = self.saved_svm.predict(self.array_values)
            self.per_pre.append(prediction)

            if check_per:
                accuracy = accuracy_score(y, prediction)
                accuracy = math.trunc(accuracy * 100)

                precision = precision_score(y, prediction, average='weighted')
                precision = math.trunc(precision * 100)

                recall = recall_score(y, prediction, average='weighted')
                recall = math.trunc(recall * 100)

                per_score = [accuracy, precision, recall]
                self.per_pre.append(per_score)
            else:
                self.per_pre.append(None)

            return self.per_pre


# data = pd.read_csv('processed.cleveland.csv', header=None)
# dataset = DATASET(data)
# dataset.clean_data()
# selected_feature = FEATURE_SELECTION(dataset, 11)
# selected_feature.select_feature()
# df = selected_feature.getter()
# X = df.iloc[:, 0:11]
# y = dataset.getter_data()['target']
# print(X)

# svm_model = SVC(kernel='linear')
# svm_model.fit(X.to_numpy(), y.to_numpy())
#
# pickle.dump(svm_model, open('finalize_svm.sav', 'wb'))
# predict = svm_model.predict(X.to_numpy())

# precision = precision_score(y, predict, average='weighted')
# accuracy = accuracy_score(y, predict)
# accuracy = math.trunc(accuracy * 100)
# print(accuracy, precision)

# self.cf_left_wig.pack_forget()
        # self.cf_right_wig.pack_forget()
        #
        # self.cf_left_wig = Frame(self.canvas_frame_wig, padx=20, pady=26, background='lightgrey')
        # self.cf_right_wig = Frame(self.canvas_frame_wig, padx=20, pady=30, background='lightgrey')
        # self.cf_left_wig.pack(fill=BOTH, expand=True, side='left')
        # self.cf_right_wig.pack(fill=BOTH, expand=True, side='left')

 # for i in range(len(sel_cf_left_label_value)):
        #     Label(self.cf_left_wig,
        #           text=sel_cf_left_label_value[i],
        #           background='lightgrey', font=('sanserif', 12), fg='grey').pack(anchor='w', padx=20, side=TOP)
        #     input_box = Entry(self.cf_left_wig, width=40, border=0)
        #     input_box.pack(fill=X, padx=20, pady=10, ipadx=5, ipady=5, side=TOP)
        #     self.cf_left_label_input.append(input_box)
        #
        # # widget for frame 4
        # for i in range(len(sel_cf_right_label_value)):
        #     Label(self.cf_right_wig,
        #           text=sel_cf_right_label_value[i],
        #           background='lightgrey', font=('sanserif', 11), fg='grey').pack(anchor='w', padx=20, side=TOP)
        #
        #     input_box = Entry(self.cf_right_wig, width=40, border=0)
        #     input_box.pack(fill=X, padx=20, pady=10, ipadx=5, ipady=5, side=TOP)
        #     self.cf_right_label_input.append(input_box)

        # pushing all widget to an array to create the order of changing focus with button or tab