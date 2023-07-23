from model.model_service import LOGISTIC_REGRESSION_MODEL
import numpy as np


class KFOLD:
    def __init__(self, old_dataset):
        self.k = 5
        self.old_dataset = old_dataset
        self.pos = [0, 0]
        self.partition = int(len(old_dataset.to_numpy()) / 5)
        self.new_dataset = np.zeros((303, old_dataset.shape[1]))
        self.new_index = 0

    def __check_ratio_of_class(self):
        class_counts = self.old_dataset['target'].value_counts()
        total_samples = len(self.old_dataset)
        class_percentages = class_counts / total_samples * 100
        return class_percentages.to_numpy()

    def balance_data_set(self):
        per = np.trunc(self.__check_ratio_of_class())
        num_neg_par = int((per[0] * self.partition) / 100)
        num_pos_par = int((per[1] * self.partition) / 100)
        old_df = self.old_dataset.to_numpy()
        old_df = old_df.astype(float)
        total_num_col = len(old_df[0]) - 1

        for i in range(self.k):
            non_zero_rows_mask = np.any(self.new_dataset != 0, axis=1)
            num_non_zero_rows = np.sum(non_zero_rows_mask)
            num_of_class = num_non_zero_rows - ((i * 27) + (i * 33))

            while (num_of_class <= num_pos_par) and self.pos[0] < len(old_df):
                if old_df[self.pos[0]][total_num_col] == 1:
                    self.new_dataset[self.new_index] = old_df[self.pos[0]]
                    self.new_index = self.new_index + 1
                self.pos[0] = self.pos[0] + 1
                non_zero_rows_mask = np.any(self.new_dataset != 0, axis=1)
                num_non_zero_rows = np.sum(non_zero_rows_mask)
                num_of_class = num_non_zero_rows - ((i * 27) + (i * 33))

            while (num_of_class <= (num_neg_par + num_pos_par)) and self.pos[1] < len(old_df):
                if old_df[self.pos[1]][total_num_col] == 0:
                    self.new_dataset[self.new_index] = old_df[self.pos[1]]
                    self.new_index = self.new_index + 1
                # print(self.pos[1])
                self.pos[1] = self.pos[1] + 1
                non_zero_rows_mask = np.any(self.new_dataset != 0, axis=1)
                num_non_zero_rows = np.sum(non_zero_rows_mask)
                num_of_class = num_non_zero_rows - ((i * 27) + (i * 33))

            if i == 4:
                if self.pos[0] != len(old_df):
                    for j in range(self.pos[0]-1, len(old_df) - 1):
                        if old_df[j][total_num_col] == 1:
                            self.new_dataset[self.new_index] = old_df[j]
                            self.new_index = self.new_index + 1

                if self.pos[1] != len(old_df):
                    for j in range(self.pos[1]-1, len(old_df) - 1):
                        if old_df[j][total_num_col] == 0:
                            self.new_dataset[self.new_index] = old_df[j]
                            self.new_index = self.new_index + 1

        return self.new_dataset

    def five_kfold(self):
        for i in range(self.k):
            logistic_regression = LOGISTIC_REGRESSION_MODEL(self.new_dataset, 6, i, self.partition)
            logistic_regression.train_model()


