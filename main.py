from tkinter import *
import pandas as pd
from model.dataset_service import DATASET
from model.feature_selection import FEATURE_SELECTION
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import precision_score, recall_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import numpy as np


def main_pro(loc, root):
    N = 13
    min_N = 4

    data = pd.read_csv(loc, header=None)
    dataset = DATASET(data)
    dataset.clean_data()

    metrics = []

    while N >= min_N:
        selected_feature = FEATURE_SELECTION(dataset, N)
        selected_feature.select_feature()

        df = selected_feature.getter()

        X, y = df.iloc[:, 0:N], df['target']

        naive = GaussianNB()
        svm_model = SVC(kernel='linear')
        dt_classifier = DecisionTreeClassifier(random_state=42)

        cv_accuracy_scores_N = cross_val_score(naive, X, y, cv=10, scoring='accuracy')
        cv_accuracy_scores_S = cross_val_score(svm_model, X, y, cv=10, scoring='accuracy')

        cv_predictions_S = cross_val_predict(svm_model, X, y, cv=10)
        cv_predictions_N = cross_val_predict(naive, X, y, cv=10)

        precision_N = precision_score(y, cv_predictions_N, average='weighted')
        recall_N = recall_score(y, cv_predictions_N, average='weighted')

        precision_S = precision_score(y, cv_predictions_S, average='weighted')
        recall_S = recall_score(y, cv_predictions_S, average='weighted')

        accuracy_scores_DT = cross_val_score(dt_classifier, X, y, cv=10, scoring='accuracy')
        cv_predictions_DT = cross_val_predict(dt_classifier, X, y, cv=10)
        precision_DT = precision_score(y, cv_predictions_DT, average='weighted')
        recall_DT = recall_score(y, cv_predictions_DT, average='weighted')

        # print("Mean Cross-validation Accuracy for Naive:", cv_accuracy_scores_N.mean())
        # print("precision for Naive:", precision_N)
        # print("recall Naive:", recall_N)
        #
        # print("Mean Cross-validation Accuracy for SVM:", cv_accuracy_scores_S.mean())
        # print("precision for SVM:", precision_S)
        # print("recall SVM:", recall_S)
        #
        # print("Mean accuracy DT:", np.mean(accuracy_scores_DT))
        # print("precision for DT:", precision_DT)
        # print("recall DT:", recall_DT)

        N -= 1

    print(metrics)
    return metrics
