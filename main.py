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

y = data["target"].to_numpy()

row = x.to_numpy()
target = data.iloc[:, -1].to_numpy()
weights = np.transpose(row)

for i in range(0, len(weights)):
    mean = np.mean(weights[i])
    maxi = np.max(weights[i])
    mini = np.min(weights[i])
    weights[i] = (weights[i] - mean) / (maxi - mini)

scaled_row = np.transpose(weights)


slopes = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
sub_slop = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
intercept = 0
sub_intercept = 0
learning_rate = 0.01
jw = np.array([])
iterations = np.array([])


def lin_regression():
    sub_reg = np.dot(scaled_row, slopes.reshape(-1, 1))
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
        derived = loss_funct * weights[j]
        derived = derived.sum() / len(y)
        sub_slop[j] = derived


for i in range(50000):
    logistic_regression()
    loss_int = loss_function()
    sub_intercept = loss_int.sum() / len(y)

    l = lo()
    sub_jw = -y * np.log(l) - (1 - y) * np.log(1 - l)

    jw = np.append(jw, sub_jw.sum() / len(y))
    iterations = np.append(iterations, i)

    slopes = slopes - (learning_rate * sub_slop)
    intercept = intercept - (learning_rate * sub_intercept)

    print(slopes)
    print(intercept)

# [-0.7475503 - 1.77656537  2.53891356 - 1.73962548 - 1.72917586 - 0.07470799
#  0.84354497  2.5658856 - 1.01970267 - 3.27534977  1.17877764 - 2.97173739
#  - 2.63663567]
# -0.11459411028268236


print(jw)
print(iterations)
plt.scatter(iterations, jw, c="blue")
plt.show()

