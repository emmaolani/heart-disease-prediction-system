import numpy as np


class DATASET:
    def __init__(self, data):
        self.data = data
        self.columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope',
                   'ca',
                   'thal', 'target']

    def setter(self, data):
        self.data = data

    def getter_data(self):
        return self.data

    def __getter_column(self):
        return self.columns

    def __add_columns(self):
        nc_dataset = self.data
        columns = self.__getter_column()
        nc_dataset.columns = columns
        self.setter(nc_dataset)

    def __get_null_val(self):
        df = self.data
        null_val = np.where(df == '?')
        return null_val

    def __get_value_to_replace(self, null):
        temp_df = self.data
        for i in range(len(null[0])):
            temp_df = temp_df.drop(null[0][i])

        value = np.array([])

        for j in range(len(null[1])):
            min_value = temp_df.iloc[:, null[1][j]].min()
            value = np.append(value, min_value)

        return value

    def __add_missing_value(self, nul_val, rep_val):
        df = self.data
        for i in range(len(rep_val)):
            df.iat[nul_val[0][i], nul_val[1][i]] = rep_val[i]

        self.setter(df)

    def __process_target(self):
        df = self.data
        df.loc[df['target'] > 1, 'target'] = 1
        self.setter(df)

    def clean_data(self):
        self.__add_columns()
        null_val = self.__get_null_val()
        replace_array = self.__get_value_to_replace(null_val)
        self.__add_missing_value(null_val, replace_array)
        self.__process_target()



