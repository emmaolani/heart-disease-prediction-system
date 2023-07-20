import numpy as np


class KFOLD:
    def __init__(self, old_dataset):
        self.k = 5
        self.old_dataset = old_dataset
        self.pos = [0, 0]
        self.partition = int(len(old_dataset.getter_data().to_numpy()) / 5)
        self.new_dataset = np.zeros((5, self.partition, 14))

    def __check_ratio_of_class(self):
        class_counts = self.old_dataset.getter_data()['target'].value_counts()
        total_samples = len(self.old_dataset.getter_data())
        class_percentages = class_counts / total_samples * 100
        return class_percentages.to_numpy()

    def balance_data_set(self):
        per = np.trunc(self.__check_ratio_of_class())
        num_neg_par = int((per[0] * self.partition) / 100)
        num_pos_par = int((per[1] * self.partition) / 100)
        old_df = self.old_dataset.getter_data().to_numpy()
        old_df = old_df.astype(float)

        total_num_col = len(old_df[0]) - 1
        # print(self.new_dataset)

        for i in range(self.k):
            neg = 0
            posi = 0
            non_zero_rows_mask = np.any(self.new_dataset[i] != 0, axis=1)
            num_non_zero_rows = np.sum(non_zero_rows_mask)
            while (num_non_zero_rows <= num_pos_par) and self.pos[0] < len(old_df):
                if old_df[self.pos[0]][total_num_col] == 1:
                    self.new_dataset[i][posi] = old_df[self.pos[0]]
                    posi = posi + 1
                    neg = neg + 1
                self.pos[0] = self.pos[0] + 1
                non_zero_rows_mask = np.any(self.new_dataset[i] != 0, axis=1)
                num_non_zero_rows = np.sum(non_zero_rows_mask)

            while (num_non_zero_rows <= (num_neg_par + num_pos_par)) and self.pos[1] < len(old_df):
                if old_df[self.pos[1]][total_num_col] == 0:
                    self.new_dataset[i][neg] = old_df[self.pos[1]]
                    neg = neg + 1
                    posi = posi + 1
                self.pos[1] = self.pos[1] + 1
                non_zero_rows_mask = np.any(self.new_dataset[i] != 0, axis=1)
                num_non_zero_rows = np.sum(non_zero_rows_mask)

            # if i == 4:
            #     for j in range(self.pos[0], len(old_df) - 1):
            #         if old_df[self.pos[0]][total_num_col] == 1:
            #             self.new_dataset[i] = self.new_dataset[i].reshape(1, -1)
            #             self.new_dataset[i] = np.vstack((self.new_dataset[i], old_df[self.pos[0]]))
            #             self.pos[0] = self.pos[0] + 1
            #
            #     for l in range(self.pos[1], len(old_df) - 1):
            #         if old_df[self.pos[1]][total_num_col] == 0:
            #             self.new_dataset[i] = np.vstack((self.new_dataset[i], old_df[self.pos[1]]))
            #             self.pos[1] = self.pos[1] + 1

        return self.new_dataset
