import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

data = pd.read_csv("heart.csv")

# feature selection
x = data.iloc[:, 0:13]
y = data.iloc[:, -1]

# apply SelectKBest class to extract top 5 feature
best_features = SelectKBest(score_func=chi2, k=13)
fit = best_features.fit(x, y)

df_scores = pd.DataFrame(fit.scores_)
df_columns = pd.DataFrame(x.columns)

features_scores = pd.concat([df_columns, df_scores], axis=1)
features_scores.columns = ['specs', 'scores']
print(features_scores)

# logistic regression gradient descent
x1 = data["age"].to_numpy()
x2 = data["sex"].to_numpy()
x3 = data["cp"].to_numpy()
x4 = data["trestbps"].to_numpy()
x5 = data["chol"].to_numpy()
x6 = data["fbs"].to_numpy()
x7 = data["restecg"].to_numpy()
x8 = data["thalach"].to_numpy()
x9 = data["exang"].to_numpy()
x10 = data["oldpeak"].to_numpy()
x11 = data["slope"].to_numpy()
x12 = data["ca"].to_numpy()
x13 = data["thal"].to_numpy()

x1_scal = (x1 - np.mean(x1)) / (np.max(x1) - np.min(x1))
x2_scal = (x2 - np.mean(x2)) / (np.max(x2) - np.min(x2))
x3_scal = (x3 - np.mean(x3)) / (np.max(x3) - np.min(x3))
x4_scal = (x4 - np.mean(x4)) / (np.max(x4) - np.min(x4))
x5_scal = (x5 - np.mean(x5)) / (np.max(x5) - np.min(x5))
x6_scal = (x6 - np.mean(x6)) / (np.max(x6) - np.min(x6))
x7_scal = (x7 - np.mean(x7)) / (np.max(x7) - np.min(x7))
x8_scal = (x8 - np.mean(x8)) / (np.max(x8) - np.min(x8))
x9_scal = (x9 - np.mean(x9)) / (np.max(x9) - np.min(x9))
x10_scal = (x10 - np.mean(x10)) / (np.max(x10) - np.min(x10))
x11_scal = (x11 - np.mean(x11)) / (np.max(x11) - np.min(x11))
x12_scal = (x12 - np.mean(x12)) / (np.max(x12) - np.min(x12))
x13_scal = (x13 - np.mean(x13)) / (np.max(x13) - np.min(x13))
y = data["target"].to_numpy()

slopes = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
sub_slop = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
intercept = 0
sub_intercept = 0
learning_rate = 0.01
jw = np.array([])
iterations = np.array([])


def lin_regression():
    matrix = np.hstack((x1_scal.reshape(-1, 1), x2_scal.reshape(-1, 1), x3_scal.reshape(-1, 1),
                        x4_scal.reshape(-1, 1), x5_scal.reshape(-1, 1), x6_scal.reshape(-1, 1),
                        x7_scal.reshape(-1, 1), x8_scal.reshape(-1, 1), x9_scal.reshape(-1, 1),
                        x10_scal.reshape(-1, 1), x11_scal.reshape(-1, 1), x12_scal.reshape(-1, 1),
                        x13_scal.reshape(-1, 1)))
    sub_reg = np.dot(matrix, slopes.reshape(-1, 1))
    reg = sub_reg.ravel() + intercept
    return reg


def lo():
    linear_reg = lin_regression()
    expon = np.exp(-1 * linear_reg)
    expon = expon + 1
    g = 1 / expon
    return g


def loss_function():
    linear_reg = lin_regression()
    expon = np.exp(-1 * linear_reg)
    g = 1 / (expon + 1)

    # calculate (f(x)-y)x
    loss_funct = g - y
    return loss_funct


def logistic_regression():
    loss_funct = loss_function()
    for j in range(0, len(sub_slop)):
        if j == 0:
            derived = loss_funct * x1_scal
        elif j == 1:
            derived = loss_funct * x2_scal
        elif j == 2:
            derived = loss_funct * x3_scal
        elif j == 3:
            derived = loss_funct * x4_scal
        elif j == 4:
            derived = loss_funct * x5_scal
        elif j == 5:
            derived = loss_funct * x6_scal
        elif j == 6:
            derived = loss_funct * x7_scal
        elif j == 7:
            derived = loss_funct * x8_scal
        elif j == 8:
            derived = loss_funct * x9_scal
        elif j == 9:
            derived = loss_funct * x10_scal
        elif j == 10:
            derived = loss_funct * x11_scal
        elif j == 11:
            derived = loss_funct * x12_scal
        elif j == 12:
            derived = loss_funct * x13_scal

        derived = derived.sum() / len(y)
        sub_slop[j] = derived


# for i in range(100000):
#     logistic_regression()
#     loss_int = loss_function()
#     sub_intercept = loss_int.sum() / len(y)
#
#     l = lo()
#     sub_jw = -y * np.log(l) - (1 - y) * np.log(1 - l)
#
#     jw = np.append(jw, sub_jw.sum() / len(y))
#     iterations = np.append(iterations, i)
#
#     slopes = slopes - (learning_rate * sub_slop)
#     intercept = intercept - (learning_rate * sub_intercept)
#
#     print(slopes)
#     print(intercept)
# [-0.7475503 - 1.77656537  2.53891356 - 1.73962548 - 1.72917586 - 0.07470799
#  0.84354497  2.5658856 - 1.01970267 - 3.27534977  1.17877764 - 2.97173739
#  - 2.63663567]
# -0.11459411028268236


print("feature", x1_scal[0], x2_scal[0], x3_scal[0], x4_scal[0], x5_scal[0], x6_scal[0], x7_scal[0], x8_scal[0], x9_scal[0],
      x10_scal[0], x11_scal[0], x12_scal[0], x13_scal[0])
print('target', y[0])

p = x1_scal[0] * -0.7475503 + x2_scal[0] * - 1.77656537 + x3_scal[0] * 2.53891356 + x4_scal[0] + - 1.73962548 + x5_scal[0] * -1.72917586 + x6_scal[0] * -0.07470799 + x7_scal[0] * 0.84354497 + x8_scal[0] * 2.5658856 + x9_scal[0] * - 1.01970267 + x10_scal[0] * - 3.27534977 + x11_scal[0] * 1.17877764 + x12_scal[0] * -2.97173739 + x13_scal[0] * - 2.63663567 + -0.11459411028268236

yhat = 1 / (1 + np.exp(-1 * p))
print('yhat', yhat)

# print(jw)
# print(iterations)
# plt.scatter(iterations, jw, c="blue")
# plt.show()

# print(x1_scal, x2_scal, x3_scal, x4_scal, x5_scal, x6_scal, x7_scal, x8_scal, x9_scal, x10_scal, x11_scal, x12_scal,
#       x13_scal, y)
