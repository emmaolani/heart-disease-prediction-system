from sklearn.feature_selection import SelectKBest, chi2
import pandas as pd


class FEATURE_SELECTION:
    def __init__(self, raw_dataset, num):
        self.raw_dataset = raw_dataset.getter_data()
        self.selected_features_df = -1
        self.x = self.raw_dataset.drop('target', axis=1)
        self.y = self.raw_dataset['target']
        self.num_top_features = num

    def select_feature(self):
        selector = SelectKBest(score_func=chi2, k=self.num_top_features)
        x_new = selector.fit_transform(self.x, self.y)
        selected_indices = selector.get_support(indices=True)
        selected_column_names = self.x.columns[selected_indices]

        self.selected_features_df = pd.DataFrame(x_new, columns=selected_column_names)
        self.selected_features_df['target'] = self.y.values

    def getter(self):
        return self.selected_features_df





