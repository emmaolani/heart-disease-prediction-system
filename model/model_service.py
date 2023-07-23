import numpy as np
import matplotlib.pyplot as plt


class LOGISTIC_REGRESSION_MODEL:
    def __init__(self, data, num, itr, partition_num):
        self.num_of_attribute = num
        self.start_index = itr * partition_num
        self.end_index = (itr * partition_num) + (partition_num + 1)

        self.raw_x_train = np.concatenate((data[:self.start_index], data[self.end_index:]), axis=0)
        self.x_train = self.raw_x_train[:, 0:num]
        self.scaled_x_train = -1
        self.y_train = self.raw_x_train[:, -1]

        self.raw_x_test = data[self.start_index:self.end_index]
        self.x_test = self.raw_x_test[:, 0:num]
        self.scaled_x_test = -1
        self.y_test = self.raw_x_test[:, -1]
        self.predictions = []

        self.slopes = np.zeros(num, dtype=float)
        self.sub_slope = np.zeros(num, dtype=float)
        self.intercept = 0
        self.sub_intercept = 0
        self.learning_rate = 0.01
        self.jw = np.array([])
        self.iterations = np.array([])

    def __scale_function(self):
        weights_train = np.transpose(self.x_train)
        weights_test = np.transpose(self.x_test)

        for i in range(0, len(weights_train)):
            mean = np.mean(weights_train[i])
            maxi = np.max(weights_train[i])
            mini = np.min(weights_train[i])
            weights_train[i] = (weights_train[i] - mean) / (maxi - mini)

        for i in range(0, len(weights_test)):
            mean = np.mean(weights_test[i])
            maxi = np.max(weights_test[i])
            mini = np.min(weights_test[i])
            weights_test[i] = (weights_test[i] - mean) / (maxi - mini)

        self.scaled_x_train = np.transpose(weights_train)
        self.scaled_x_test = np.transpose(weights_test)

    def __linear_combination(self):
        sub_combination = np.dot(self.scaled_x_train, self.slopes.reshape(-1, 1))
        combination = sub_combination.ravel() + self.intercept
        return combination

    def __sigmoid_function(self):
        linear_combination = self.__linear_combination()
        expon = np.exp(-1 * linear_combination)
        expon = expon + 1
        g = 1 / expon
        return g

    def __loss_function(self):
        linear_combination = self.__linear_combination()
        expon = np.exp(-1 * linear_combination)
        expon = expon + 1
        g = 1 / expon
        # calculate (f(x)-y)x
        loss_funct = g - self.y_train
        return loss_funct

    def __logistic_regression(self):
        loss_funct = self.__loss_function()
        transpose_x_train = np.transpose(self.x_train)
        for j in range(self.num_of_attribute):
            derived = loss_funct * transpose_x_train[j]
            derived = derived.sum() / len(self.y_train)
            self.sub_slope = derived

    def train_model(self):
        self.__scale_function()
        for i in range(100000):
            self.__logistic_regression()
            loss_int = self.__loss_function()
            self.sub_intercept = loss_int.sum() / len(self.y_train)

            l = self.__sigmoid_function()
            sub_jw = -self.y_train * np.log(l) - (1 - self.y_train) * np.log(1 - l)
            self.jw = np.append(self.jw, sub_jw.sum() / len(self.y_train))
            self.iterations = np.append(self.iterations, i)

            self.slopes = self.slopes - (self.learning_rate * self.sub_slope)
            self.intercept = self.intercept - (self.learning_rate * self.sub_intercept)

            # print(self.slopes)
            # print(self.intercept)

        sub_combination = np.dot(self.scaled_x_test, self.slopes.reshape(-1, 1))
        combination = sub_combination.ravel() + self.intercept
        expon = np.exp(-1 * combination)
        expon = expon + 1
        g = 1 / expon
        self.predictions = g
        print('Y-hat', g)
        print('Y', len(self.y_test))
        # print(self.jw)
        # print(self.iterations)
        plt.scatter(self.iterations, self.jw, c="blue")
        plt.show()








# arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18]])
# # Define the range of indices you want to remove (1 to 10, inclusive)
# start_index = 1
# end_index = 4
# # Remove the specified rows
# new_arr = np.concatenate((arr[:start_index], arr[end_index:]), axis=0)
# deleted_rows = arr[start_index:end_index]
# print("Modified array:")
# print(new_arr)
# print("Deleted rows:")
# print(deleted_rows)
#
